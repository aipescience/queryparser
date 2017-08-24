__title__ = 'queryparser'
__version__ = '0.1.3'
__author__ = 'Gal Matijevic'
__email__ = 'gmatijevic@aip.de'
__license__ = 'Apache-2.0'
__copyright__ = 'Copyright 2017 Leibniz Institute for Astrophysics Potsdam (AIP)'

VERSION = __version__


class QueryError(Exception):
    def __init__(self, message=''):
        super(QueryError, self).__init__(message)
        self.message = message
