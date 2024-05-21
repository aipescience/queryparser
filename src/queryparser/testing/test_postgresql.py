# -*- coding: utf-8 -*-

from .utils import _test_parsing

from queryparser.postgresql import PostgreSQLQueryProcessor
from queryparser.exceptions import QueryError, QuerySyntaxError

import os
import pytest
import yaml


with open(os.path.dirname(__file__) + '/tests.yaml') as f:
    tests = yaml.load(f, Loader=yaml.FullLoader)


@pytest.mark.parametrize("t", tests['common_tests'])
def test_postgresql_parsing_common(t):
    _test_parsing(PostgreSQLQueryProcessor, t)


@pytest.mark.parametrize("t", tests['postgresql_tests'])
def test_postgresql_parsing(t):
    _test_parsing(PostgreSQLQueryProcessor, t)


@pytest.mark.parametrize("t", tests['common_syntax_tests'])
def test_postgresql_syntax(t):
    with pytest.raises(QuerySyntaxError):
        PostgreSQLQueryProcessor(t)


@pytest.mark.parametrize("t", tests['common_query_tests'])
def test_postrgresql_query(t):
    with pytest.raises(QueryError):
        PostgreSQLQueryProcessor(t)

