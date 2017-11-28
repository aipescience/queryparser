# -*- coding: utf-8 -*-

from . import TestCase
from queryparser.exceptions import QueryError, QuerySyntaxError


class PostgresqlTestCase(TestCase):

    def test_query000(self):
        self._test_postgresql_parsing(
            """
            SELECT tab.a AS col1 FROM db.tab;
            """,
            ('db.tab.a',),
            (),
            (),
            ('col1: db.tab.a',),
            ('db.tab',)
        )

    def test_query001(self):
        self._test_postgresql_parsing(
            """
            SELECT a
            FROM db.tab,
            (VALUES (1, 'one'), (2, 'two'), (3, 'three')) AS t (num,letter);
            """,
            ('db.tab.a',),
            (),
            (),
            ('a: db.tab.a',),
            ('db.tab',)
        )

