# -*- coding: utf-8 -*-

from __future__ import (absolute_import, print_function)

import antlr4
import logging
import re

from .PostgreSQLParser import PostgreSQLParser
from .PostgreSQLParserListener import PostgreSQLParserListener

from ..common import parse_alias, process_column_name,\
        get_column_name_listener, get_table_name_listener,\
        get_column_keyword_function_listener


class PgSphereListener(PostgreSQLParserListener):

    def __init__(self, columns, indexed_objects=None):
        self.column_name_listener = get_column_name_listener(
                PostgreSQLParserListener)()
        self.walker = antlr4.ParseTreeWalker()

        self.cctx_dict = {}
        for c in columns:
            try:
                # PgSphere sphere stuff can't be in the USING statement
                self.cctx_dict[c[3]] = c[:3]
            except IndexError:  # TODO: check if this is the best way
                pass

        self.indexed_objects = indexed_objects
        self.replace_dict = {}

    def enterSpoint(self, ctx):
        try:
            spoint = self.indexed_objects['spoint']
        except KeyError:
            return

        cn = process_column_name(self.column_name_listener, self.walker, ctx,
                '"')
        cols = []

        for c in cn:
            try:
                cols.append(self.cctx_dict[c[3]])
            except KeyError:
                pass

        if len(cols):
            for sp in spoint:
                if sp[0] == cols[0] and sp[1] == cols[1]:
                    rt = ctx.start.getInputStream().getText(ctx.start.start,
                                                            ctx.stop.stop)
                    self.replace_dict[rt] = sp[2]
