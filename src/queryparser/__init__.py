class QueryError(Exception):
    def __init__(self, message=''):
        super(QueryError, self).__init__(message)
        self.message = message
