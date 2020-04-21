# -*- coding: utf-8 -*-

import pytest 

from queryparser.adql import ADQLQueryTranslator
from queryparser.exceptions import QueryError, QuerySyntaxError

from queryparser.mysql import MySQLQueryProcessor
from queryparser.postgresql import PostgreSQLQueryProcessor
# from queryparser.adql import ADQLQueryTranslator


def _test_parsing(query_processor, test, translate=False):
    query, columns, keywords, functions, display_columns, tables,\
            replace_schema_name = test

    if translate:
        adt = ADQLQueryTranslator()
        adt.set_query(query)
        if query_processor == MySQLQueryProcessor:
            query = adt.to_mysql()

    if replace_schema_name is None:
        qp = query_processor(query)
    else:
        qp = query_processor()
        qp.set_query(query)
        qp.process_query(replace_schema_name=replace_schema_name)

    qp_columns = ['.'.join([str(j) for j in i[:3]]) for i in qp.columns
                  if i[0] is not None and i[1] is not None]
    qp_display_columns = ['%s: %s' % (str(i[0]),
                                      '.'.join([str(j) for j in i[1]]))
                          for i in qp.display_columns]
    qp_tables = ['.'.join([str(j) for j in i]) for i in qp.tables
                  if i[0] is not None and i[1] is not None]

    if columns is not None:
        assert set(columns) == set(qp_columns)

    if keywords is not None:
        assert set([i.lower() for i in keywords]) == set(qp.keywords)

    if functions is not None:
        assert set(functions) == set(qp.functions)

    if display_columns is not None:
        assert set(display_columns) == set(qp_display_columns)

    if tables is not None:
        assert set(tables) == set(qp_tables)


def _test_syntax(query_processor, query):
    with pytest.raises(QuerySyntaxError):
        qp = query_processor(query)
        qp.process_query()


def _test_query(query_processor, query):
    with pytest.raises(QueryError):
        qp = query_processor(query)
        qp.process_query()


def _test_adql_translation(test):
    query, translated_query, output = test
    adt = ADQLQueryTranslator(query)

    if translated_query is not None:
        if output == 'mysql':
            assert translated_query.strip() == adt.to_mysql()
        elif output == 'postgresql':
            assert translated_query.strip() == adt.to_postgresql()
    

# class TestCase(unittest.TestCase):
    # pass

    # def _test_mysql_parsing(self, query, columns=None, keywords=None,
                            # functions=None, display_columns=None, tables=None,
                            # replace_schema_name=None):

        # if replace_schema_name is None:
            # qp = MySQLQueryProcessor(query)
        # else:
            # qp = MySQLQueryProcessor()
            # qp.set_query(query)
            # qp.process_query(replace_schema_name=replace_schema_name)

        # qp_columns = ['.'.join([str(j) for j in i[:3]]) for i in qp.columns
                      # if i[0] is not None and i[1] is not None]
        # qp_display_columns = ['%s: %s' % (str(i[0]),
                                          # '.'.join([str(j) for j in i[1]]))
                              # for i in qp.display_columns]
        # qp_tables = ['.'.join([str(j) for j in i]) for i in qp.tables
                      # if i[0] is not None and i[1] is not None]

        # if columns:
            # self.assertSetEqual(set(columns), set(qp_columns))

        # if keywords:
            # self.assertSetEqual(set(keywords), set(qp.keywords))

        # if functions:
            # self.assertSetEqual(set(functions), set(qp.functions))

        # if display_columns:
            # self.assertSetEqual(set(display_columns), set(qp_display_columns))

        # if tables:
            # self.assertSetEqual(set(tables), set(qp_tables))

    # def _test_postgresql_parsing(self, query, columns=None, keywords=None,
                            # functions=None, display_columns=None, tables=None,
                            # replace_schema_name=None):
        # qp = PostgreSQLQueryProcessor(query)
        # qp.process_query()

        # qp_columns = ['.'.join([str(j) for j in i[:3]]) for i in qp.columns
                      # if i[0] is not None and i[1] is not None]
        # qp_display_columns = ['%s: %s' % (str(i[0]),
                                          # '.'.join([str(j) for j in i[1]]))
                              # for i in qp.display_columns]
        # qp_tables = ['.'.join([str(j) for j in i]) for i in qp.tables
                      # if i[0] is not None and i[1] is not None]

        # if columns:
            # self.assertSetEqual(set(columns), set(qp_columns))

        # if keywords:
            # self.assertSetEqual(set(keywords), set(qp.keywords))

        # if functions:
            # self.assertSetEqual(set(functions), set(qp.functions))

        # if display_columns:
            # self.assertSetEqual(set(display_columns), set(qp_display_columns))

        # if tables:
            # self.assertSetEqual(set(tables), set(qp_tables))

    # def _test_adql_mysql_translation(self, query, adql_query=None):
        # adt = ADQLQueryTranslator(query)

        # if adql_query:
            # self.assertEqual(adql_query.strip(), adt.to_mysql())

    # def _test_adql_postgresql_translation(self, query, adql_query=None):
        # adt = ADQLQueryTranslator(query)

        # if adql_query:
            # self.assertEqual(adql_query.strip(), adt.to_postgresql())

    # def _test_adql_mysql_translation_parsing(self, query, columns=None,
                                             # keywords=None, functions=None,
                                             # display_columns=None):
        # adt = ADQLQueryTranslator()
        # qp = MySQLQueryProcessor()

        # adt.set_query(query)

        # qp.set_query(adt.to_mysql())
        # qp.process_query()

        # qp_columns = ['.'.join([str(j) for j in i]) for i in qp.columns
                      # if i[0] is not None and i[1] is not None]
        # qp_display_columns = ['%s: %s' % (str(i[0]),
                                          # '.'.join([str(j) for j in i[1]]))
                              # for i in qp.display_columns]

        # if columns:
            # self.assertSetEqual(set(columns), set(qp_columns))

        # if keywords:
            # self.assertSetEqual(set(keywords), set(qp.keywords))

        # if functions:
            # self.assertSetEqual(set(functions), set(qp.functions))

        # if display_columns:
            # self.assertSetEqual(set(display_columns), set(qp_display_columns))

    # def _test_adql_postgresql_translation_parsing(self, query, columns=None,
                                             # keywords=None, functions=None,
                                             # tables=None, display_columns=None,
                                             # indexed_objects=None):
        # adt = ADQLQueryTranslator()
        # qp = PostgreSQLQueryProcessor()

        # adt.set_query(query)

        # qp.set_query(adt.to_postgresql())
        # qp.process_query(indexed_objects=indexed_objects)

        # qp_columns = ['.'.join([str(j) for j in i]) for i in qp.columns
                      # if i[0] is not None and i[1] is not None]
        # qp_display_columns = ['%s: %s' % (str(i[0]),
                                          # '.'.join([str(j) for j in i[1]]))
                              # for i in qp.display_columns]

        # if columns:
            # self.assertSetEqual(set(columns), set(qp_columns))

        # if keywords:
            # self.assertSetEqual(set(keywords), set(qp.keywords))

        # if functions:
            # self.assertSetEqual(set(functions), set(qp.functions))

        # if tables:
            # self.assertSetEqual(set(tables), set(qp.tables))

        # if display_columns:
            # self.assertSetEqual(set(display_columns), set(qp_display_columns))
