import unittest

from queryparser.mysql import MySQLQueryProcessor
from queryparser.adql import ADQLQueryTranslator


class TestCase(unittest.TestCase):

    def _test_mysql_parsing(self, query, columns=None, keywords=None,
                            functions=None, display_columns=None):
        qp = MySQLQueryProcessor(query)

        qp_columns = ['.'.join([str(j) for j in i]) for i in qp.columns
                      if i[0] is not None and i[1] is not None]
        qp_display_columns = ['%s: %s' % (str(i[0]),
                                          '.'.join([str(j) for j in i[1]]))
                              for i in qp.display_columns]

        if columns:
            self.assertSetEqual(set(columns), set(qp_columns))

        if keywords:
            self.assertSetEqual(set(keywords), set(qp.keywords))

        if functions:
            self.assertSetEqual(set(functions), set(qp.functions))

        if display_columns:
            self.assertSetEqual(set(display_columns), set(qp_display_columns))

    def _test_adql_mysql_translation(self, query, adql_query=None):
        adt = ADQLQueryTranslator(query)

        if adql_query:
            self.assertEqual(adql_query.strip(), adt.to_mysql())

    def _test_adql_mysql_translation_parsing(self, query, columns=None,
                                             keywords=None, functions=None,
                                             display_columns=None):
        adt = ADQLQueryTranslator()
        qp = MySQLQueryProcessor()

        adt.set_query(query)

        qp.set_query(adt.to_mysql())
        qp.process_query()

        qp_columns = ['.'.join([str(j) for j in i]) for i in qp.columns
                      if i[0] is not None and i[1] is not None]
        qp_display_columns = ['%s: %s' % (str(i[0]),
                                          '.'.join([str(j) for j in i[1]]))
                              for i in qp.display_columns]

        if columns:
            self.assertSetEqual(set(columns), set(qp_columns))

        if keywords:
            self.assertSetEqual(set(keywords), set(qp.keywords))

        if functions:
            self.assertSetEqual(set(functions), set(qp.functions))

        if display_columns:
            self.assertSetEqual(set(display_columns), set(qp_display_columns))
