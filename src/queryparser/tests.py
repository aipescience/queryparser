
from queryparser import MySQLQueryProcessor
from queryparser import ADQLQueryTranslator

from queryparser.examples import test_queries
from queryparser.examples import broken_queries
from queryparser.examples import adql_queries


class Tests:

    def test_mysql_basic(self):
        q = "SELECT a FROM tab;"
        qp = MySQLQueryProcessor(q)

    def test_mysql_example_queries(self):
        qp = MySQLQueryProcessor()

        for q in test_queries.queries:
            qp.set_query(q[0])
            qp.process_query()
        for q in broken_queries.queries:
            qp.set_query(q[0])
            qp.process_query()

    def test_adql_basic(self):
        q = "SELECT a FROM tab"
        adt = ADQLQueryTranslator(q)

    def test_adql_example_queries(self):
        adt = ADQLQueryTranslator()

        for q in adql_queries.queries:
            adt.set_query(q)
            translated_query = adt.to_mysql()

    def test_adql_syntax_error(self):
        q = "SELETC blablabla"
        adt = ADQLQueryTranslator()
        try:
            adt.set_query(q)
            translated_query = adt.to_mysql()
        except RuntimeError:
            pass

    def test_adql_polygon(self):
       q = """SELECT POLYGON('ICRS', 10, -10.5, 20, 20.6, 30, 30.7) FROM b"""
       adt = ADQLQueryTranslator(q)
       try:
           adt.to_mysql()
       except AttributeError:
           pass
