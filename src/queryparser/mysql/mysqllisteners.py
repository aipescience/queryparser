# -*- coding: utf-8 -*-

from __future__ import (absolute_import, print_function)

import antlr4
import logging
import re

#from antlr4.error.ErrorListener import ErrorListener

from .MySQLParser import MySQLParser
from .MySQLParserListener import MySQLParserListener

from ..common import parse_alias, process_column_name, \
        get_column_name_listener, get_table_name_listener

#  logging.basicConfig(level=logging.INFO)



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
        self.column_name_listener = get_column_name_listener(MySQLParserListener)()
        self.table_name_listener = get_table_name_listener(MySQLParserListener, '`')()
        self.walker = antlr4.ParseTreeWalker()

        self.data = []

    def _process_alias(self, ctx):
        try:
            alias = ctx.alias()
        except AttributeError:
            alias = None
        alias = parse_alias(alias, '`')
        return alias

    def _extract_column(self, ctx, append=True, join_columns=False):
        cn = process_column_name(self.column_name_listener, self.walker,
                                 ctx, '`')
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
        alias = parse_alias(ctx.alias(), '`')
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

    def enterHaving_clause(self, ctx):
        self.keywords.append('having')
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


class SyntaxErrorListener(ErrorListener):
    def __init__(self):
        super(SyntaxErrorListener, self).__init__()
        self.syntax_errors = []

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        if offending_symbol is not None:
            self.syntax_errors.append((line, column, offending_symbol.text))
        else:
            self.syntax_errors.append((line, column, msg))
