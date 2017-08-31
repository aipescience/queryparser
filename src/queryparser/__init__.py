class QueryError(Exception):
    def __init__(self, message=''):
        self.message = message

class QuerySyntaxError(Exception):
    def __init__(self, syntax_errors=[]):
        self.syntax_errors = syntax_errors
