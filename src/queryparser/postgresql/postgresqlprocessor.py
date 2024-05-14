# -*- coding: utf-8 -*-
"""
PostgreSQL processor. Its task is to check if a query has any syntax errors and
to extract all accessed columns as well as keywords and functions being
used in a query.

"""

from __future__ import (absolute_import, print_function)

__all__ = ["PostgreSQLQueryProcessor"]

from .PostgreSQLLexer import PostgreSQLLexer
from .PostgreSQLParser import PostgreSQLParser
from .PostgreSQLParserListener import PostgreSQLParserListener

from ..common import SQLQueryProcessor


class PostgreSQLQueryProcessor(SQLQueryProcessor):
    def __init__(self, query=None):
        super().__init__(PostgreSQLLexer, PostgreSQLParser,
                         PostgreSQLParserListener, '"', query)
