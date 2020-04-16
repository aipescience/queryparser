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
from .MySQLParserListener import MySQLParserListener

from ..exceptions import QueryError, QuerySyntaxError

from ..common import parse_alias, process_column_name,\
        get_schema_name_listener,\
        get_remove_subqueries_listener, get_query_listener,\
        get_column_keyword_function_listener,\
        SQLQueryProcessor


class MySQLQueryProcessor(SQLQueryProcessor):

    def __init__(self, query=None):
        super().__init__(MySQLParser, query)

    def process_query(self, replace_schema_name={}):
        """
        Parses and processes the query. After a successful run it fills up
        columns, keywords, functions and syntax_errors lists.

        """
        # Antlr objects
        inpt = antlr4.InputStream(self.query)
        lexer = MySQLLexer(inpt)
        stream = antlr4.CommonTokenStream(lexer)
        parser = MySQLParser(stream)
        lexer._listeners = [self.syntax_error_listener]
        parser._listeners = [self.syntax_error_listener]

        # Parse the query
        tree = parser.query()
        if len(self.syntax_error_listener.syntax_errors):
            raise QuerySyntaxError(self.syntax_error_listener.syntax_errors)

        if len(replace_schema_name.items()):
            schema_name_listener = get_schema_name_listener(
                    MySQLParserListener, '`')(replace_schema_name)
            self.walker.walk(schema_name_listener, tree)
            self._query = stream.getText()

        query_listener = get_query_listener(MySQLParserListener,
                MySQLParser, '`')()
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
                    MySQLParserListener, MySQLParser)(ctx.depth())
            #column_keyword_function_listener = ColumnKeywordFunctionListener()
            column_keyword_function_listener = \
                    get_column_keyword_function_listener(
                            MySQLParserListener, '`')()

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
        self.display_columns = [(i[0].lstrip('`').rstrip('`'),
                                list(self._strip_column(i[1])))
                                for i in display_columns]

        self.tables = list(set([tuple([i[0][0].lstrip('`').rstrip('`')
                        if i[0][0] is not None else i[0][0],
                        i[0][1].lstrip('`').rstrip('`')
                        if i[0][1] is not None else i[0][1]]) for i in tables]))
