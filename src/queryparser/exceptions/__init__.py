# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-


class QueryError(Exception):
    def __init__(self, messages=[]):
        self.messages = messages


class QuerySyntaxError(Exception):
    def __init__(self, syntax_errors=[]):
        self.syntax_errors = syntax_errors
