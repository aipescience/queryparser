# -*- coding: utf-8 -*-

from . import _test_adql_translation

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

# class ADQLTestCase(TestCase):

    # def test_query000(self):
        # self._test_adql_mysql_translation(
            # """
                # SELECT POINT('icrs', 10, 10) AS "p" FROM "db".tab
            # """,
            # ''.join((
                # 'SELECT spoint(RADIANS(10.0), RADIANS(10.0)) AS `p` ',
                # 'FROM `db`.`tab`;'
            # )).strip()
        # )

    # def test_query001(self):
        # self._test_adql_mysql_translation(
            # """
                # SELECT TOP 10 AREA(CIRCLE('ICRS', "tab".RA, -2.23, 176.98))
                # FROM db.tab
            # """,
            # ''.join((
                # 'SELECT sarea(scircle(spoint(RADIANS(`tab`.`RA`), ',
                # 'RADIANS(-2.23)), RADIANS(176.98))) FROM `db`.`tab` LIMIT 10;'
            # )).strip()
        # )

    # def test_query002(self):
        # self._test_adql_mysql_translation(
            # """
                # SELECT BOX('ICRS', 25.4, -20.5, 1.1, 1.2) FROM db.tab
            # """,
            # ''.join((
                # 'SELECT sbox(spoint(RADIANS(25.4),RADIANS(-20.5)),',
                # 'spoint(RADIANS(26.500000000000),RADIANS(-19.300000000000))) FROM `db`.`tab`;'
            # )).strip()
        # )

    # def test_query003(self):
        # self._test_adql_mysql_translation(
            # """
                # SELECT TOP 10 CONTAINS(POINT('ICRS', 0, 0),
                                       # CIRCLE('ICRS', 0, 0, 1))
                # FROM db.tab
            # """,
            # ''.join((
                # 'SELECT srcontainsl(spoint(RADIANS(0.0), RADIANS(0.0)), ',
                # 'scircle(spoint(RADIANS(0.0), RADIANS(0.0)), RADIANS(1.0))) ',
                # 'FROM `db`.`tab` LIMIT 10;'
            # )).strip()
        # )

    # def test_query004(self):
        # self._test_adql_mysql_translation(
            # """
                # SELECT DISTANCE(POINT('ICRS', 0, 0), POINT('ICRS', 0, 1))
                # FROM db.tab
            # """,
            # ''.join((
                # 'SELECT DEGREES(sdist(spoint(RADIANS(0.0), RADIANS(0.0)), ',
                # 'spoint(RADIANS(0.0), RADIANS(1.0)))) FROM `db`.`tab`;'
            # )).strip()
        # )

    # def test_query005(self):
        # self._test_adql_mysql_translation(
            # """
                # SELECT INTERSECTS(CIRCLE('ICRS', 0, 0, 10),
                                  # BOX('ICRS', 2, 0, 10, 10))
                # FROM db.tab;
            # """,
            # ''.join((
                # 'SELECT soverlaps(scircle(spoint(RADIANS(0.0), RADIANS(0.0))',
                # ', RADIANS(10.0)), sbox(spoint(RADIANS(2.0),RADIANS(0.0)),',
                # 'spoint(RADIANS(12.000000000000),RADIANS(10.000000000000)))) FROM `db`.`tab`;'
            # )).strip()
        # )

    # def test_query006(self):
        # self._test_adql_mysql_translation(
            # """
                # SELECT CENTROID(CIRCLE('ICRS', "tab".RA, -20/4., 1))
                # FROM db.tab
            # """,
            # ''.join((
                # 'SELECT scenter(scircle(spoint(RADIANS(`tab`.`RA`), ',
                # 'RADIANS(-5.0)), RADIANS(1.0))) FROM `db`.`tab`;'
            # )).strip()
        # )

    # def test_query020(self):
        # self._test_adql_mysql_translation(
            # """
                # SELECT TOP 10 DISTANCE(POINT('ICRS',0,0),
                    # POINT('ICRS',"VII/233/xsc".RAJ2000,"VII/233/xsc".DEJ2000))
                # FROM db."VII/233/xsc"
            # """,
            # ''.join((
                # 'SELECT DEGREES(sdist(spoint(RADIANS(0.0), RADIANS(0.0)), ',
                # 'spoint(RADIANS(`VII/233/xsc`.`RAJ2000`), ',
                # 'RADIANS(`VII/233/xsc`.`DEJ2000`)))) FROM ',
                # '`db`.`VII/233/xsc` LIMIT 10;'
            # )).strip()
        # )

    # def test_query021(self):
        # self._test_adql_mysql_translation(
            # """
                # SELECT TOP 1 source_id, ra, dec, DISTANCE(POINT('ICRS',ra,dec),
                     # POINT('ICRS',266.41683,-29.00781)) AS dist
                # FROM GDR1.gaia_source
                # WHERE 1=CONTAINS(POINT('ICRS',ra,dec),
                             # CIRCLE('ICRS',266.41683,-29.00781, 0.08333333))
            # """,
            # ''.join((
                # 'SELECT `source_id`, `ra`, `dec`, ',
                # 'DEGREES(sdist(spoint(RADIANS(`ra`), RADIANS(`dec`)), ',
                # 'spoint(RADIANS(266.41683), RADIANS(-29.00781)))) AS dist ',
                # 'FROM `GDR1`.`gaia_source` WHERE 1 = ',
                # 'srcontainsl(spoint(RADIANS(`ra`), RADIANS(`dec`)), ',
                # 'scircle(spoint(RADIANS(266.41683), RADIANS(-29.00781)), ',
                # 'RADIANS(0.08333333))) LIMIT 1;'
            # )).strip()
        # )

    # def test_query022(self):
        # self._test_adql_mysql_translation(
            # """
            # SELECT DISTANCE(
            # POINT('ICRS', ra, dec),
            # POINT('ICRS', 266.41683, -29.00781)
            # ) AS dist
            # FROM gaiadr1.gaia_source
            # WHERE 1=CONTAINS(
                # POINT('ICRS', ra, dec),
                # CIRCLE('ICRS', 266.41683, -29.00781, 0.08333333)
                # )
            # ORDER BY dist ASC
            # """,
            # ''.join((
                # 'SELECT DEGREES(sdist(spoint(RADIANS(`ra`), RADIANS(`dec`)), ',
                # 'spoint(RADIANS(266.41683), RADIANS(-29.00781)))) AS dist ',
                # 'FROM `gaiadr1`.`gaia_source` WHERE 1 = ',
                # 'srcontainsl(spoint(RADIANS(`ra`), RADIANS(`dec`)), ',
                # 'scircle(spoint(RADIANS(266.41683), RADIANS(-29.00781)), ',
                # 'RADIANS(0.08333333))) ORDER BY `dist` ASC;'
            # )).strip()
        # )

    # def test_query023(self):
        # self._test_adql_mysql_translation(
            # """
            # SELECT *
            # FROM gaiadr1.gaia_source
            # WHERE 1=CONTAINS(
            # POINT('ICRS',ra,dec),
            # CIRCLE('ICRS',266.41683,-29.00781, 0.08333333)
            # )
            # AND phot_g_mean_mag>=10 AND phot_g_mean_mag<15
            # ORDER BY phot_g_mean_mag ASC
            # """,
            # ''.join((
                # 'SELECT * FROM `gaiadr1`.`gaia_source` WHERE 1 = ',
                # 'srcontainsl(spoint(RADIANS(`ra`), RADIANS(`dec`)), ',
                # 'scircle(spoint(RADIANS(266.41683), RADIANS(-29.00781)), ',
                # 'RADIANS(0.08333333))) AND `phot_g_mean_mag` >= 10 AND ',
                # '`phot_g_mean_mag` < 15 ORDER BY `phot_g_mean_mag` ASC;'
            # )).strip()
        # )

    # def test_query024(self):
        # self._test_adql_mysql_translation(
            # """
            # SELECT TOP 10
            # gaia_healpix_index(6, source_id) AS healpix_6,
            # count(*) / 0.83929 as sources_per_sq_deg,
            # avg(astrometric_n_good_obs_al) AS avg_n_good_al,
            # avg(astrometric_n_good_obs_ac) AS avg_n_good_ac,
            # avg(astrometric_n_good_obs_al + astrometric_n_good_obs_ac)
                # AS avg_n_good,
            # avg(astrometric_excess_noise) as avg_excess_noise
            # FROM gaiadr1.tgas_source
            # GROUP BY healpix_6
            # """,
            # ''.join((
                # 'SELECT gaia_healpix_index(6, `source_id`) AS healpix_6, ',
                # 'count(*) / 0.83929 AS sources_per_sq_deg, ',
                # 'avg(`astrometric_n_good_obs_al`) AS avg_n_good_al, ',
                # 'avg(`astrometric_n_good_obs_ac`) AS avg_n_good_ac, ',
                # 'avg(`astrometric_n_good_obs_al` + ',
                # '`astrometric_n_good_obs_ac`) AS avg_n_good, ',
                # 'avg(`astrometric_excess_noise`) AS avg_excess_noise FROM ',
                # '`gaiadr1`.`tgas_source` GROUP BY `healpix_6` LIMIT 10;'
            # )).strip()
        # )

    # def test_query025(self):
        # self._test_adql_mysql_translation(
            # """
            # SELECT gaia.source_id, gaia.hip,
            # gaia.phot_g_mean_mag + 5 * log10(gaia.parallax) - 10
                # AS g_mag_abs_gaia,
            # gaia.phot_g_mean_mag + 5 * log10(hip.plx) - 10
                # AS g_mag_abs_hip
            # FROM gaiadr1.tgas_source AS gaia
            # INNER JOIN "public".hipparcos_newreduction AS hip
            # ON gaia.hip = hip.hip
            # WHERE gaia.parallax/gaia.parallax_error >= 5 AND
            # hip.plx/hip.e_plx >= 5 AND
            # hip.e_b_v > 0.0 and hip.e_b_v <= 0.05 AND
            # hip.b_v >= 1.0 AND hip.b_v <= 1.1 AND
            # 2.5 / log(10) * gaia.phot_g_mean_flux_error /
                # gaia.phot_g_mean_flux <= 0.05
            # """,
            # ''.join((
                # 'SELECT `gaia`.`source_id`, `gaia`.`hip`, ',
                # '`gaia`.`phot_g_mean_mag` + 5 * log10(`gaia`.`parallax`) - ',
                # '10 AS g_mag_abs_gaia, `gaia`.`phot_g_mean_mag` + 5 * ',
                # 'log10(`hip`.`plx`) - 10 AS g_mag_abs_hip FROM ',
                # '`gaiadr1`.`tgas_source` AS `gaia` INNER JOIN ',
                # '`public`.`hipparcos_newreduction` AS `hip` ON `gaia`.`hip` ',
                # '= `hip`.`hip` WHERE `gaia`.`parallax` / ',
                # '`gaia`.`parallax_error` >= 5 AND `hip`.`plx` / ',
                # '`hip`.`e_plx` >= 5 AND `hip`.`e_b_v` > 0.0 and ',
                # '`hip`.`e_b_v` <= 0.05 AND `hip`.`b_v` >= 1.0 AND ',
                # '`hip`.`b_v` <= 1.1 AND 2.5 / log(10) * ',
                # '`gaia`.`phot_g_mean_flux_error` / `gaia`.`phot_g_mean_flux` ',
                # '<= 0.05;'
            # )).strip()
        # )

    # def test_query026(self):
        # self._test_adql_mysql_translation(
            # """
            # SELECT g_mag_abs_hip_index / 5. AS g_mag_abs_hip,
                   # count(g_mag_abs_hip_index) AS freq
            # FROM (
            # SELECT floor((gaia.phot_g_mean_mag + 5 * log10(hip.plx) - 10) * 5)
                # AS g_mag_abs_hip_index
            # FROM gaiadr1.tgas_source AS gaia
            # INNER JOIN "public".hipparcos_newreduction AS hip
            # ON gaia.hip = hip.hip
            # WHERE gaia.parallax/gaia.parallax_error >= 5 AND
            # hip.plx/hip.e_plx >= 5 AND
            # hip.e_b_v > 0.0 and hip.e_b_v <= 0.05 AND
            # hip.b_v >= 1.0 and hip.b_v <= 1.1 AND
            # 2.5 / log(10) * gaia.phot_g_mean_flux_error /
                # gaia.phot_g_mean_flux <= 0.05
            # ) AS subquery
            # GROUP BY g_mag_abs_hip_index
            # ORDER BY g_mag_abs_hip
            # """,
            # ''.join((
                # 'SELECT `g_mag_abs_hip_index` / 5. AS g_mag_abs_hip, ',
                # 'count(`g_mag_abs_hip_index`) AS freq FROM (SELECT ',
                # 'floor((`gaia`.`phot_g_mean_mag` + 5 * log10(`hip`.`plx`) - ',
                # '10) * 5) AS g_mag_abs_hip_index FROM ',
                # '`gaiadr1`.`tgas_source` AS `gaia` INNER JOIN ',
                # '`public`.`hipparcos_newreduction` AS `hip` ON `gaia`.`hip` =',
                # ' `hip`.`hip` WHERE `gaia`.`parallax` / ',
                # '`gaia`.`parallax_error` >= 5 AND `hip`.`plx` / `hip`.`e_plx`',
                # ' >= 5 AND `hip`.`e_b_v` > 0.0 and `hip`.`e_b_v` <= 0.05 AND ',
                # '`hip`.`b_v` >= 1.0 and `hip`.`b_v` <= 1.1 AND 2.5 / log(10) ',
                # '* `gaia`.`phot_g_mean_flux_error` / ',
                # '`gaia`.`phot_g_mean_flux` <= 0.05) AS `subquery` GROUP BY ',
                # '`g_mag_abs_hip_index` ORDER BY `g_mag_abs_hip`;'
            # )).strip()
        # )

    # def test_query027(self):
        # self._test_adql_mysql_translation(
            # """
            # SELECT TOP 10 gaia.source_id,
            # gaia.phot_g_mean_mag + 5 * log10(gaia.parallax) - 10 AS g_mag_abs ,
            # gaia.phot_g_mean_mag - tmass.ks_m AS g_min_ks
            # FROM gaiadr1.tgas_source AS gaia
            # INNER JOIN gaiadr1.tmass_best_neighbour AS xmatch
            # ON gaia.source_id = xmatch.source_id
            # INNER JOIN gaiadr1.tmass_original_valid AS tmass
            # ON tmass.tmass_oid = xmatch.tmass_oid
            # WHERE gaia.parallax/gaia.parallax_error >= 5 AND
            # ph_qual = 'AAA' AND
            # sqrt(power(2.5 / log(10) * gaia.phot_g_mean_flux_error
                # / gaia.phot_g_mean_flux, 2) ) <= 0.05 AND
            # sqrt(power(2.5/log(10)*gaia.phot_g_mean_flux_error
                # / gaia.phot_g_mean_flux, 2)
                # + power(tmass.ks_msigcom, 2)) <= 0.05
            # """,
            # ''.join((
                # 'SELECT `gaia`.`source_id`, `gaia`.`phot_g_mean_mag` + 5 * ',
                # 'log10(`gaia`.`parallax`) - 10 AS g_mag_abs, ',
                # '`gaia`.`phot_g_mean_mag` - `tmass`.`ks_m` AS g_min_ks FROM ',
                # '`gaiadr1`.`tgas_source` AS `gaia` INNER JOIN ',
                # '`gaiadr1`.`tmass_best_neighbour` AS `xmatch` ON ',
                # '`gaia`.`source_id` = `xmatch`.`source_id` INNER JOIN ',
                # '`gaiadr1`.`tmass_original_valid` AS `tmass` ON ',
                # '`tmass`.`tmass_oid` = `xmatch`.`tmass_oid` WHERE ',
                # '`gaia`.`parallax` / `gaia`.`parallax_error` >= 5 AND ',
                # "`ph_qual` = 'AAA' AND sqrt(power(2.5 / log(10) * ",
                # '`gaia`.`phot_g_mean_flux_error` / `gaia`.`phot_g_mean_flux`,',
                # ' 2)) <= 0.05 AND sqrt(power(2.5 / log(10) * ',
                # '`gaia`.`phot_g_mean_flux_error` / ',
                # '`gaia`.`phot_g_mean_flux`, 2) + power(`tmass`.`ks_msigcom`, ',
                # '2)) <= 0.05 LIMIT 10;'
            # )).strip()
        # )

    # def test_query028(self):
        # self._test_adql_mysql_translation(
            # """
            # SELECT
            # g_min_ks_index / 10 AS g_min_ks,
            # g_mag_abs_index / 10 AS g_mag_abs,
            # count(*) AS n
            # FROM (
            # SELECT TOP 10 gaia.source_id,
            # floor((gaia.phot_g_mean_mag+5*log10(gaia.parallax)-10) * 10)
                # AS g_mag_abs_index,
            # floor((gaia.phot_g_mean_mag-tmass.ks_m) * 10) AS g_min_ks_index
            # FROM gaiadr1.tgas_source AS gaia
            # INNER JOIN gaiadr1.tmass_best_neighbour AS xmatch
            # ON gaia.source_id = xmatch.source_id
            # INNER JOIN gaiadr1.tmass_original_valid AS tmass
            # ON tmass.tmass_oid = xmatch.tmass_oid
            # WHERE gaia.parallax/gaia.parallax_error >= 5 AND
            # ph_qual = 'AAA' AND
            # sqrt(power(2.5 / log(10) * gaia.phot_g_mean_flux_error /
                # gaia.phot_g_mean_flux, 2)) <= 0.05 AND
            # sqrt(power(2.5 / log(10) * gaia.phot_g_mean_flux_error /
                # gaia.phot_g_mean_flux, 2)
            # + power(tmass.ks_msigcom, 2)) <= 0.05
            # )AS subquery
            # GROUP BY g_min_ks_index, g_mag_abs_index
            # """,
            # ''.join((
                # 'SELECT `g_min_ks_index` / 10 AS g_min_ks, `g_mag_abs_index` ',
                # '/ 10 AS g_mag_abs, count(*) AS n FROM (SELECT ',
                # '`gaia`.`source_id`, floor((`gaia`.`phot_g_mean_mag` + 5 * ',
                # 'log10(`gaia`.`parallax`) - 10) * 10) AS g_mag_abs_index, ',
                # 'floor((`gaia`.`phot_g_mean_mag` - `tmass`.`ks_m`) * 10) AS ',
                # 'g_min_ks_index FROM `gaiadr1`.`tgas_source` AS `gaia` INNER ',
                # 'JOIN `gaiadr1`.`tmass_best_neighbour` AS `xmatch` ON ',
                # '`gaia`.`source_id` = `xmatch`.`source_id` INNER JOIN ',
                # '`gaiadr1`.`tmass_original_valid` AS `tmass` ON ',
                # '`tmass`.`tmass_oid` = `xmatch`.`tmass_oid` WHERE ',
                # '`gaia`.`parallax` / `gaia`.`parallax_error` >= 5 AND ',
                # "`ph_qual` = 'AAA' AND sqrt(power(2.5 / log(10) * ",
                # '`gaia`.`phot_g_mean_flux_error` / ',
                # '`gaia`.`phot_g_mean_flux`, 2)) <= 0.05 AND sqrt(power(2.5 / ',
                # 'log(10) * `gaia`.`phot_g_mean_flux_error` / ',
                # '`gaia`.`phot_g_mean_flux`, 2) + power(`tmass`.`ks_msigcom`, ',
                # '2)) <= 0.05 LIMIT 10) AS `subquery` GROUP BY ',
                # '`g_min_ks_index`, `g_mag_abs_index`;'
            # )).strip()
        # )

    # def test_query029(self):
        # self._test_adql_mysql_translation(
            # """
            # SELECT POLYGON('ICRS', 1.0, -1.0, 2.0, -2.0, 3.0, -3.0)
            # FROM db.tab
            # """,
            # ''.join((
                # "SELECT spoly('{(1.0d,-1.0d),(2.0d,-2.0d),(3.0d,-3.0d)}') ",
                # 'FROM `db`.`tab`;'
            # )).strip()
        # )

    # def test_query030(self):
        # self._test_adql_mysql_translation(
            # """
            # SELECT TOP 10 a FROM (
                # SELECT TOP 20 foo AS a
                # FROM (
                    # SELECT TOP 30 ra AS foo FROM db.tab
                # ) AS subsub
            # ) AS sub;
            # """,
            # ''.join((
                # 'SELECT `a` FROM (SELECT `foo` AS a FROM (SELECT `ra` AS foo '
                # 'FROM `db`.`tab` LIMIT 30) AS `subsub` LIMIT 20) AS `sub` ',
                # 'LIMIT 10;'
            # )).strip()
        # )

    # def test_query031(self):
        # self._test_adql_mysql_translation(
            # """
            # SELECT a
            # FROM (
                # SELECT TOP 5 a
                # FROM db.tab, (
                    # SELECT TOP 10 *
                    # FROM db.foo
                # ) AS sub
            # ) AS qqq
            # """,
            # ''.join((
                # 'SELECT `a` FROM (SELECT `a` FROM `db`.`tab`, (SELECT * FROM ',
                # '`db`.`foo` LIMIT 10) AS `sub` LIMIT 5) AS `qqq`;'
            # )).strip()
        # )

    # def test_query032(self):
        # self._test_adql_mysql_translation(
            # """
            # SELECT TOP 2 a
            # FROM (
                # SELECT a
                # FROM db.tab, (
                    # SELECT TOP 10 *
                    # FROM db.foo
                # ) AS sub
            # ) AS qqq
            # """,
            # ''.join((
                # 'SELECT `a` FROM (SELECT `a` FROM `db`.`tab`, (SELECT * FROM ',
                # '`db`.`foo` LIMIT 10) AS `sub`) AS `qqq` LIMIT 2;'
            # )).strip()
        # )

    # def test_query033(self):
        # self._test_adql_mysql_translation(
            # """
            # SELECT TOP 2 a
            # FROM (
                # SELECT TOP 5 a
                # FROM db.tab, (
                    # SELECT *
                    # FROM db.foo
                # ) AS sub
            # ) AS qqq
            # """,
            # ''.join((
                # 'SELECT `a` FROM (SELECT `a` FROM `db`.`tab`, (SELECT * FROM ',
                # '`db`.`foo`) AS `sub` LIMIT 5) AS `qqq` LIMIT 2;'
            # )).strip()
        # )

    # def test_syntax_error_001(self):
        # q = """SELECR a FROM db.tab;"""
        # with self.assertRaises(QuerySyntaxError):
            # self._test_adql_mysql_translation(q)

    # def test_query_error_001(self):
        # adt = ADQLQueryTranslator()
        # with self.assertRaises(QueryError):
            # adt.to_mysql()

    # def test_query_error_002(self):
        # q = """
            # SELECT a FROM db.tab
            # INTERSECT
            # SELECT b FROM db.tab;
            # """
        # with self.assertRaises(QueryError):
            # self._test_adql_mysql_translation_parsing(q)

    # def test_query_error_003(self):
        # q = """
            # SELECT a FROM db.tab
            # EXCEPT
            # SELECT b FROM db.tab;
            # """
        # with self.assertRaises(QueryError):
            # self._test_adql_mysql_translation_parsing(q)

    # def test_query_error_004(self):
        # q = """
            # WITH t1 AS (
                # SELECT a FROM db.tab
            # )
            # SELECT t1.* FROM t1;
            # """
        # with self.assertRaises(QueryError):
            # self._test_adql_mysql_translation_parsing(q)

    # def test_query100(self):
        # self._test_adql_mysql_translation_parsing(
            # """
            # SELECT POINT('icrs', ra, de) FROM db.tab
            # """,
            # ('db.tab.ra', 'db.tab.de'),
            # (),
            # ('spoint', 'RADIANS')
        # )

    # def test_query101(self):
        # self._test_adql_mysql_translation_parsing(
            # """
            # SELECT
            # g_min_ks_index / 10 AS g_min_ks,
            # g_mag_abs_index / 10 AS g_mag_abs,
            # count(*) AS n
            # FROM (
                # SELECT TOP 10 gaia.source_id,
                # floor((gaia.phot_g_mean_mag+5*log10(gaia.parallax)-10) * 10)
                    # AS g_mag_abs_index,
                # floor((gaia.phot_g_mean_mag-tmass.ks_m) * 10) AS g_min_ks_index
                # FROM gaiadr1.tgas_source AS gaia
                # INNER JOIN gaiadr1.tmass_best_neighbour AS xmatch
                # ON gaia.source_id = xmatch.source_id
                # INNER JOIN gaiadr1.tmass_original_valid AS tmass
                # ON tmass.tmass_oid = xmatch.tmass_oid
                # WHERE gaia.parallax/gaia.parallax_error >= 5 AND
                # xmatch.ph_qual = 'AAA' AND
                # sqrt(power(2.5 / log(10) * gaia.phot_g_mean_flux_error /
                    # gaia.phot_g_mean_flux, 2)) <= 0.05 AND
                # sqrt(power(2.5 / log(10) * gaia.phot_g_mean_flux_error /
                    # gaia.phot_g_mean_flux, 2)
                # + power(tmass.ks_msigcom, 2)) <= 0.05
            # ) AS subquery
            # GROUP BY g_min_ks_index, g_mag_abs_index
            # """,
            # ('gaiadr1.tgas_source.source_id',
             # 'gaiadr1.tgas_source.parallax',
             # 'gaiadr1.tgas_source.parallax_error',
             # 'gaiadr1.tgas_source.phot_g_mean_flux',
             # 'gaiadr1.tgas_source.phot_g_mean_flux_error',
             # 'gaiadr1.tgas_source.phot_g_mean_mag',
             # 'gaiadr1.tmass_best_neighbour.ph_qual',
             # 'gaiadr1.tmass_best_neighbour.source_id',
             # 'gaiadr1.tmass_best_neighbour.tmass_oid',
             # 'gaiadr1.tmass_original_valid.ks_m',
             # 'gaiadr1.tmass_original_valid.ks_msigcom',
             # 'gaiadr1.tmass_original_valid.tmass_oid',
             # ),
            # ('limit', 'where', 'join', 'group by'),
            # ('sqrt', 'log10', 'log', 'count', 'floor', 'power')
        # )

    # def test_query102(self):
        # self._test_adql_mysql_translation_parsing(
            # """
                # SELECT TOP 1 source_id, ra, dec, DISTANCE(POINT('ICRS',ra,dec),
                     # POINT('ICRS',266.41683,-29.00781)) AS dist
                # FROM GDR1.gaia_source
                # WHERE 1=CONTAINS(POINT('ICRS',ra,dec),
                                # CIRCLE('ICRS',266.41683,-29.00781, 0.08333333))
            # """,
            # ('GDR1.gaia_source.source_id',
             # 'GDR1.gaia_source.ra',
             # 'GDR1.gaia_source.dec'),
            # (),
            # (),
            # ('source_id: GDR1.gaia_source.source_id',
             # 'ra: GDR1.gaia_source.ra',
             # 'dec: GDR1.gaia_source.dec')
        # )

    # def test_query103(self):
        # self._test_adql_mysql_translation_parsing(
            # """
            # SELECT POINT('icrs', ra, dec) as "p", z AS y FROM "db".tab
            # """,
            # ('db.tab.ra', 'db.tab.dec', 'db.tab.z'),
            # (),
            # ('spoint', 'RADIANS'),
            # ('y: db.tab.z',)
        # )

    # def test_query104(self):
        # self._test_adql_mysql_translation_parsing(
            # """
            # SELECT a FROM db.tab WHERE a IN (b)
            # """,
            # ('db.tab.a', 'db.tab.b'),
            # ('where',),
            # (),
            # ('a: db.tab.a',)
        # )

    # def test_query200(self):
        # self._test_adql_postgresql_translation(
            # """
                # SELECT POINT('icrs', 10, 10) AS "p" FROM "db".tab
            # """,
            # ''.join((
                # 'SELECT spoint(RADIANS(10.0), RADIANS(10.0)) AS "p" ',
                # 'FROM "db".tab;'
            # )).strip()
        # )

    # def test_query201(self):
        # self._test_adql_postgresql_translation(
            # """
                # SELECT TOP 10 AREA(CIRCLE('ICRS', "tab".RA, -2.23, 176.98))
                # FROM db.tab
            # """,
            # ''.join((
                # 'SELECT area(scircle(spoint(RADIANS("tab".RA), ',
                # 'RADIANS(-2.23)), RADIANS(176.98))) FROM db.tab LIMIT 10;'
            # )).strip()
        # )

    # def test_query202(self):
        # self._test_adql_postgresql_translation(
            # """
                # SELECT BOX('ICRS', 25.4, -20.5, 1.1, 1.2) FROM db.tab
            # """,
            # ''.join((
                # 'SELECT sbox(spoint(RADIANS(25.4),RADIANS(-20.5)),',
                # 'spoint(RADIANS(26.500000000000),RADIANS(-19.300000000000))) FROM db.tab;'
            # )).strip()
        # )

    # def test_query203(self):
        # self._test_adql_postgresql_translation(
            # """
                # SELECT TOP 10 CONTAINS(POINT('ICRS', 0, 0),
                                       # CIRCLE('ICRS', 0, 0, 1))
                # FROM db.tab
            # """,
            # ''.join((
                # 'SELECT spoint(RADIANS(0.0), RADIANS(0.0)) @ ',
                # 'scircle(spoint(RADIANS(0.0), RADIANS(0.0)), RADIANS(1.0)) ',
                # 'FROM db.tab LIMIT 10;'
            # )).strip()
        # )

    # def test_query204(self):
        # self._test_adql_postgresql_translation(
            # """
                # SELECT DISTANCE(POINT('ICRS', 0, 0), POINT('ICRS', 0, 1))
                # FROM db.tab
            # """,
            # ''.join((
                # 'SELECT DEGREES(spoint(RADIANS(0.0), RADIANS(0.0)) <-> ',
                # 'spoint(RADIANS(0.0), RADIANS(1.0))) FROM db.tab;'
            # )).strip()
        # )

    # def test_query204(self):
        # self._test_adql_postgresql_translation(
            # """
                # SELECT DISTANCE(POINT('ICRS', 0, 0), POINT('ICRS', 0, 1))
                # FROM db.tab
            # """,
            # ''.join((
                # 'SELECT DEGREES(spoint(RADIANS(0.0), RADIANS(0.0)) <-> ',
                # 'spoint(RADIANS(0.0), RADIANS(1.0))) FROM db.tab;'
            # )).strip()
        # )

    # def test_query205(self):
        # self._test_adql_postgresql_translation_parsing(
            # """
                # SELECT TOP 1 source_id, ra, dec, DISTANCE(POINT('ICRS',ra,dec),
                     # POINT('ICRS',266.41683,-29.00781)) AS dist
                # FROM GDR1.gaia_source
                # WHERE 1=CONTAINS(POINT('ICRS',ra,dec),
                                # CIRCLE('ICRS',266.41683,-29.00781, 0.08333333))
            # """,
            # ('GDR1.gaia_source.source_id',
             # 'GDR1.gaia_source.ra',
             # 'GDR1.gaia_source.dec'),
            # (),
            # (),
            # (('GDR1', 'gaia_source'),),
            # ('source_id: GDR1.gaia_source.source_id',
             # 'ra: GDR1.gaia_source.ra',
             # 'dec: GDR1.gaia_source.dec')
        # )

    # def test_query206(self):
        # self._test_adql_postgresql_translation_parsing(
            # """
                # SELECT gaia.source_id, gaia.parallax
                # FROM gdr1.tgas_source AS gaia
                # WHERE CONTAINS(POINT('ICRS', gaia.ra, gaia.dec),
                               # CIRCLE('ICRS', 56.75, 24.12, 5)) = 1
                # AND SQRT(POWER(gaia.pmra - 20.5, 2) +
                         # POWER(gaia.pmdec + 45.5, 2)) < 6.0
            # """,
            # ('gdr1.tgas_source.source_id',
             # 'gdr1.tgas_source.ra',
             # 'gdr1.tgas_source.dec',
             # 'gdr1.tgas_source.pmra',
             # 'gdr1.tgas_source.pmdec',
             # 'gdr1.tgas_source.parallax'),
            # ('where',),
            # ('spoint', 'scircle', 'POWER', 'SQRT', 'RADIANS'),
            # (('gdr1', 'tgas_source'),),
            # ('source_id: gdr1.tgas_source.source_id',
             # 'parallax: gdr1.tgas_source.parallax')
        # )

    # def test_query207(self):
        # self._test_adql_postgresql_translation_parsing(
            # """
                # SELECT gaia.source_id,
                       # gaia.phot_g_mean_mag + 5 * LOG10(gaia.parallax) -
                       # 10 AS g_mag_abs,
                       # gaia.phot_g_mean_mag - tmass.ks_m AS g_min_ks
                # FROM gdr1.tgas_source as gaia
                # INNER JOIN gdr1.tmass_best_neighbour AS xmatch
                # ON gaia.source_id = xmatch.source_id
                # INNER JOIN gdr1.tmass_original_valid AS tmass
                # ON tmass.tmass_oid = xmatch.tmass_oid
                # WHERE gaia.parallax / gaia.parallax_error >= 5 
                # AND tmass.ph_qual = 'AAA' 
                # AND SQRT(POWER(2.5 / log(10) *
                    # gaia.phot_g_mean_flux_error / gaia.phot_g_mean_flux, 2))
                    # <= 0.05 
                # AND SQRT(POWER(2.5 / log(10) *
                    # gaia.phot_g_mean_flux_error / gaia.phot_g_mean_flux, 2) +
                    # power(tmass.ks_msigcom, 2)) <= 0.05
            # """,
            # ('gdr1.tgas_source.source_id',
             # 'gdr1.tgas_source.parallax',
             # 'gdr1.tgas_source.parallax_error',
             # 'gdr1.tgas_source.phot_g_mean_mag',
             # 'gdr1.tgas_source.phot_g_mean_flux_error',
             # 'gdr1.tgas_source.phot_g_mean_flux',
             # 'gdr1.tmass_best_neighbour.source_id',
             # 'gdr1.tmass_best_neighbour.tmass_oid',
             # 'gdr1.tmass_original_valid.ks_m',
             # 'gdr1.tmass_original_valid.ph_qual',
             # 'gdr1.tmass_original_valid.tmass_oid',
             # 'gdr1.tmass_original_valid.ks_msigcom'),
            # ('where', 'join'),
            # ('LOG', 'log', 'SQRT', 'power', 'POWER'),
            # (('gdr1', 'tgas_source'),
             # ('gdr1', 'tmass_original_valid'),
             # ('gdr1', 'tmass_best_neighbour')),
            # ('source_id: gdr1.tgas_source.source_id',
             # )
        # )

    # def test_query208(self):
        # self._test_adql_postgresql_translation_parsing(
            # """
                # SELECT gaia.source_id, gaia.hip,
                       # gaia.phot_g_mean_mag + 5 * log10(gaia.parallax) - 10
                       # AS g_mag_abs_gaia,
                       # gaia.phot_g_mean_mag + 5 * log10(hip.plx) - 10
                       # AS g_mag_abs_hip
                # FROM gdr1.tgas_source AS gaia
                # INNER JOIN public.hipparcos AS hip
                # ON gaia.hip = hip.hip
                # WHERE gaia.parallax / gaia.parallax_error >= 5
                # AND hip.plx / hip.e_plx >= 5
                # AND hip.e_b_v > 0.0 AND hip.e_b_v <= 0.05
                # AND hip.b_v >= 1.0 AND hip.b_v <= 1.1
                # AND 2.5 / log(10) * gaia.phot_g_mean_flux_error /
                    # gaia.phot_g_mean_flux <= 0.05
            # """,
            # ('gdr1.tgas_source.source_id',
             # 'gdr1.tgas_source.hip',
             # 'gdr1.tgas_source.parallax',
             # 'gdr1.tgas_source.parallax_error',
             # 'gdr1.tgas_source.phot_g_mean_mag',
             # 'gdr1.tgas_source.phot_g_mean_flux_error',
             # 'gdr1.tgas_source.phot_g_mean_flux',
             # 'public.hipparcos.hip',
             # 'public.hipparcos.plx',
             # 'public.hipparcos.e_plx',
             # 'public.hipparcos.b_v',
             # 'public.hipparcos.e_b_v'),
            # ('where', 'join'),
            # ('LOG', 'log'),
            # (('public', 'hipparcos'),
             # ('gdr1', 'tgas_source')),
            # ('source_id: gdr1.tgas_source.source_id',
             # 'hip: gdr1.tgas_source.hip',
             # )
        # )

    # def test_query209(self):
        # self._test_adql_postgresql_translation_parsing(
            # """
                # SELECT gaia.source_id, gaia.hip,
                       # gaia.phot_g_mean_mag + 5 * log10(gaia.parallax) - 10
                       # AS g_mag_abs,
                       # hip.b_v
                # FROM gdr1.tgas_source AS gaia
                # INNER JOIN public.hipparcos AS hip
                # ON gaia.hip = hip.hip
                # WHERE gaia.parallax / gaia.parallax_error >= 5
                # AND hip.e_b_v > 0.0 AND hip.e_b_v <= 0.05
                # AND 2.5 / log(10) * gaia.phot_g_mean_flux_error /
                    # gaia.phot_g_mean_flux <= 0.05
            # """,
            # ('gdr1.tgas_source.source_id',
             # 'gdr1.tgas_source.hip',
             # 'gdr1.tgas_source.parallax',
             # 'gdr1.tgas_source.parallax_error',
             # 'gdr1.tgas_source.phot_g_mean_mag',
             # 'gdr1.tgas_source.phot_g_mean_flux_error',
             # 'gdr1.tgas_source.phot_g_mean_flux',
             # 'public.hipparcos.hip',
             # 'public.hipparcos.b_v',
             # 'public.hipparcos.e_b_v'),
            # ('where', 'join'),
            # ('LOG', 'log'),
            # (('public', 'hipparcos'), ('gdr1', 'tgas_source')),
            # ('source_id: gdr1.tgas_source.source_id',
             # 'hip: gdr1.tgas_source.hip',
             # 'b_v: public.hipparcos.b_v',
             # )
        # )

    # def test_query210(self):
        # self._test_adql_postgresql_translation_parsing(
            # """
                # SELECT *
                # FROM "gdr2"."gaia_source"
                # WHERE CONTAINS(POINT('ICRS',"gdr2"."gaia_source"."ra",
                                            # "gdr2"."gaia_source"."dec"),
                               # CIRCLE('ICRS',290.667,44.5,15))=1;
            # """,
            # ('gdr2.gaia_source.*',),
            # ('where', '*'),
            # ('spoint', 'scircle', 'RADIANS'),
            # (('gdr2', 'gaia_source'),),
            # ()
        # )

    # def test_query211(self):
        # self._test_adql_postgresql_translation_parsing(
            # """
                # SELECT id 
                # FROM db.tab1
                # JOIN db.tab2 USING (id);
            # """,
            # ('db.tab1.id', 'db.tab2.id'),
            # ('join', ),
            # (),
            # (('db', 'tab1'), ('db', 'tab2')),
            # ('id: db.tab1.id',)
        # )

    # def test_query212(self):
        # self._test_adql_postgresql_translation_parsing(
            # """
            # SELECT gaia.source_id, gaia.ra, gaia.dec, gd.r_est
            # FROM gdr2.gaia_source gaia, gdr2_contrib.geometric_distance gd
            # WHERE 1 = CONTAINS(POINT('ICRS', gaia.ra, gaia.dec), 
                                       # CIRCLE('ICRS',245.8962, -26.5222, 0.5))
            # AND gaia.phot_g_mean_mag < 15
            # AND gaia.source_id = gd.source_id
            # """,
            # ('gdr2.gaia_source.ra', 'gdr2.gaia_source.dec',
             # 'gdr2.gaia_source.source_id', 'gdr2.gaia_source.phot_g_mean_mag',
             # 'gdr2.gaia_source.pos',
             # 'gdr2_contrib.geometric_distance.source_id',
             # 'gdr2_contrib.geometric_distance.r_est'),
            # ('where',),
            # ('spoint', 'scircle', 'RADIANS'),
            # (('gdr2', 'gaia_source'), ('gdr2_contrib', 'geometric_distance')),
            # ('ra: gdr2.gaia_source.ra', 'dec: gdr2.gaia_source.dec',
             # 'source_id: gdr2.gaia_source.source_id', 
             # 'r_est: gdr2_contrib.geometric_distance.r_est'),
            # {'spoint': ((('gdr2', 'gaia_source', 'ra'),
                         # ('gdr2', 'gaia_source', 'dec'),
                         # 'pos'),)}
        # )

    # def test_query213(self):
        # self._test_adql_postgresql_translation_parsing(
            # """
            # SELECT column_name FROM TAP_SCHEMA.columns
            # WHERE ucd LIKE '%meta.ref%'
            # """,
            # ('TAP_SCHEMA.columns.column_name', 'TAP_SCHEMA.columns.ucd'),
            # ('where', ),
            # (),
            # (('TAP_SCHEMA', 'columns'),),
            # ('column_name: TAP_SCHEMA.columns.column_name',)
        # )
