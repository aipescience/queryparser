import unittest

from queryparser.mysql import MySQLQueryProcessor
from queryparser.adql import ADQLQueryTranslator


class TestCase(unittest.TestCase):

    def _test_mysql_parsing(self, query, columns=None, keywords=None, functions=None, column_aliases=None):
        qp = MySQLQueryProcessor()
        qp.set_query(query)
        qp.process_query()

        if columns:
            self.assertSetEqual(set(columns), qp.columns)

        if keywords:
            self.assertSetEqual(set(keywords), qp.keywords)

        if functions:
            self.assertSetEqual(set(functions), qp.functions)

        if column_aliases:
            self.assertSetEqual(set(column_aliases), qp.column_aliases)

    def _test_adql_translation(self, query, translated_query=None, syntax_errors=None):
        adt = ADQLQueryTranslator()
        adt.set_query(query)

        if translated_query:
            self.assertEqual(translated_query, adt.to_mysql())

        if syntax_errors:
            self.assertEqual(syntax_errors, adt.syntax_error_listener.syntax_errors)
