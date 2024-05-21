# -*- coding: utf-8 -*-

from .utils import _test_parsing

from queryparser.exceptions import QueryError, QuerySyntaxError
from queryparser.mysql import MySQLQueryProcessor

import os
import pytest
import yaml


with open(os.path.dirname(__file__) + '/tests.yaml') as f:
    tests = yaml.load(f, Loader=yaml.FullLoader)


@pytest.mark.parametrize("t", tests['common_tests'])
def test_mysql_parsing_common(t):
    _test_parsing(MySQLQueryProcessor, t)


@pytest.mark.parametrize("t", tests['mysql_tests'])
def test_mysql_parsing(t):
    _test_parsing(MySQLQueryProcessor, t)


@pytest.mark.parametrize("t", tests['common_syntax_tests'])
def test_mysql_syntax(t):
    with pytest.raises(QuerySyntaxError):
        MySQLQueryProcessor(t)

@pytest.mark.parametrize("t", tests['common_query_tests'])
def test_mysql_query(t):
    with pytest.raises(QueryError):
        MySQLQueryProcessor(t)
