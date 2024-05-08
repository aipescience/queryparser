# -*- coding: utf-8 -*-

from queryparser.exceptions import QuerySyntaxError
from .utils import _test_parsing

from queryparser.adql import ADQLQueryTranslator
from queryparser.mysql import MySQLQueryProcessor
from queryparser.postgresql import PostgreSQLQueryProcessor

import os
import pytest
import yaml

with open(os.path.dirname(__file__) + '/tests.yaml') as f:
    tests = yaml.load(f, Loader=yaml.FullLoader)


@pytest.mark.parametrize("t", tests['adql_mysql_tests'])
def test_adql_mysql_translation(t):
    query, translated_query = t
    adt = ADQLQueryTranslator(query)
    if translated_query is not None:
        assert translated_query.strip() == adt.to_mysql()


@pytest.mark.parametrize("t", tests['adql_postgresql_tests'])
def test_adql_postgresql_parsing(t):
    _, postgres_query = t
    print(f"Failed query: {postgres_query}")
    PostgreSQLQueryProcessor(postgres_query)



@pytest.mark.parametrize("t", tests['adql_postgresql_tests'])
def test_adql_postgresql_translation(t):
    query, translated_query = t
    adt = ADQLQueryTranslator(query)
    if translated_query is not None:
        assert translated_query.strip() == adt.to_postgresql()


@pytest.mark.parametrize("t", tests['common_translation_tests'])
def test_adql_mysql_parsing_common(t):
    _test_parsing(MySQLQueryProcessor, t, translate=True)


@pytest.mark.parametrize("t", tests['common_translation_tests'])
def test_adql_postgresql_parsing_common(t):
    _test_parsing(PostgreSQLQueryProcessor, t, translate=True)


@pytest.mark.parametrize("t", tests['common_syntax_tests'])
def test_postgresql_syntax(t):
    with pytest.raises(QuerySyntaxError):
        ADQLQueryTranslator(t)

