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

    def test_query029(self):
        self._test_postgresql_parsing(
            """
            SELECT p.fofTreeId, p.treeSnapnum, p.mass, p.np
            FROM MDR1.FOFMtree AS p,
                 (SELECT fofTreeId, mainLeafId FROM MDR1.FOFMtree
            WHERE fofId=85000000000) AS mycl
            WHERE p.fofTreeId BETWEEN mycl.fofTreeId AND mycl.mainLeafId
            ORDER BY p.treeSnapnum
            """,
            ('MDR1.FOFMtree.fofTreeId', 'MDR1.FOFMtree.fofId',
             'MDR1.FOFMtree.mainLeafId', 'MDR1.FOFMtree.mass',
             'MDR1.FOFMtree.np', 'MDR1.FOFMtree.treeSnapnum'),
            ('where', 'order by'),
            (),
            ('fofTreeId: MDR1.FOFMtree.fofTreeId', 'mass: MDR1.FOFMtree.mass',
             'np: MDR1.FOFMtree.np',
             'treeSnapnum: MDR1.FOFMtree.treeSnapnum'),
            ('MDR1.FOFMtree',)
        )

    def test_query037(self):
        self._test_postgresql_parsing(
            """
            SELECT t.RAVE_OBS_ID AS c1, t.HEALPix AS c2,
                   h.logg_SC AS c3, h.TEFF AS c4
            FROM RAVEPUB_DR5.RAVE_DR5 AS t
            JOIN (
                SELECT sc.RAVE_OBS_ID, logg_SC, k.TEFF
                FROM RAVEPUB_DR5.RAVE_Gravity_SC sc
                JOIN (
                    SELECT RAVE_OBS_ID, TEFF
                    FROM RAVEPUB_DR5.RAVE_ON
                    LIMIT 1000
                ) AS k USING (RAVE_OBS_ID)
            ) AS h USING (RAVE_OBS_ID)
            """,
            ('RAVEPUB_DR5.RAVE_DR5.RAVE_OBS_ID',
             'RAVEPUB_DR5.RAVE_DR5.HEALPix', 'RAVEPUB_DR5.RAVE_ON.TEFF',
             'RAVEPUB_DR5.RAVE_Gravity_SC.logg_SC',
             'RAVEPUB_DR5.RAVE_ON.RAVE_OBS_ID',
             'RAVEPUB_DR5.RAVE_Gravity_SC.RAVE_OBS_ID'),
            ('join', 'limit'),
            (),
            ('c1: RAVEPUB_DR5.RAVE_DR5.RAVE_OBS_ID',
             'c2: RAVEPUB_DR5.RAVE_DR5.HEALPix',
             'c3: RAVEPUB_DR5.RAVE_Gravity_SC.logg_SC',
             'c4: RAVEPUB_DR5.RAVE_ON.TEFF'),
            ('RAVEPUB_DR5.RAVE_DR5', 'RAVEPUB_DR5.RAVE_Gravity_SC',
             'RAVEPUB_DR5.RAVE_ON')
        )

    def test_query038(self):
        self._test_postgresql_parsing(
            """
            SELECT arr[1:3] FROM db.phot;
            """,
            ('db.phot.arr',),
            (),
            (),
            ('arr: db.phot.arr',),
            ('db.phot',)
        )

    def test_query038(self):
        self._test_postgresql_parsing(
            """
            -- multidimensional matrices can be parsed too
            SELECT arr[1:3][1][2][3][4] FROM db.phot;
            """,
            ('db.phot.arr',),
            (),
            (),
            ('arr: db.phot.arr',),
            ('db.phot',)
        )

    def test_query044(self):
        self._test_postgresql_parsing(
            """
            SELECT COUNT(*) AS n, id, mra, mlem AS qqq, blem
            FROM (
                SELECT inner1.id, mra, mlem,
                       inner2.col3 + inner2.parallax AS blem
                FROM (
                    SELECT qwerty.id, MAX(ra) AS mra, inner1.parallax,
                           qwerty.mlem mlem
                    FROM db.tab dbt
                    JOIN (
                        SELECT rekt AS parallax, id, mlem
                        FROM db.bar
                    ) AS qwerty USING (id)
                ) AS inner1
                JOIN (
                    SELECT qqq, col2 AS ra2, parallax, subsub.col3
                    FROM (
                        SELECT ra AS qqq, col2, col3, parallax
                        FROM db.gaia AS gaia
                        WHERE col5 > 5
                    ) AS subsub
                ) AS inner2
                ON inner1.parallax = inner2.parallax
            ) AS subq
            GROUP BY id;
            """,
            ('db.bar.id', 'db.bar.rekt', 'db.bar.mlem', 'db.tab.id',
             'db.tab.ra', 'db.gaia.ra', 'db.gaia.col2',
             'db.gaia.col3', 'db.gaia.parallax', 'db.gaia.col5'),
            ('join', 'where', 'group by'),
            ('MAX', 'COUNT'),
            ('n: None.None.None', 'id: db.bar.id', 'mra: db.tab.ra',
             'qqq: db.bar.mlem', 'blem: None.None.blem'),
            ('db.tab', 'db.bar', 'db.gaia')
        )
