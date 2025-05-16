# -*- coding: utf-8 -*-

from queryparser.adql import ADQLQueryTranslator
from queryparser.mysql import MySQLQueryProcessor
from queryparser.postgresql import PostgreSQLQueryProcessor


def _test_parsing(query_processor, test, translate=False):
    if len(test) == 7:
        (
            query,
            columns,
            keywords,
            functions,
            display_columns,
            tables,
            replace_function_names,
        ) = test
        replace_schema_name = None
    elif len(test) == 8:
        (
            query,
            columns,
            keywords,
            functions,
            display_columns,
            tables,
            replace_schema_name,
            replace_function_names,
        ) = test

    if translate:
        adt = ADQLQueryTranslator()
        adt.set_query(query)
        if query_processor == MySQLQueryProcessor:
            query = adt.to_mysql()
        elif query_processor == PostgreSQLQueryProcessor:
            query = adt.to_postgresql()

    if replace_function_names is None:
        replace_function_names = []

    qp = query_processor()
    qp.set_query(query)
    qp.process_query(
        replace_schema_name=replace_schema_name,
        replace_function_names=replace_function_names,
    )

    qp_columns = [
        '.'.join([str(j) for j in i[:3]])
        for i in qp.columns
        if i[0] is not None and i[1] is not None
    ]
    qp_display_columns = [
        '%s: %s' % (str(i[0]), '.'.join([str(j) for j in i[1]]))
        for i in qp.display_columns
    ]
    qp_tables = [
        '.'.join([str(j) for j in i])
        for i in qp.tables
        if i[0] is not None and i[1] is not None
    ]

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
