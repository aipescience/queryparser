import unittest

from queryparser.mysql import MySQLQueryProcessor
from queryparser.adql import ADQLQueryTranslator


class TestCase(unittest.TestCase):

    def _test_mysql_parsing(self, query, columns=None, keywords=None,
                            functions=None, display_columns=None):
        qp = MySQLQueryProcessor()
        qp.set_query(query)
        qp.process_query()
            
        try:
            qp_columns = ['.'.join(i) for i in qp.columns]
            qp_display_columns = [(i[0], '.'.join(i[1])) for i in
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

    def _test_adql_translation(self, query, translated_query=None,
                               syntax_errors=None):
        adt = ADQLQueryTranslator()
        adt.set_query(query)

        if translated_query:
            self.assertEqual(translated_query, adt.to_mysql())

        if syntax_errors:
            self.assertEqual(syntax_errors,
                             adt.syntax_error_listener.syntax_errors)
