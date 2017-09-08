# -*- coding: utf-8 -*-

from __future__ import (absolute_import, print_function)

import antlr4
import logging
import re

from antlr4.error.ErrorListener import ErrorListener

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


class ColumnNameListener(MySQLParserListener):
    """
    Get all column names.

    """
    def __init__(self):
        self.column_name = []

    def enterColumn_spec(self, ctx):
        self.column_name.append(ctx)


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

        self.data = []

    def _process_alias(self, ctx):
        try:
            alias = ctx.alias()
        except AttributeError:
            alias = None
        alias = parse_alias(alias)
        return alias

    def _extract_column(self, ctx, append=True, join_columns=False):
        cn = process_column_name(self.column_name_listener, self.walker,
                                 ctx)
        alias = self._process_alias(ctx)

        if len(cn) > 1:
            if join_columns:
                columns = [[i, None, join_columns] for i in cn]
            else:
                columns = [[i, None] for i in cn]

        else:
            if join_columns:
                columns = [[cn[0], alias, join_columns]]
            else:
                columns = [[cn[0], alias]]

        if not append:
            return alias, columns

        if alias is not None:
            self.column_aliases.append(alias)

        if cn[0] not in self.column_aliases:
            self.columns.extend(columns)

    def enterTable_references(self, ctx):
        self.walker.walk(self.table_name_listener, ctx)
        tas = self.table_name_listener.table_aliases
        if len(tas):
            logging.info((ctx.depth(), ctx.__class__.__name__, tas))
            self.data.append([ctx.depth(), ctx, tas])
        else:
            logging.info((ctx.depth(), ctx.__class__.__name__))
            self.data.append([ctx.depth(), ctx])

    def enterTable_atom(self, ctx):
        alias = parse_alias(ctx.alias())
        ts = ctx.table_spec()
        if ts:
            tn = [None, None]
            if ts.schema_name():
                tn[0] = ts.schema_name().getText().replace('`', '')
            if ts.table_name():
                tn[1] = ts.table_name().getText().replace('`', '')
            self.tables.append((alias, tn, ctx.depth()))

            logging.info((ctx.depth(), ctx.__class__.__name__, [tn, alias]))
            self.data.append([ctx.depth(), ctx, [tn, alias]])

    def enterDisplayed_column(self, ctx):
        logging.info((ctx.depth(), ctx.__class__.__name__,
                     self._extract_column(ctx, append=False)[1]))
        self.data.append([ctx.depth(), ctx,
                          self._extract_column(ctx, append=False)[1]])
        self._extract_column(ctx)
        if ctx.ASTERISK():
            self.keywords.append('*')

    def enterSelect_expression(self, ctx):
        logging.info((ctx.depth(), ctx.__class__.__name__))
        self.data.append([ctx.depth(), ctx])

    def enterSelect_list(self, ctx):
        if ctx.ASTERISK():
            logging.info((ctx.depth(), ctx.__class__.__name__,
                         [[None, None, '*'], None]))
            self.data.append([ctx.depth(), ctx, [[[None, None, '*'], None]]])
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
        logging.info((ctx.depth(), ctx.__class__.__name__,
                     self._extract_column(ctx, append=False)[1]))
        self.data.append([ctx.depth(), ctx,
                          self._extract_column(ctx, append=False)[1]])

    def enterWhere_clause(self, ctx):
        self.keywords.append('where')
        self._extract_column(ctx)
        logging.info((ctx.depth(), ctx.__class__.__name__,
                     self._extract_column(ctx, append=False)[1]))
        self.data.append([ctx.depth(), ctx,
                          self._extract_column(ctx, append=False)[1]])

    def enterOrderby_clause(self, ctx):
        self.keywords.append('order by')
        col = self._extract_column(ctx, append=False)
        if col[1][0][0][2] not in self.column_aliases:
            self._extract_column(ctx)
        logging.info((ctx.depth(), ctx.__class__.__name__,
                     self._extract_column(ctx, append=False)[1]))
        self.data.append([ctx.depth(), ctx,
                          self._extract_column(ctx, append=False)[1]])

    def enterLimit_clause(self, ctx):
        self.keywords.append('limit')

    def enterJoin_condition(self, ctx):
        self.keywords.append('join')
        self._extract_column(ctx, join_columns=ctx)
        logging.info((ctx.depth(), ctx.__class__.__name__,
                     self._extract_column(ctx, append=False)[1]))
        self.data.append([ctx.depth(), ctx,
                          self._extract_column(ctx, append=False)[1]])


class QueryListener(MySQLParserListener):
    """
    Extract all select_expressions.

    """
    def __init__(self):
        self.select_expressions = []
        self.select_list = None
        self.keywords = []
        self.subquery_aliases = {}

    def enterSelect_statement(self, ctx):
        if ctx.UNION_SYM():
            self.keywords.append('union')

    def enterSelect_expression(self, ctx):
        # we need to keep track of unions as they act as subqueries
        self.select_expressions.append(ctx)

        parent = ctx.parentCtx.parentCtx
        if isinstance(parent, MySQLParser.SubqueryContext):
            try:
                alias = parent.parentCtx.alias()
                alias = parse_alias(alias)
                self.subquery_aliases[ctx] = alias
            except AttributeError:
                pass

    def enterSelect_list(self, ctx):
        if not self.select_list:
            self.select_list = ctx


class RemoveSubqueriesListener(MySQLParserListener):
    """
    Remove nested select_expressions.

    """
    def __init__(self, depth):
        self.depth = depth
        #  self.subquery_aliases = []

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
            #  self.subquery_aliases.append([alias, ctx.depth()])
            ctx.parentCtx.removeLastChild()


class SchemaNameListener(MySQLParserListener):

    def __init__(self, replace_schema_name):
        self.replace_schema_name = replace_schema_name

    def enterSchema_name(self, ctx):
        ttype = ctx.start.type
        sn = ctx.getTokens(ttype)[0].getSymbol().text
        try:
            nsn = self.replace_schema_name[sn.replace('`', '')]
            try:
                nsn = unicode(nsn, 'utf-8')
            except NameError:
                pass
            nsn = re.sub('(|`)(?!`)[\S]*[^`](|`)', r'\1%s\2' % nsn, sn)
            ctx.getTokens(ttype)[0].getSymbol().text = nsn
        except KeyError:
            pass


class SyntaxErrorListener(ErrorListener):
    def __init__(self):
        super(SyntaxErrorListener, self).__init__()
        self.syntax_errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.syntax_errors.append((line, column, offendingSymbol.text))


class TableNameListener(MySQLParserListener):
    """
    Get table names.

    """
    def __init__(self):
        self.table_names = []
        self.table_aliases = []

    def enterTable_atom(self, ctx):
        self.table_names.append(ctx)

    def enterAlias(self, ctx):
        alias = parse_alias(ctx)
        self.table_aliases.append(alias)
