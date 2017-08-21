# -*- coding: utf-8 -*-
"""
MySQL processor. Its task is to check if a query has any syntax errors and
to extract all accessed columns as well as keywords and functions being
used in a query.

"""

from __future__ import (absolute_import, print_function)

__all__ = ["MySQLQueryProcessor"]

import re

import antlr4
from antlr4.error.ErrorListener import ErrorListener

from .MySQLLexer import MySQLLexer
from .MySQLParser import MySQLParser
from .MySQLParserListener import MySQLParserListener

from queryparser import QueryError


def parse_alias(alias):
    """
    Extract the alias if available.

    :param alias:
        antlr context.

    """
    if alias:
        alias = alias.ID().getText().strip('`')
    else:
        alias = None
    return alias


def process_column_name(column_name_listener, walker, ctx):
    cn = []
    column_name_listener.column_name = []
    walker.walk(column_name_listener, ctx)
    if column_name_listener.column_name:
        for i in column_name_listener.column_name:
            cni = [None, None, None]
            if i.schema_name():
                cni[0] = i.schema_name().getText().replace('`', '')
            if i.table_name():
                cni[1] = i.table_name().getText().replace('`', '')
            if i.column_name():
                cni[2] = i.column_name().getText().replace('`', '')
            cn.append(cni)
    else:
        try:
            ctx.ASTERISK()
            ts = ctx.table_spec()
            cn = [[None, None, '*']]
            if ts.schema_name():
                cn[0][0] = ts.schema_name().getText().replace('`', '')
            if ts.table_name():
                cn[0][1] = ts.table_name().getText().replace('`', '')
        except AttributeError:
            cn = [[None, None, None]]

    return cn


def process_table_name(table_name_listener, walker, ctx):
    table_name_listener.table_names = []
    walker.walk(table_name_listener, ctx)
    tn = []
    for tns in table_name_listener.table_names:
        table_ref = tns.table_spec()
        if table_ref is None:
            continue
        tni = [None, None]
        if table_ref.schema_name():
            tni[0] = table_ref.schema_name().getText().replace('`', '')
        if table_ref.table_name():
            tni[1] = table_ref.table_name().getText().replace('`', '')
        tn.append(tni)

    return tn


class QueryListener(MySQLParserListener):
    """
    Extract all select_expressions.

    """
    def __init__(self):
        self.select_expressions = []
        self.select_list = None
        self.keywords = []

    def enterSelect_statement(self, ctx):
        if ctx.UNION_SYM():
            self.keywords.append('union')

    def enterSelect_expression(self, ctx):
        # we need to keep track of unions as they act as subqueries
        self.select_expressions.append(ctx)

    def enterSelect_list(self, ctx):
        if not self.select_list:
            self.select_list = ctx


class RemoveSubqueriesListener(MySQLParserListener):
    """
    Remove nested select_expressions.

    """
    def __init__(self, depth):
        self.depth = depth
        self.subquery_aliases = []
        #  self.walker = antlr4.ParseTreeWalker()
        #  self.table_name_listener = TableNameListener()

    def enterSelect_expression(self, ctx):
        parent = ctx.parentCtx.parentCtx

        if isinstance(parent, MySQLParser.SubqueryContext) and ctx.depth() >\
                self.depth:
            try:
                alias = parent.parentCtx.alias()
            except AttributeError:
                alias = None

            # subquery alias
            alias = parse_alias(alias)
            self.subquery_aliases.append(alias)
            ctx.parentCtx.removeLastChild()


class ColumnNameListener(MySQLParserListener):
    """
    Get all column names.

    """
    def __init__(self):
        self.column_name = []

    def enterColumn_spec(self, ctx):
        #  self.column_name.append(ctx.getText())
        self.column_name.append(ctx)


class TableNameListener(MySQLParserListener):
    """
    Get table names.

    """
    def __init__(self):
        self.table_names = []

    def enterTable_atom(self, ctx):
        #  self.column_name.append(ctx.getText())
        self.table_names.append(ctx)


class ColumnKeywordFunctionListener(MySQLParserListener):
    """
    Extract columns, keywords and functions.

    """
    def __init__(self):
        self.tables = []
        self.columns = []
        self.column_aliases = []
        self.keywords = []
        self.functions = []
        self.column_name_listener = ColumnNameListener()
        self.table_name_listener = TableNameListener()
        self.walker = antlr4.ParseTreeWalker()

    def _process_alias(self, ctx):
        try:
            alias = ctx.alias()
        except AttributeError:
            alias = None
        alias = parse_alias(alias)
        return alias

    def _extract_column(self, ctx, append=True):
        cn = process_column_name(self.column_name_listener, self.walker,
                                 ctx)
        alias = self._process_alias(ctx)
        if len(cn) > 1:
            columns = [[i, None] for i in cn]
        else:
            columns = [[cn[0], alias]]

        if not append:
            return alias, columns

        if alias is not None:
            self.column_aliases.append(alias)

        if cn[0] not in self.column_aliases:
            self.columns.extend(columns)

    def enterTable_atom(self, ctx):
        alias = parse_alias(ctx.alias())
        ts = ctx.table_spec()
        if ts:
            tn = [None, None]
            if ts.schema_name():
                tn[0] = ts.schema_name().getText().replace('`', '')
            if ts.table_name():
                tn[1] = ts.table_name().getText().replace('`', '')
            self.tables.append((alias, tn))

    def enterDisplayed_column(self, ctx):
        self._extract_column(ctx)
        if ctx.ASTERISK():
            self.keywords.append('*')

    def enterSelect_list(self, ctx):
        if ctx.ASTERISK():
            self.columns.append(('*', None))
            self.keywords.append('*')

    def enterFunctionList(self, ctx):
        self.functions.append(ctx.getText())

    def enterGroup_functions(self, ctx):
        self.functions.append(ctx.getText())

    def enterGroupby_clause(self, ctx):
        self.keywords.append('group by')
        col = self._extract_column(ctx, append=False)
        if col[1][0][0][2] not in self.column_aliases:
            self._extract_column(ctx)

    def enterWhere_clause(self, ctx):
        self.keywords.append('where')
        self._extract_column(ctx)

    def enterOrderby_clause(self, ctx):
        self.keywords.append('order by')
        col = self._extract_column(ctx, append=False)
        if col[1][0][0][2] not in self.column_aliases:
            self._extract_column(ctx)

    def enterLimit_clause(self, ctx):
        self.keywords.append('limit')

    def enterJoin_condition(self, ctx):
        self.keywords.append('join')
        self._extract_column(ctx)

class SyntaxErrorListener(ErrorListener):
    def __init__(self):
        super(SyntaxErrorListener, self).__init__()
        self.syntax_errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.syntax_errors.append((line, column, offendingSymbol.text))


class MySQLQueryProcessor(object):
    """
    Object used for processing MySQL queries. Its objective is query validation
    (syntax error detection )and extraction of used columns, keywords and
    functions.

    :param query:
        MySQL query string.

    """
    def __init__(self, query=None):
        self.walker = antlr4.ParseTreeWalker()

        self.columns = set()
        self.keywords = set()
        self.functions = set()
        self.display_columns = []
        self.syntax_error_listener = SyntaxErrorListener()
        self.syntax_errors = []
        if query is not None:
            self._query = query.rstrip(';') + ';'
            self.process_query()

    def extract_columns(self, subquery_aliases, query_names):
        sub_dct = {}
        columns = []

        
        for suba, qn in zip(subquery_aliases[::-1], query_names[::-1]):
            sub_columns = []
            tab_dct = dict(qn[0])

            # Replace the subquery aliases
            for col in qn[1]:
                if col[0] == '*':
                    col = [[None, None, '*'], col[1]]

                if not None in col[0]:
                    sub_columns.append(col)

                elif col[0][0] is None and col[0][1] is None and col[0][2] is None:
                        pass

                elif col[0][1] is not None:
                    try:
                        val = tab_dct[col[0][1]]
                        col[0][0] = val[0]
                        col[0][1] = val[1]
                        sub_columns.append(col)
                    except KeyError:
                        if col[0][0] is None:
                            for tab in qn[0]:
                                if col[0][1] == tab[1][1]:
                                    sub_columns.append([[tab[1][0], col[0][1],
                                             col[0][2]], col[1]])
                        else:
                            sub_columns.append(col)

                elif col[0][1] is None and col[0][0] is None:
                    for tab in qn[0]:
                        sub_columns.append([[tab[1][0], tab[1][1], col[0][2]],
                                             col[1]])

            if suba is not None:
                sub_dct[suba] = sub_columns

            columns.extend(sub_columns)

        return columns, sub_dct

    def process_query(self):
        """
        Parses and processes the query. After a successful run it fills up
        columns, keywords, functions and syntax_errors lists.

        """
        inpt = antlr4.InputStream(self.query)
        lexer = MySQLLexer(inpt)
        stream = antlr4.CommonTokenStream(lexer)
        parser = MySQLParser(stream)
        parser._listeners = [self.syntax_error_listener]

        # Parse the query
        tree = parser.query()

        query_listener = QueryListener()
        subquery_aliases = [None]
        query_names = []
        keywords = []
        functions = []

        self.walker.walk(query_listener, tree)
        keywords.extend(query_listener.keywords)

        for ctx in query_listener.select_expressions:
            remove_subquieries_listener = RemoveSubqueriesListener(ctx.depth())
            column_keyword_function_listener = ColumnKeywordFunctionListener()

            # Remove nested subqueries from select_expressions
            self.walker.walk(remove_subquieries_listener, ctx)
            subquery_aliases.extend(remove_subquieries_listener.subquery_aliases)
            
            # Extract table and column names and keywords
            self.walker.walk(column_keyword_function_listener, ctx)

            query_names.append([column_keyword_function_listener.tables,
                                column_keyword_function_listener.columns])
            keywords.extend(column_keyword_function_listener.keywords)
            functions.extend(column_keyword_function_listener.functions)

        column_keyword_function_listener = ColumnKeywordFunctionListener()
        self.walker.walk(column_keyword_function_listener,
                         query_listener.select_list)
        display_columns = column_keyword_function_listener.columns

        # Unions are have independent select queries but are not counted in
        # the subqueries
        diff = len(query_listener.select_expressions) - len(subquery_aliases)
        if diff > 0:
            subquery_aliases.extend([None] * diff)

        # If we only got table name without any database specification, we
        # raise an error.
        for table in [i[0] for i in query_names][0]:
            assert table[1][0] is not None, "Missing database specification."
            assert table[1][1] is not None, "Missing table specification."

        columns, sub_dct = self.extract_columns(subquery_aliases, query_names)
        touched_columns = [] 
        for col in columns:
            if col[0][0] is not None:
                touched_columns.append(tuple(col[0]))

        touched_columns = sorted(list(set(touched_columns)))

        columns, _ = self.extract_columns([None], [[query_names[0][0],
                                                    display_columns]])

        for k in range(max(1, len(subquery_aliases) - 1)):
            display_columns = [] 
            for col in columns:
                alias = col[1]
                if col[0][0] is not None:
                    if alias is None:
                        alias = col[0][2] 
                    display_columns.append((tuple(col[0]), alias))
                else:
                    
                    try:
                        sd = sub_dct[col[0][1]]
                    except KeyError:
                        raise QueryError('Invalid database specification `%s`.'
                                % col[0][1])
                    found_among_aliases = False
                    for c in sd:
                        if col[0][2] == c[1]:
                            if alias is None:
                                alias = col[0][2] 
                            display_columns.append((tuple(col[0]), alias))
                            found_among_aliases = True
                    if not found_among_aliases:
                        for c in sd:
                            if col[0][2] == c[0][2]:
                                if alias is None:
                                    alias = c[0][2] 
                                display_columns.append((tuple(c[0]), alias))

            columns = display_columns

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

        if not len(self.syntax_error_listener.syntax_errors):
            self.columns = list(set(touched_columns).difference(del_columns))
            self.keywords = list(set(keywords))
            self.functions = list(set(functions))
            self.display_columns = [(i[1], i[0]) for i in display_columns]
        else:
            self.syntax_errors = self.syntax_error_listener.syntax_errors

    @property
    def query(self):
        """
        Get the query string.

        """
        return self._query

    def set_query(self, query):
        """
        Helper to set the query string.

        """
        self.columns = set()
        self.keywords = set()
        self.functions = set()
        self.display_columns = []
        self.syntax_errors = []
        self._query = query.rstrip(';') + ';'
