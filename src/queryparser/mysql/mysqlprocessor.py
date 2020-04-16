# -*- coding: utf-8 -*-
"""
MySQL processor. Its task is to check if a query has any syntax errors and
to extract all accessed columns as well as keywords and functions being
used in a query.

"""

from __future__ import (absolute_import, print_function)

__all__ = ["MySQLQueryProcessor"]

from .MySQLLexer import MySQLLexer
from .MySQLParser import MySQLParser
from .MySQLParserListener import MySQLParserListener

from ..common import SQLQueryProcessor


class MySQLQueryProcessor(SQLQueryProcessor):
    def __init__(self, query=None):
        super().__init__(MySQLLexer, MySQLParser, MySQLParserListener, '`',
                         query)
