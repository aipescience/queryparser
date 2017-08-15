# -*- coding: utf-8 -*-
"""
MySQL processor. Its task is to check if a query has any syntax errors and
to extract all accessed columns as well as keywords and functions being
used in a query.

"""

from __future__ import (absolute_import, print_function)

__all__ = ["MySQLQueryProcessor"]

import antlr4
from antlr4.error.ErrorListener import ErrorListener

from .MySQLLexer import MySQLLexer
from .MySQLParser import MySQLParser
from .MySQLParserListener import MySQLParserListener


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


class QueryListener(MySQLParserListener):
    """
    Extract all select_expressions.

    """
    def __init__(self):
        self.select_expressions = []
        self.keywords = []

    def enterSelect_statement(self, ctx):
        if ctx.UNION_SYM():
            self.keywords.append('union')

    def enterSelect_expression(self, ctx):
        self.select_expressions.append(ctx)


class RemoveSubqueriesListener(MySQLParserListener):
    """
    Remove nested select_expressions.

    """
    def __init__(self, depth):
        self.depth = depth
        self.subquery_aliases = {}

    def enterSelect_expression(self, ctx):
        parent = ctx.parentCtx.parentCtx
        if isinstance(parent, MySQLParser.SubqueryContext) and ctx.depth() >\
                self.depth:
            try:
                alias = parent.parentCtx.alias()
            except AttributeError:
                alias = None
            table_ref = ctx.table_references().getText()\
                .split('JOIN')[0].replace('`', '')
            alias = parse_alias(alias)
            self.subquery_aliases[alias] = table_ref
            ctx.parentCtx.removeLastChild()


class ColumnNameListener(MySQLParserListener):
    """
    Get all column names.

    """
    def __init__(self):
        self.column_name = []

    def enterColumn_spec(self, ctx):
        self.column_name.append(ctx.getText())


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
        self.walker = antlr4.ParseTreeWalker()

    def _process_column_name(self, ctx):
        cn = []
        self.column_name_listener.column_name = []
        self.walker.walk(self.column_name_listener, ctx)
        if self.column_name_listener.column_name:
            for i in self.column_name_listener.column_name:
                cn.append(i.replace('`', ''))
        else:
            try:
                if ctx.ASTERISK():
                    cn = [ctx.getText()]
                else:
                    cn = ['NULL']
            except AttributeError:
                cn = ['NULL']
        return cn

    def _process_alias(self, ctx):
        try:
            alias = ctx.alias()
        except AttributeError:
            alias = None
        alias = parse_alias(alias)
        return alias

    def _extract_column(self, ctx):
        cn = self._process_column_name(ctx)
        alias = self._process_alias(ctx)
        if alias is not None:
            self.column_aliases.append(alias)

        if cn[0] not in self.column_aliases:
            if len(cn) > 1:
                self.columns.extend([(i, None) for i in cn])
            else:
                self.columns.append((cn[0], alias))

    def enterTable_atom(self, ctx):
        alias = parse_alias(ctx.alias())
        ts = ctx.table_spec()
        if ts:
            self.tables.append((ts.getText().replace('`', ''), alias))

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
        self._extract_column(ctx)

    def enterWhere_clause(self, ctx):
        self.keywords.append('where')
        self._extract_column(ctx)

    def enterOrderby_clause(self, ctx):
        self.keywords.append('order by')
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
        self.column_aliases = {}
        self.syntax_error_listener = SyntaxErrorListener()
        self.syntax_errors = []
        if query is not None:
            self._query = query.rstrip(';') + ';'
            self.process_query()

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
        subquery_aliases = {}
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
            for als in remove_subquieries_listener.subquery_aliases.items():
                subquery_aliases[als[0]] = als[1]

            # Extract table and column names and keywords
            self.walker.walk(column_keyword_function_listener, ctx)

            query_names.append([column_keyword_function_listener.tables,
                                column_keyword_function_listener.columns])
            keywords.extend(column_keyword_function_listener.keywords)
            functions.extend(column_keyword_function_listener.functions)

        columns = []
        col_aliases = {}

        for qn in query_names:
            tab_dict = {}
            tab = []
            for i in qn[0]:
                if i[1]:
                    tab_dict[i[1]] = i[0]
                else:
                    tab.append(i[0])

            for i in qn[1]:
                parts = i[0].split('.')

                if len(parts) == 3:
                    columns.append(i[0])

                if len(parts) == 2 and parts[0] not in subquery_aliases:
                    # we need to replace the table name alias
                    try:
                        update = tab_dict[parts[0]]
                        cappend = '%s.%s' % (update, parts[1])
                        if i[0] != 'NULL' and i[1] is not None:
                            col_aliases[i[1]] = cappend
                        columns.append(cappend)
                    except KeyError:
                        pass

                elif len(parts) == 2 and parts[0] in subquery_aliases.keys():
                    try:
                        alias_key = i[0].split('.')
                        if i[0] != 'NULL' and i[1] is not None:
                            col_aliases[i[1]] = '.'.join(
                                (subquery_aliases[alias_key[0]], alias_key[1]))
                    except KeyError:
                        pass

                if len(parts) == 1:
                    if i[0] != 'NULL' and i[1] is not None:
                        col_aliases[i[1]] = i[0]
                    dvs = list(tab_dict.values())
                    if len(dvs) > 1 or len(tab) > 1:
                        for k in dvs:
                            columns.append('%s.%s' % (k, parts[0]))
                        for k in tab:
                            columns.append('%s.%s' % (k, parts[0]))

                    else:
                        if len(dvs):
                            columns.append('%s.%s' % (dvs[0], parts[0]))
                        elif len(tab):
                            columns.append('%s.%s' % (tab[0], parts[0]))

        # Let's get rid of all columns that are already covered by
        # db.tab.*. Figure out a better way to do it and replace the code
        # below.
        asterisk_columns = []
        del_columns = []
        for col in columns:
            if col.split('.')[-1] == '*':
                asterisk_columns.append(col)
        for acol in asterisk_columns:
            for col in columns:
                if acol != col and acol.split('.')[:-1] == col.split('.')[:-1]:
                    del_columns.append(col)

        if not len(self.syntax_error_listener.syntax_errors):
            self.columns = set(columns).difference(del_columns)
            self.keywords = set(keywords)
            self.functions = set(functions)
            self.column_aliases = col_aliases
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
        self.column_aliases = {}
        self.syntax_errors = []
        self._query = query.rstrip(';') + ';'
