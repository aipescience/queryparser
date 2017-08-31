import unittest

from queryparser.mysql import MySQLQueryProcessor
from queryparser.adql import ADQLQueryTranslator


class TestCase(unittest.TestCase):

    def _test_mysql_parsing(self, query, columns=None, keywords=None,
                            functions=None, display_columns=None):
        qp = MySQLQueryProcessor(query)

        qp_columns = ['.'.join(i) for i in qp.columns]
        qp_display_columns = ['%s: %s' % (i[0], '.'.join(i[1])) for i in
                              qp.display_columns]

        if columns:
            self.assertSetEqual(set(columns), set(qp_columns))

        if keywords:
            self.assertSetEqual(set(keywords), set(qp.keywords))

        if functions:
            self.assertSetEqual(set(functions), set(qp.functions))

        if display_columns:
            self.assertSetEqual(set(display_columns), set(qp_display_columns))

<<<<<<< HEAD
    def _test_adql_mysql_translation(self, query, adql_query=None):
=======
    def _test_adql_mysql_translation(self, query, adql_query=None,
                               syntax_errors=None):
>>>>>>> 8f342a505271bdeed9de99b1fb9d901d7c471f9e
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

        try:
            qp_columns = ['.'.join(i) for i in qp.columns]
            qp_display_columns = ['%s: %s' % (i[0], '.'.join(i[1])) for i in
                                  qp.display_columns]
        except TypeError:
            pass

        if columns:
            self.assertSetEqual(set(columns), set(qp_columns))

        if keywords:
            self.assertSetEqual(set(keywords), set(qp.keywords))

        if functions:
            self.assertSetEqual(set(functions), set(qp.functions))

        if display_columns:
            self.assertSetEqual(set(display_columns), set(qp_display_columns))
