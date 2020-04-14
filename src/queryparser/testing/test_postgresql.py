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
        
    def test_query010(self):
        self._test_postgresql_parsing(
            """
            SELECT A.*, B.*
            FROM db1.table1 A
            LEFT JOIN db2.table1 B
            ON A.id = B.id;
            """,
            ('db1.table1.*', 'db2.table1.*'),
            ('join', '*'),
            (),
            ('*: db1.table1.*', '*: db2.table1.*'),
            ('db1.table1', 'db2.table1')
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

    def test_query039(self):
        self._test_postgresql_parsing(
            """
            SELECT ra, dec FROM gdr1.gaia_source
            WHERE pos @ scircle(spoint(1.44, 0.23), 0.01)
            """,
            ('gdr1.gaia_source.ra', 'gdr1.gaia_source.dec',
             'gdr1.gaia_source.pos'),
            ('where',),
            ('scircle', 'spoint'),
            ('ra: gdr1.gaia_source.ra', 'dec: gdr1.gaia_source.dec'),
            ('gdr1.gaia_source',)
        )

    def test_query040(self):
        self._test_postgresql_parsing(
            """
            SELECT ra, dec FROM gdr1.gaia_source
            WHERE pos @ scircle(spoint(1.44, 0.23), 0.01)
            """,
            ('gdr1.gaia_source.ra', 'gdr1.gaia_source.dec',
             'gdr1.gaia_source.pos'),
            ('where',),
            ('scircle', 'spoint'),
            ('ra: gdr1.gaia_source.ra', 'dec: gdr1.gaia_source.dec'),
            ('gdr1.gaia_source',)
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

    def test_query050(self):
        self._test_postgresql_parsing(
            """
            SELECT curves.observation_time,
                  mod(curves.observation_time - rrlyrae.epoch_g, rrlyrae.p1),
                  rrlyrae.p1 AS phase,
                  curves.g_magnitude,
                  2.5 / log(10) * curves.g_flux_error / curves.g_flux
                  AS g_magnitude_error
            FROM gdr1.phot_variable_time_series_gfov AS curves
            INNER JOIN gdr1.rrlyrae AS rrlyrae
            ON rrlyrae.source_id = curves.source_id
            WHERE rrlyrae.source_id = 5284240582308398080 
            AND pos @ sbox(spoint(1.44, 0.23), spoint(1.5, 0.3))
            """,
            (
                'gdr1.phot_variable_time_series_gfov.g_flux',
                'gdr1.phot_variable_time_series_gfov.g_flux_error',
                'gdr1.phot_variable_time_series_gfov.g_magnitude',
                'gdr1.phot_variable_time_series_gfov.observation_time',
                'gdr1.phot_variable_time_series_gfov.pos',
                'gdr1.phot_variable_time_series_gfov.source_id',
                'gdr1.rrlyrae.epoch_g',
                'gdr1.rrlyrae.p1',
                'gdr1.rrlyrae.source_id'
                ),
            ('where', 'join'),
            ('sbox', 'spoint', 'mod', 'log'),
            ('g_magnitude: gdr1.phot_variable_time_series_gfov.g_magnitude',
             'observation_time: gdr1.phot_variable_time_series_gfov.observation_time',
             'phase: gdr1.rrlyrae.p1'),
            ('gdr1.phot_variable_time_series_gfov', 'gdr1.rrlyrae')
        )

    def test_query051(self):
        self._test_postgresql_parsing(
            """
            SELECT q2.c / q1.c FROM (
                SELECT CAST(COUNT(*) AS FLOAT) AS c
                FROM gdr1.tgas_source
            ) AS q1 
            CROSS JOIN (
                SELECT COUNT(*) AS c
                FROM gdr1.tgas_source
                WHERE parallax / parallax_error > 10
            ) AS q2
            """,
            ('gdr1.tgas_source.parallax', 'gdr1.tgas_source.parallax_error',
             'gdr1.tgas_source.None'),
            ('where', ),
            ('COUNT',),
            (),
            ('gdr1.tgas_source',)
        )

    def test_query052(self):
        self._test_postgresql_parsing(
            """
	    SELECT * FROM gdr2.vari_cepheid AS v
	    JOIN gdr2.gaia_source AS g USING(source_id)
	    WHERE g.pos @ scircle(spoint(4.2917, -0.4629), 0.008) 
            """,
            ('gdr2.gaia_source.pos', 'gdr2.gaia_source.source_id',
             'gdr2.vari_cepheid.*'),
            ('where', 'join', '*'),
            ('scircle', 'spoint'),
            ('*: gdr2.vari_cepheid.*',),
            ('gdr2.gaia_source', 'gdr2.vari_cepheid')
        )

    def test_query053(self):
        '''
        Test non-standard space characters.
        '''
        self._test_postgresql_parsing(
            """
	    SELECT s FROM db.tab;
            """,
            ('db.tab.s',),
            (),
            (),
            ('s: db.tab.s',),
            ('db.tab',)
        )

    def test_syntax_error_001(self):
        q = """
            SELECT a FROM db.tab
            WHERE par = ”AAA”
            """
        with self.assertRaises(QuerySyntaxError):
            self._test_postgresql_parsing(q)
