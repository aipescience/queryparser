# -*- coding: utf-8 -*-
"""
PostgreSQL processor. Its task is to check if a query has any syntax errors and
to extract all accessed columns as well as keywords and functions being
used in a query.

"""

from __future__ import (absolute_import, print_function)

__all__ = ["PostgreSQLQueryProcessor"]

import antlr4
import sys

from .PostgreSQLLexer import PostgreSQLLexer
from .PostgreSQLParser import PostgreSQLParser
from .PostgreSQLParserListener import PostgreSQLParserListener

from ..exceptions import QueryError, QuerySyntaxError

from .postgresqllisteners import PgSphereListener

from ..common import parse_alias, process_column_name,\
        get_column_name_listener, get_schema_name_listener,\
        get_remove_subqueries_listener, get_query_listener,\
        SyntaxErrorListener,\
        get_column_keyword_function_listener


class PostgreSQLQueryProcessor(object):
    """
    Object used for processing PostgreSQL queries. Its objective is query
    validation (syntax error detection )and extraction of used columns,
    keywords and functions.

    :param query:
        PostgreSQL query string.

    """
    def __init__(self, query=None):
        self.walker = antlr4.ParseTreeWalker()
        self.columns = set()
        self.keywords = set()
        self.functions = set()
        self.display_columns = []
        self.syntax_error_listener = SyntaxErrorListener()

        if query is not None:
            self.set_query(query)
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

        # Keep track of the ctx stack
        ctx_stack = []

        for i in column_keyword_function_listener.data:
            if isinstance(i[1], PostgreSQLParser.Displayed_columnContext):
                # this happens if there is an expression involving
                # more columns
                if len(i[2]) > 1:
                    for j in i[2]:
                        other_columns.append([j])
                else:
                    select_list_columns.append(i[2])
                alias = parse_alias(i[1].alias(), '"')
                if alias is not None:
                    column_aliases.append(alias)
                ctx_stack.append(i)

            if isinstance(i[1], PostgreSQLParser.Table_atomContext):
                select_list_tables.append([i[2], i[0]])
                ctx_stack.append(i)

            if isinstance(i[1], PostgreSQLParser.Table_referencesContext):
                if len(i) > 2:
                    select_list_table_references.extend(i[2])
                    ctx_stack.append(i)

            if isinstance(i[1], PostgreSQLParser.Select_listContext):
                if len(i) == 3:
                    select_list_columns.append([[i[2][0][0] + [i[1]],
                                                i[2][0][1]]])
                    ctx_stack.append(i)

            if isinstance(i[1], PostgreSQLParser.Where_clauseContext) or\
               isinstance(i[1], PostgreSQLParser.Having_clauseContext):
                if len(i[2]) > 1:
                    for j in i[2]:
                        other_columns.append([j])
                else:
                    other_columns.append(i[2])
                ctx_stack.append(i)

            if isinstance(i[1], PostgreSQLParser.Join_conditionContext):
                join = i[0]
                join_using = i[2]

                # if USING we need all columns in all columns if they
                # have no references
                if i[1].USING_SYM():
                    for ctx in ctx_stack[::-1]:
                        if not isinstance(ctx[1],
                                          PostgreSQLParser.Table_atomContext):
                            break
                        for ju in join_using:
                            if ju[0][1] is None:
                                other_columns.append([[[ctx[2][0][0],
                                                        ctx[2][0][1],
                                                        ju[0][2],
                                                        ctx[1]], None]])
                elif i[1].ON():
                    if len(i[2]) > 1:
                        for j in i[2]:
                            other_columns.append([j])

                ctx_stack.append(i)

            if isinstance(i[1], PostgreSQLParser.Orderby_clauseContext):
                if len(i[2]) > 1:
                    for j in i[2]:
                        go_columns.append([j])
                else:
                    go_columns.append(i[2])
                ctx_stack.append(i)

            if isinstance(i[1], PostgreSQLParser.Groupby_clauseContext):
                if len(i[2]) > 1:
                    for j in i[2]:
                        go_columns.append([j])
                else:
                    go_columns.append(i[2])
                ctx_stack.append(i)

        return select_list_columns, select_list_tables,\
            select_list_table_references, other_columns, go_columns, join,\
            join_using, column_aliases

    def _get_budget_column(self, c, tab, ref):
        cname = c[0][2]
        cctx = c[0][3]
        calias = c[1]
        t = tab

        column_found = False

        for bc in ref:
            if bc[0][2] == '*':
                t = [[bc[0][0], bc[0][1]], 'None']
                column_found = True
                break
            elif bc[1] and c[0][2] == bc[1]:
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

        return cname, cctx, calias, column_found, t

    def _extract_columns(self, columns, select_list_tables, ref_dict, join,
                         budget, column_aliases, touched_columns=None,
                         subquery_contents=None):

        # Here we store all columns that might have references somewhere
        # higer up in the tree structure. We'll revisit them later.
        missing_columns = []
        remove_column_idxs = []

        for i, col in enumerate(columns):
            c = col[0]

            cname = c[0][2]
            cctx = c[0][3]
            calias = c[1]

            # if * is selected we don't care too much
            #  if c[0][0] is None and c[0][1] is None and c[0][2] == '*':
                #  for slt in select_list_tables:
                    #  extra_columns.append([[slt[0][0][0], slt[0][0][1], cname,
                                           #  c[0][3]], calias])
                #  remove_column_idxs.append(i)
                #  continue

            # this can happen for example in ... WHERE EXISTS ... clauses
            if cname is None and calias is None:
                remove_column_idxs.append(i)
                continue

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
                    cname, cctx, calias, column_found, tab =\
                            self._get_budget_column(c, tab, budget[-1][2])
                    # raise an ambigous column
                    if column_found and c[0][1] is None:
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
                    cname, cctx, calias, column_found, tab =\
                            self._get_budget_column(c, tab, ref[2])

                    ref_cols = [j[0][2] for j in ref[2]]
                    if not column_found and c[0][1] is not None\
                            and c[0][1] != tab[0][1] and '*' not in ref_cols:
                        raise QueryError("Unknown column '%s.%s'." % (c[0][1],
                                                                      c[0][2]))

                else:
                    # ref is a table
                    tab = ref[0]

            except KeyError:
                if None not in c[0]:
                    cname = c[0][2]
                    cctx = c[0][3]
                    calias = c[1]
                    tab = [[c[0][0], c[0][1]]]
                    column_found = True

                # table is either referenced directly or by an alias
                elif c[0][2] is not None and c[0][1] is not None:
                    if subquery_contents is not None:
                        try:
                            contents = subquery_contents[c[0][1]]
                            cname, cctx, calias, column_found, tab =\
                                self._get_budget_column(c, tab, contents)

                        except KeyError:
                            tabs = [j[0][0][:2] for j in
                                    subquery_contents.values()]
                            tabs += [j[0][0] for j in select_list_tables]
                            column_found = False
                            for t in tabs:
                                if t[1] == c[0][1]:
                                    cname = c[0][2]
                                    cctx = c[0][3]
                                    calias = c[1]
                                    tab = [t]
                                    column_found = True

                            if not column_found:
                                missing_columns.append(c)
                                columns[i] = [[c[0][0], c[0][1],
                                               c[0][2], c[0][3]], c[1]]
                                if touched_columns is not None:
                                    touched_columns.append([[c[0][0], c[0][1],
                                                           c[0][2], c[0][3]],
                                                           c[1]])
                                continue
                    else:
                        if tab[0][1] == c[0][1]:
                            columns[i] = [[tab[0][0], tab[0][1],
                                          c[0][2], c[0][3]], c[1]]
                        else:

                            missing_columns.append(c)
                            columns[i] = [[c[0][0], c[0][1],
                                           c[0][2], c[0][3]], c[1]]
                            if touched_columns is not None:
                                touched_columns.append([[c[0][0], c[0][1],
                                                       c[0][2], c[0][3]],
                                                       c[1]])
                        continue

                elif c[0][2] is not None and c[0][2] != '*' and c[0][1] is \
                        None and len(ref_dict.keys()) > 1 and not join:
                    raise QueryError("Column '%s' is ambiguous." % c[0][2])

                elif len(budget) and tab[0][0] is None and tab[0][1] is None:
                    ref = budget[-1]
                    column_found = False

                    if isinstance(ref[0], int):
                        cname, cctx, calias, column_found, tab =\
                                self._get_budget_column(c, tab, ref[2])

                        # We allow None.None colunms because they are produced
                        # by count(*)
                        if not column_found and c[0][2] is not None\
                                and c[0][2] not in column_aliases:
                            raise QueryError("Unknown column '%s'." % c[0][2])

            if touched_columns is not None:
                touched_columns.append([[tab[0][0], tab[0][1], cname, cctx],
                                        calias])
            else:
                columns[i] = [[tab[0][0], tab[0][1], cname, c[0][3]], calias]

        for i in remove_column_idxs[::-1]:
            columns.pop(i)

        return missing_columns

    def process_query(self, replace_schema_name=None, indexed_objects=None):
        """
        Parses and processes the query. After a successful run it fills up
        columns, keywords, functions and syntax_errors lists.

        """
        # Antlr objects
        inpt = antlr4.InputStream(self.query)
        lexer = PostgreSQLLexer(inpt)
        #  lexer.removeErrorListeners()
        stream = antlr4.CommonTokenStream(lexer)
        parser = PostgreSQLParser(stream)
        lexer._listeners = [self.syntax_error_listener]
        parser._listeners = [self.syntax_error_listener]

        # Parse the query
        tree = parser.query()
        if len(self.syntax_error_listener.syntax_errors):
            raise QuerySyntaxError(self.syntax_error_listener.syntax_errors)

        if replace_schema_name is not None:
            schema_name_listener = get_schema_name_listener(
                    PostgreSQLParserListener, '"')(replace_schema_name)
            self.walker.walk(schema_name_listener, tree)
            self._query = stream.getText()

        query_listener = get_query_listener(PostgreSQLParserListener,
                PostgreSQLParser, '"')()
        subquery_aliases = [None]
        keywords = []
        functions = []
        tables = []

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

        # Iterate through subqueries starting with the lowerst level
        for ccc, ctx in enumerate(query_listener.select_expressions[::-1]):
            remove_subquieries_listener = get_remove_subqueries_listener(
                    PostgreSQLParserListener, PostgreSQLParser)(ctx.depth())
            #column_keyword_function_listener = ColumnKeywordFunctionListener()
            column_keyword_function_listener = \
                    get_column_keyword_function_listener(
                            PostgreSQLParserListener, '"')()

            # Remove nested subqueries from select_expressions
            self.walker.walk(remove_subquieries_listener, ctx)

            # Extract table and column names, keywords, functions
            self.walker.walk(column_keyword_function_listener, ctx)

            keywords.extend(column_keyword_function_listener.keywords)
            functions.extend(column_keyword_function_listener.functions)

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

            #tables.extend([i[0][0] for i in select_list_tables])
            tables.extend([i[0] for i in select_list_tables])

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

                budget.extend(join_columns)

            if subquery_alias is not None:
                subquery_contents[subquery_alias] = current_columns

        if len(missing_columns):
            mc = self._extract_columns(missing_columns, select_list_tables,
                                       ref_dict, join, budget,
                                       column_aliases_from_previous,
                                       touched_columns, subquery_contents)
            if len(mc):
                unref_cols = "', '".join(['.'.join([j for j in i[0][:3] if j])
                                         for i in mc])
                raise QueryError("Unreferenced column(s): '%s'." % unref_cols)

        # If we have indexed_objects, we are also accessing those. We
        # need to add them into the columns stack:
        if indexed_objects is not None:
            for k, v in indexed_objects.items():
                for vals in v:
                    touched_columns.append([[vals[0][0], vals[0][1], vals[2], None], None])

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

        columns = list(set(touched_columns).difference(del_columns))
        self.columns = list(set([self._strip_column(i) for i in columns]))
        self.keywords = list(set(keywords))
        self.functions = list(set(functions))
        self.display_columns = [(i[0].lstrip('"').rstrip('"'),
                                list(self._strip_column(i[1])))
                                for i in display_columns]

        self.tables = list(set([tuple([i[0][0].lstrip('"').rstrip('"')
                        if i[0][0] is not None else i[0][0],
                        i[0][1].lstrip('"').rstrip('"')
                        if i[0][1] is not None else i[0][1]]) for i in tables]))

        # If there are any pg_sphere objects that are indexed we need
        # to replace the ADQL translated query parts with the indexed column
        # names
        if indexed_objects is not None:
            # we need to correctly alias 'pos' columns
            for k, v in indexed_objects.items():
                indexed_objects[k] = list([list(i) for i in v])
                for i, vals in enumerate(v):
                    for t in tables:
                        if vals[0][0] == t[0][0] and vals[0][1] == t[0][1] and t[1] is not None:
                            indexed_objects[k][i][2] = t[1] + '.' + indexed_objects[k][i][2]

            pg_sphere_listener = PgSphereListener(columns, indexed_objects)
            self.walker.walk(pg_sphere_listener, tree)
            for k, v in pg_sphere_listener.replace_dict.items():
                self._query = self._query.replace(k, v)

    @property
    def query(self):
        """
        Get the query string.

        """
        return self._query

    def _strip_query(self, query):
        if sys.version_info[0] < 3:
            try:
                query = unicode(query, 'utf-8')
            except TypeError:
                # already unicode so we don't do anything
                pass
        return query.lstrip('\n').rstrip().rstrip(';') + ';'

    def _strip_column(self, col):
        scol = [None, None, None]
        for i in range(3):
            if col[i] is not None:
                scol[i] = col[i].lstrip('"').rstrip('"')
        return tuple(scol)

    def set_query(self, query):
        """
        Helper to set the query string.
        """
        self.columns = set()
        self.keywords = set()
        self.functions = set()
        self.display_columns = []
        self.syntax_error_listener = SyntaxErrorListener()
        self._query = self._strip_query(query)
