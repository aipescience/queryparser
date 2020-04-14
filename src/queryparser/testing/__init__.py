# -*- coding: utf-8 -*-

import unittest

from queryparser.mysql import MySQLQueryProcessor
from queryparser.postgresql import PostgreSQLQueryProcessor
from queryparser.adql import ADQLQueryTranslator


class TestCase(unittest.TestCase):

    def _test_mysql_parsing(self, query, columns=None, keywords=None,
                            functions=None, display_columns=None, tables=None,
                            replace_schema_name=None):

        if replace_schema_name is None:
            qp = MySQLQueryProcessor(query)
        else:
            qp = MySQLQueryProcessor()
            qp.set_query(query)
            qp.process_query(replace_schema_name=replace_schema_name)

        qp_columns = ['.'.join([str(j) for j in i]) for i in qp.columns
                      if i[0] is not None and i[1] is not None]
        qp_display_columns = ['%s: %s' % (str(i[0]),
                                          '.'.join([str(j) for j in i[1]]))
                              for i in qp.display_columns]
        qp_tables = ['.'.join([str(j) for j in i]) for i in qp.tables
                      if i[0] is not None and i[1] is not None]

        if columns:
            self.assertSetEqual(set(columns), set(qp_columns))

        if keywords:
            self.assertSetEqual(set(keywords), set(qp.keywords))

        if functions:
            self.assertSetEqual(set(functions), set(qp.functions))

        if display_columns:
            self.assertSetEqual(set(display_columns), set(qp_display_columns))

        if tables:
            self.assertSetEqual(set(tables), set(qp_tables))

    def _test_postgresql_parsing(self, query, columns=None, keywords=None,
                            functions=None, display_columns=None, tables=None,
                            replace_schema_name=None):
        qp = PostgreSQLQueryProcessor(query)
        qp.process_query()

        qp_columns = ['.'.join([str(j) for j in i[:3]]) for i in qp.columns
                      if i[0] is not None and i[1] is not None]
        qp_display_columns = ['%s: %s' % (str(i[0]),
                                          '.'.join([str(j) for j in i[1]]))
                              for i in qp.display_columns]
        qp_tables = ['.'.join([str(j) for j in i]) for i in qp.tables
                      if i[0] is not None and i[1] is not None]

        if columns:
            self.assertSetEqual(set(columns), set(qp_columns))

        if keywords:
            self.assertSetEqual(set(keywords), set(qp.keywords))

        if functions:
            self.assertSetEqual(set(functions), set(qp.functions))

        if display_columns:
            self.assertSetEqual(set(display_columns), set(qp_display_columns))

        if tables:
            self.assertSetEqual(set(tables), set(qp_tables))

    def _test_adql_mysql_translation(self, query, adql_query=None):
        adt = ADQLQueryTranslator(query)

        if adql_query:
            self.assertEqual(adql_query.strip(), adt.to_mysql())

    def _test_adql_postgresql_translation(self, query, adql_query=None):
        adt = ADQLQueryTranslator(query)

        if adql_query:
            self.assertEqual(adql_query.strip(), adt.to_postgresql())

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

    def _test_adql_postgresql_translation_parsing(self, query, columns=None,
                                             keywords=None, functions=None,
                                             tables=None, display_columns=None,
                                             indexed_objects=None):
        adt = ADQLQueryTranslator()
        qp = PostgreSQLQueryProcessor()

        adt.set_query(query)

        qp.set_query(adt.to_postgresql())
        qp.process_query(indexed_objects=indexed_objects)

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

        if tables:
            self.assertSetEqual(set(tables), set(qp.tables))

        if display_columns:
            self.assertSetEqual(set(display_columns), set(qp_display_columns))
