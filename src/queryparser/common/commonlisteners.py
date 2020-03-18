# -*- coding: utf-8 -*-
# All listeners that are with minor modifications shared between PostgreSQL
# and MySQL.
from __future__ import (absolute_import, print_function)

import re

from antlr4.error.ErrorListener import ErrorListener


def parse_alias(alias, quote_char):
    """
    Extract the alias if available.

    :param alias:
        antlr context.

    :parma quote_char:
        which quotation character to use

    """
    if alias:
        alias = alias.ID().getText().strip(quote_char)
    else:
        alias = None
    return alias


def process_column_name(column_name_listener, walker, ctx, quote_char):
    '''
    cn[0] - schema
    cn[1] - table
    cn[2] - column
    cn[3] - ctx
    cn[4] - column was selected, not yet implemented
    '''
    cn = []
    column_name_listener.column_name = []
    walker.walk(column_name_listener, ctx)
    if column_name_listener.column_name:
        for i in column_name_listener.column_name:
            cni = [None, None, None, i]
            if i.schema_name():
                cni[0] = i.schema_name().getText().replace(quote_char, '')
            if i.table_name():
                cni[1] = i.table_name().getText().replace(quote_char, '')
            if i.column_name():
                cni[2] = i.column_name().getText().replace(quote_char, '')
            cn.append(cni)
    else:
        try:
            ctx.ASTERISK()
            ts = ctx.table_spec()
            cn = [[None, None, '*', None]]
            if ts.schema_name():
                cn[0][0] = ts.schema_name().getText().replace(quote_char, '')
            if ts.table_name():
                cn[0][1] = ts.table_name().getText().replace(quote_char, '')
        except AttributeError:
            cn = [[None, None, None, None]]
    return cn


def get_column_name_listener(base):

    class ColumnNameListener(base):
        """
        Get all column names.

        """
        def __init__(self):
            self.column_name = []
            self.column_as_array = []

        def enterColumn_spec(self, ctx):
            try:
                if ctx.children[1].getText():
                    self.column_as_array.append(ctx)
                else:
                    self.column_as_array.append(None)
            except IndexError:
                self.column_as_array.append(None)
            self.column_name.append(ctx)

    return ColumnNameListener


def get_table_name_listener(base, quote_char):

    class TableNameListener(base):
        """
        Get table names.

        """
        def __init__(self):
            self.table_names = []
            self.table_aliases = []

        def enterTable_atom(self, ctx):
            self.table_names.append(ctx)

        def enterAlias(self, ctx):
            alias = parse_alias(ctx, quote_char)
            self.table_aliases.append(alias)

    return TableNameListener


def get_schema_name_listener(base, quote_char):

    class SchemaNameListener(base):

        def __init__(self, replace_schema_name):
            self.replace_schema_name = replace_schema_name

        def enterSchema_name(self, ctx):
            ttype = ctx.start.type
            sn = ctx.getTokens(ttype)[0].getSymbol().text
            try:
                nsn = self.replace_schema_name[sn.replace(quote_char, '')]
                try:
                    nsn = unicode(nsn, 'utf-8')
                except NameError:
                    pass
                nsn = re.sub('(|{})(?!{})[\S]*[^{}](|{})'.format(quote_char,
                    quote_char, quote_char, quote_char), r'\1{}\2'.format(nsn),
                    sn)
                ctx.getTokens(ttype)[0].getSymbol().text = nsn
            except KeyError:
                pass

    return SchemaNameListener


def get_remove_subqueries_listener(base, base_parser):

    class RemoveSubqueriesListener(base):
        """
        Remove nested select_expressions.

        """
        def __init__(self, depth):
            self.depth = depth

        def enterSelect_expression(self, ctx):
            parent = ctx.parentCtx.parentCtx

            if isinstance(parent, base_parser.SubqueryContext) and \
               ctx.depth() > self.depth:
                # we need to remove all Select_expression instances, not
                # just the last one so we loop over until we get all of them out
                seinstances = [isinstance(i,
                               base_parser.Select_expressionContext)
                               for i in ctx.parentCtx.children]
                while True in seinstances:
                    ctx.parentCtx.removeLastChild()
                    seinstances = [isinstance(i,
                                   base_parser.Select_expressionContext)
                                   for i in ctx.parentCtx.children]

    return RemoveSubqueriesListener


def get_query_listener(base, base_parser, quote_char):

    class QueryListener(base):
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
            if isinstance(parent, base_parser.SubqueryContext):
                try:
                    alias = parent.parentCtx.alias()
                    alias = parse_alias(alias, quote_char)
                    self.subquery_aliases[ctx] = alias
                except AttributeError:
                    pass

        def enterSelect_list(self, ctx):
            if not self.select_list:
                self.select_list = ctx

    return QueryListener


class SyntaxErrorListener(ErrorListener):
    def __init__(self):
        super(SyntaxErrorListener, self).__init__()
        self.syntax_errors = []

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        if offending_symbol is not None:
            self.syntax_errors.append((line, column, offending_symbol.text))
        else:
            self.syntax_errors.append((line, column, msg))
