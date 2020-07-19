# -*- coding: utf-8 -*-

from . import _test_parsing, _test_adql_translation, _test_syntax

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
    _test_adql_translation(t + ['mysql'])


@pytest.mark.parametrize("t", tests['adql_postgresql_tests'])
def test_adql_postgresql_translation(t):
    _test_adql_translation(t + ['postgresql'])


@pytest.mark.parametrize("t", tests['common_translation_tests'])
def test_adql_mysql_parsing(t):
    _test_parsing(MySQLQueryProcessor, t, translate=True)


@pytest.mark.parametrize("t", tests['common_translation_tests'])
def test_adql_postgresql_parsing(t):
    _test_parsing(PostgreSQLQueryProcessor, t, translate=True)


@pytest.mark.parametrize("t", tests['common_syntax_tests'])
def test_postgresql_syntax(t):
    _test_syntax(ADQLQueryTranslator , t)
