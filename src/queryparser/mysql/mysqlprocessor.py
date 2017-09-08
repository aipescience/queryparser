# -*- coding: utf-8 -*-
"""
MySQL processor. Its task is to check if a query has any syntax errors and
to extract all accessed columns as well as keywords and functions being
used in a query.

"""

from __future__ import (absolute_import, print_function)

__all__ = ["MySQLQueryProcessor"]

import antlr4

from .MySQLLexer import MySQLLexer
from .MySQLParser import MySQLParser

from ..exceptions import QueryError, QuerySyntaxError

from .mysqllisteners import ColumnKeywordFunctionListener,\
        QueryListener, RemoveSubqueriesListener, SyntaxErrorListener,\
        SchemaNameListener

from .mysqllisteners import parse_alias


class MySQLQueryProcessor(object):
    """
    Object used for processing MySQL queries. Its objective is query validation
    (syntax error detection )and extraction of used columns, keywords and
    functions.

    :param query:
        MySQL query string.

    :param strict: (optional)
        If set to True ambiguous columns (b) in queries such as
            SELECT a, b FROM db.tab1
            JOIN (
                SELECT id, col AS b FROM db.tab2
            ) AS sub USING(id)
        will raise a ``QueryError``.

    """
    def __init__(self, query=None, strict=False):
        self.walker = antlr4.ParseTreeWalker()

        self.columns = set()
        self.keywords = set()
        self.functions = set()
        self.display_columns = []
        self.syntax_error_listener = SyntaxErrorListener()
        self._strict = strict
        if query is not None:
            self._query = self._strip_query(query)
            self.process_query()

    def _extract_instances(self, column_keyword_function_listener):
        select_list_columns = []
        other_columns = []
        go_columns = []
        column_aliases = []
        select_list_tables = []
        select_list_table_references = []
        join = 0
        join_using = None

        for i in column_keyword_function_listener.data:
            if isinstance(i[1], MySQLParser.Displayed_columnContext):
                # this happens if there is an expression involving
                # more columns
                if len(i[2]) > 1:
                    for j in i[2]:
                        other_columns.append([j])
                else:
                    select_list_columns.append(i[2])
                alias = parse_alias(i[1].alias())
                if alias is not None:
                    column_aliases.append(alias)

            if isinstance(i[1], MySQLParser.Table_atomContext):
                select_list_tables.append([i[2], i[0]])

            if isinstance(i[1], MySQLParser.Table_referencesContext):
                if len(i) > 2:
                    select_list_table_references.extend(i[2])

            if isinstance(i[1], MySQLParser.Select_listContext):
                if len(i) == 3:
                    select_list_columns.append(i[2])

            if isinstance(i[1], MySQLParser.Where_clauseContext):
                if len(i[2]) > 1:
                    for j in i[2]:
                        other_columns.append([j])
                else:
                    other_columns.append(i[2])

            if isinstance(i[1], MySQLParser.Join_conditionContext):
                join = i[0]
                if len(i[2]) > 1:
                    for j in i[2]:
                        other_columns.append([j])
                join_using = i[2]

            if isinstance(i[1], MySQLParser.Orderby_clauseContext):
                if len(i[2]) > 1:
                    for j in i[2]:
                        go_columns.append([j])
                else:
                    go_columns.append(i[2])

            if isinstance(i[1], MySQLParser.Groupby_clauseContext):
                if len(i[2]) > 1:
                    for j in i[2]:
                        go_columns.append([j])
                else:
                    go_columns.append(i[2])

        return select_list_columns, select_list_tables,\
            select_list_table_references, other_columns, go_columns, join,\
            join_using, column_aliases

    def _get_budget_column(self, c, tab, ref):
        cname = c[0][2]
        calias = c[1]
        t = tab

        column_found = False

        for bc in ref:
            if bc[1] and c[0][2] == bc[1]:
                t = [[bc[0][0], bc[0][1]], 'None']
                cname = bc[0][2]
                if c[1] is None:
                    calias = c[0][2]
                column_found = True
                break
            elif c[0][2] == bc[0][2] and bc[1] is None:
                t = [[bc[0][0], bc[0][1]], 'None']
                column_found = True
                break

        return cname, calias, column_found, t

    def _extract_columns(self, columns, select_list_tables, ref_dict, join,
                         budget, column_aliases, touched_columns=None,
                         subquery_contents=None):

        # Here we store all columns that might have references somewhere
        # higer up in the tree structure. We'll revisit them later.
        missing_columns = []

        for i, col in enumerate(columns):
            c = col[0]

            cname = c[0][2]
            calias = c[1]

            tab = [[None, None], None]
            try:
                tab = select_list_tables[0][0]
                if tab[0][0] is None:
                    raise QueryError('Missing schema specification.')

                # We have to check if we also have a join on the same level
                # and we are actually touching a column from the joined table
                if join and c[0][2] != '*' and\
                        (tab[1] != c[0][1] or
                         (tab[1] is None and c[0][1] is None)):
                    cname, calias, column_found, tab =\
                            self._get_budget_column(c, tab, budget[-1][2])
                    # raise an ambigous column if using strict
                    if column_found and self._strict and c[0][1] is None:
                        raise QueryError("Column '%s' is possibly ambiguous."
                                         % c[0][2])

            except IndexError:
                pass

            try:
                # ref can be a table or a budget of columns
                ref = ref_dict[c[0][1]]
                column_found = False

                if isinstance(ref[0], int):
                    # ref is a budget column
                    cname, calias, column_found, tab =\
                            self._get_budget_column(c, tab, ref[2])

                    if not column_found and c[0][1] is not None\
                            and c[0][1] != tab[0][1]:
                        raise QueryError("Unknown column '%s.%s'." % (c[0][1],
                                                                      c[0][2]))

                else:
                    # ref is a table
                    tab = ref[0]

            except KeyError:
                if c[0][2] is not None and c[0][1] is not None:
                    if subquery_contents is not None:
                        try:
                            contents = subquery_contents[c[0][1]]
                            cname, calias, column_found, tab =\
                                self._get_budget_column(c, tab, contents)

                        except KeyError:
                            missing_columns.append(c)
                            columns[i] = [[c[0][0], c[0][1], c[0][2]], c[1]]
                            if touched_columns is not None:
                                touched_columns.append([[c[0][0], c[0][1],
                                                       c[0][2]], c[1]])
                            continue
                    else:
                        missing_columns.append(c)
                        columns[i] = [[c[0][0], c[0][1], c[0][2]], c[1]]
                        if touched_columns is not None:
                            touched_columns.append([[c[0][0], c[0][1],
                                                   c[0][2]], c[1]])
                        continue

                elif c[0][2] is not None and c[0][1] is None and\
                        len(ref_dict.keys()) > 1 and not join:
                    raise QueryError("Column '%s' is ambiguous." % c[0][2])

                elif len(budget) and tab[0][0] is None and tab[0][1] is None:
                    ref = budget[-1]
                    column_found = False

                    if isinstance(ref[0], int):
                        cname, calias, column_found, tab =\
                                self._get_budget_column(c, tab, ref[2])

                        # We allow None.None colunms because they are produced
                        # by count(*)
                        if not column_found and c[0][2] is not None\
                                and c[0][2] not in column_aliases:
                            raise QueryError("Unknown column '%s'." % c[0][2])

            if touched_columns is not None:
                touched_columns.append([[tab[0][0], tab[0][1], cname], calias])
            else:
                columns[i] = [[tab[0][0], tab[0][1], cname], calias]

        return missing_columns

    def process_query(self, replace_schema_name={}):
        """
        Parses and processes the query. After a successful run it fills up
        columns, keywords, functions and syntax_errors lists.

        :param strict: (optional)
            Dictionary of replacement schema names. If it is provided
            each key schema name will be replaced with its value.

        """
        # Antlr objects
        inpt = antlr4.InputStream(self.query)
        lexer = MySQLLexer(inpt)
        stream = antlr4.CommonTokenStream(lexer)
        parser = MySQLParser(stream)
        parser._listeners = [self.syntax_error_listener]

        # Parse the query
        tree = parser.query()
        if len(self.syntax_error_listener.syntax_errors):
            raise QuerySyntaxError(self.syntax_error_listener.syntax_errors)

        if len(replace_schema_name.items()):
            schema_name_listener = SchemaNameListener(replace_schema_name)
            self.walker.walk(schema_name_listener, tree)
            self._query = stream.getText()

        query_listener = QueryListener()
        subquery_aliases = [None]
        keywords = []
        functions = []

        self.walker.walk(query_listener, tree)
        keywords.extend(query_listener.keywords)
        subquery_aliases = query_listener.subquery_aliases

        # Columns that are accessed by the query
        touched_columns = []
        # List we use to propagete the columns through the tree
        budget = []
        # Are there any joins in the query?
        join = 0

        missing_columns = []

        column_aliases = []
        column_aliases_from_previous = []

        subquery_contents = {}

        # Check if we have non-unique subquery aliases
        if len(set(subquery_aliases.values())) !=\
                len(subquery_aliases.values()):
            raise QueryError('Query includes non-unique subquery aliases.')

        # Iterate through subqueries starting with the lowerst level
        for ccc, ctx in enumerate(query_listener.select_expressions[::-1]):
            remove_subquieries_listener = RemoveSubqueriesListener(ctx.depth())
            column_keyword_function_listener = ColumnKeywordFunctionListener()

            # Remove nested subqueries from select_expressions
            self.walker.walk(remove_subquieries_listener, ctx)

            # Extract table and column names, keywords, functions
            self.walker.walk(column_keyword_function_listener, ctx)

            keywords.extend(column_keyword_function_listener.keywords)
            functions.extend(column_keyword_function_listener.functions)

            # Let's make sure we have a select expression context
            #  if not isinstance(column_keyword_function_listener.data[0][1],
            #                    MySQLParser.Select_expressionContext):
            #      continue

            # Does the subquery has an alias?
            try:
                subquery_alias = subquery_aliases[ctx]
            except KeyError:
                subquery_alias = None

            current_depth = column_keyword_function_listener.data[0][0]

            # We get the columns from the select list along with all
            # other touched columns and any posible join conditions
            column_aliases_from_previous = [i for i in column_aliases]
            select_list_columns, select_list_tables,\
                select_list_table_references, other_columns, go_columns, join,\
                join_using, column_aliases =\
                self._extract_instances(column_keyword_function_listener)

            # Then we need to connect the column names s with tables and
            # databases

            ref_dict = {}

            for ref in select_list_table_references:
                ref_found = False
                for tab in select_list_tables:
                    if ref == tab[0][1]:
                        ref_dict[ref] = tab
                        ref_found = True

                if not ref_found:
                    for b in budget:
                        if ref == b[1]:
                            ref_dict[ref] = b
                            #  ref_found = True

                #  if not ref_found:
                    #  raise QueryError('Missing table reference %s.' % ref)

            if not len(select_list_table_references):
                for table in select_list_tables:
                    ref_dict[table[0][0][1]] = table

            mc = self._extract_columns(select_list_columns, select_list_tables,
                                       ref_dict, join, budget,
                                       column_aliases_from_previous)
            missing_columns.extend([[i] for i in mc])

            touched_columns.extend(select_list_columns)
            current_columns = [i for i in select_list_columns]
            budget.append([current_depth, subquery_alias, select_list_columns])

            aliases = [i[1] for i in select_list_columns] + column_aliases
            for col in go_columns:
                if col[0][0][2] not in aliases:
                    other_columns.append(col)

            mc = self._extract_columns(other_columns, select_list_tables,
                                       ref_dict, join, budget,
                                       column_aliases_from_previous,
                                       touched_columns)

            missing_columns.extend([[i] for i in mc])

            if join:
                join_columns = []
                join_columns.append(budget.pop(-1))
                if len(join_using) == 1:
                    for tab in select_list_tables:
                        touched_columns.append([[tab[0][0][0], tab[0][0][1],
                                                 join_using[0][0][2]], None])
                bp = []
                for b in budget[::-1]:
                    if b[0] > current_depth:
                        bp.append(budget.pop(-1)[2])

                # check if the join_column is in each sub select_list
                #  for b in bp:
                #  bcols = [i[0][2] for i in b]
                #  if join_using[0][0][2] not in bcols and '*' not in bcols
                #  raise QueryError('Missing join column `%s`.' %
                #                         #  join_using[0][0][2])
                budget.extend(join_columns)

            if subquery_alias is not None:
                subquery_contents[subquery_alias] = current_columns

        if len(missing_columns):
            mc = self._extract_columns(missing_columns, select_list_tables,
                                       ref_dict, join, budget,
                                       column_aliases_from_previous,
                                       touched_columns, subquery_contents)
            if len(mc):
                unref_cols = "', '".join(['.'.join([j for j in i[0] if j])
                                         for i in mc])
                raise QueryError("Unreferenced column(s): '%s'." % unref_cols)

        touched_columns = set([tuple(i[0]) for i in touched_columns])

        # extract display_columns
        display_columns = []
        mc = self._extract_columns([[i] for i in budget[-1][2]],
                                   select_list_tables, ref_dict, join, budget,
                                   column_aliases_from_previous,
                                   display_columns, subquery_contents)

        display_columns = [[i[1] if i[1] else i[0][2], i[0]]
                           for i in display_columns]

        # Let's get rid of all columns that are already covered by
        # db.tab.*. Figure out a better way to do it and replace the code
        # below.
        asterisk_columns = []
        del_columns = []
        for col in touched_columns:
            if col[2] == '*':
                asterisk_columns.append(col)

        for acol in asterisk_columns:
            for col in touched_columns:
                if acol[0] == col[0] and acol[1] == col[1] and \
                        acol[2] != col[2]:
                    del_columns.append(col)

        self.columns = list(set(touched_columns).difference(del_columns))
        self.keywords = list(set(keywords))
        self.functions = list(set(functions))
        self.display_columns = [(i[0], i[1]) for i in display_columns]

    @property
    def query(self):
        """
        Get the query string.

        """
        return self._query

    @property
    def strict(self):
        """
        Get the strict flag.

        """
        return self._strict

    def _strip_query(self, query):
        return query.lstrip('\n').rstrip().rstrip(';') + ';'

    def set_query(self, query):
        """
        Helper to set the query string.

        """
        self.columns = set()
        self.keywords = set()
        self.functions = set()
        self.display_columns = []
        self._query = self._strip_query(query)
