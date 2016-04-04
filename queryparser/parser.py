# -*- coding: utf-8 -*-

from visitor import Visitor
from mysql.mysqlparser import MySQLQueryProcessor

processor_types = {'mysql': MySQLQueryProcessor}

class QueryParser(object):
    def __init__(self, query=None, query_type=None):
        self._accepted_types = ('mysql',)

        if query is not None:
            assert isinstance(query, str), 'Query must be a string.'
            assert query_type in self._accepted_types,\
                'Please specifiy query type %s.' % str(self._accepted_types)

        self._query = query
        self._query_type = query_type
        self._syntax_errors = None
        self._visitors = []

    @property
    def query(self):
        """
        Get the query string.

        """
        return self._query

    def set_query(self, value, query_type):
        """
        Set the query string. Tree object is emptied so there is no
        mismatch between the query and the parsed tree.

        :param value:
            Query string.

        :param query_type:
            For now just mysql.

        """
        if query_type not in self._accepted_types:
            raise ValueError("Query type must be %s" %
                             str(self._accepted_types))

        self.reset()
        self._query = str(value)
        self._query_type = query_type

    def process(self):
        """
        If there are no registered visitors, raise an error.

        """
        if len(self._visitors) == 0:
            raise ValueError("There are no registered visitors to be "
                             "processed.")

        processor = processor_types[self._query_type](self._query)

        if processor.syntax_errors:
            print("Query has syntax errors.")
            self._syntax_errors = processor.syntax_errors
            return False

        self._passed = []
        for v in self._visitors:
            cs = set(processor.columns)
            ks = set(processor.keywords)
            status = []

            if not cs.issubset(v.columns):
                print("Visitor %s is not allowed to access columns %s." %
                      (v, str(tuple(cs.difference(v.columns)))))
                status.append(False)
            else:
                status.append(True)

            if not ks.issubset(v.keywords):
                print(("Visitor %s is not allowed to issue following " +
                       "statements: %s.") %
                      (v, str(tuple(ks.difference(v.keywords))).upper()))
                status.append(False)
            else:
                status.append(True)

            self._passed.append(status)

    def register(self, visitor):
        """
        Validate and register a visitor object. It must be inherited
        from the `Visitor` class.

        :param visitor:
            Visitor object inherited from ``Visitor`` class.

        """
        assert issubclass(visitor.__class__, Visitor),\
            "Visitor %s not an instance of Visitor class." % str(visitor)

        self._visitors.append(visitor)

    def reset(self):
        self._passed = []
        self._query = None
        self._query_type = None
        self._syntax_errors = None

    @property
    def syntax_errors(self):
        """
        Get syntax errors, if there are any.

        """
        return self._syntax_errors

    @property
    def visitors(self):
        return self._visitors

    @property
    def passed(self):
        return self._passed



if __name__ == '__main__':
    from test.test_queries import queries
    from test.broken_queries import queries as bqueries

    qi = 5

    v = Visitor()
    v.set_columns(queries[qi][1])
    v.set_keywords(queries[qi][2])
        
    qp = QueryParser(queries[qi][0], 'mysql')
    qp.register(v)
    qp.process()
    print(qp.passed)
