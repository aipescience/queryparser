# -*- coding: utf-8 -*-

from queryparser.postgresql import PostgreSQLQueryProcessor
from queryparser.adql import ADQLQueryTranslator
import numpy as np


def test01():
    queries = [
            "SELECT spoint ( 270.0*pi()/180.0,-30.0*pi()/180.0  ) AS sp FROM db.tab;",
            "SELECT strans ( 20.0*pi()/180.0, -270.0*pi()/180.0, 70.5*pi()/180.0, 'XZY' );",
            "SELECT scircle ( spoint (0,0), 30.0*pi()/180.0  );",
            "SELECT sline ( strans (0, 0, 0, 'ZXZ'), 20.0*pi()/180.0  );",
            "SELECT sellipse ( spoint (0, 0), 10.0*pi()/180.0, 5.0*pi()/180.0, pi()/2.0 );",
            "SELECT scircle(spoint(0, 0), 0.1);",
            "SELECT spoly '{ (270d,-10d), (270d,30d), (290d,10d)  } ';",
            "SELECT sbox(spoint(0,0),spoint(1,1));",
            "SELECT count(*) FROM gdr1.gaia_source WHERE pg_sphere_point @ sbox(spoint(0.1,-0.03),spoint(0.11, -0.02));"
            ]

    qp = PostgreSQLQueryProcessor()
    for q in queries:
        qp.set_query(q)
        qp.process_query()

        print(qp.columns)


def f1():
    query = """
        SELECT DISTANCE(
                POINT('ICRS', ra, dec),
                POINT('ICRS', 266.41683, -29.00781)
                ) AS dist
        FROM gaiadr1.gaia_source
        WHERE 1=CONTAINS(
                POINT('ICRS', ra, dec),
                CIRCLE('ICRS', 266.41683, -29.00781, 0.08333333)
                )
        AND x < 1
        OR 1=CONTAINS(
                POINT('ICRS', ra, dec),
                CIRCLE('ICRS', 66.41683, -29.00781, 0.08333333)
                )
        ORDER BY dist ASC
        """

    query = """
    SELECT *
    FROM gdr1.gaia_source
    WHERE 1=CONTAINS(
    POINT('ICRS',ra,dec),
    CIRCLE('ICRS',266.41683,-29.00781, 0.08333333)
            )
            AND phot_g_mean_mag>=10 AND phot_g_mean_mag<15
            ORDER BY phot_g_mean_mag ASC
    """
    query = """
    SELECT gmag * 0.1 AS gmag_bin, COUNT(gmag) AS number
    FROM
    (
        SELECT FLOOR(phot_g_mean_mag * 10) AS gmag
        FROM gdr1.gaia_source
    ) AS gmag_tab
    GROUP BY gmag;
    """
    query = """
    select TOP 50000
    magellan.vmc_source_x_gdr2_gaia_source.nid,
    magellan.vmc_source_x_gdr2_gaia_source.source_id,
    magellan.vmc_source_x_gdr2_gaia_source.dist
    from magellan.vmc_source_x_gdr2_gaia_source,magellan.vmc_source,gdr2.gaia_source
    where gdr2.gaia_source.random_index between 0 and 50000
    AND magellan.vmc_source_x_gdr2_gaia_source.source_id=gdr2.gaia_source.source_id
    AND magellan.vmc_source_x_gdr2_gaia_source.nid=magellan.vmc_source.nid
    AND 1=CONTAINS(POINT('ICRS',gaiadr2.gaia_source.ra,gaiadr2.gaia_source.dec), BOX(‘ICRS GEOCENTER’,35, -73, 10, 10) ) 
    """

    adt = ADQLQueryTranslator(query)
    pgq = adt.to_postgresql()
    print(pgq)
    qp = PostgreSQLQueryProcessor()
    qp.set_query(pgq)
    qp.process_query()
    print(qp.columns)
    print(qp.display_columns)
    print(qp.tables)
    print(qp.functions)


def f2():
    query = """
        SELECT TOP 100 ra, dec
        FROM "gdr1".tgas_source AS tgas
        WHERE 1=CONTAINS( POINT('ICRS', tgas.ra, tgas.dec),
        POLYGON('ICRS', 21.480, -47.354, 21.697,-47.229, 21.914,-47.354,
        21.914,-47.604, 21.697,-47.729, 21.480, -47.604) )
    """
    query = """
    SELECT ra, dec, DISTANCE( POINT('ICRS', gaia.ra, dec),
                              POINT('ICRS', 200, 45)  ) AS dist
    FROM gdr1.gaia_source AS gaia
    WHERE 1 = CONTAINS( POINT('ICRS', ra, dec), CIRCLE('ICRS', 200, 45, 60)  ) 
    """
    query = """
    select gaia.source_id,
    gaia.parallax
    from gdr1.tgas_source as gaia
    where 1=contains(point('ICRS',gaia.ra,gaia.dec),circle('ICRS',56.75,24.12,5))
    and sqrt(power(gaia.pmra-20.5,2)+power(gaia.pmdec+45.5,2)) < 6.0
    """
    query = """
    select t1.source_id,t1.ra, t1.dec, t1."phot_rp_mean_mag", t1.bp_rp, t1.bp_g ,
        t1."radial_velocity" ,t1."teff_val",
            t2."mean_obs_time_g_fov",t2."mean_mag_g_fov",t2."mean_mag_bp",
                t2."time_duration_rp",t2."num_selected_rp"
                FROM "gdr2"."gaia_source" as t1, "gdr2"."vari_time_series_statistics" as t2
                WHERE t1."source_id" = t2."source_id"
                ORDER BY t1.source_id;
            """
    query = """
    SELECT ra, dec FROM gdr2.gaia_source AS g
    WHERE CONTAINS(POINT('ICRS', g.ra, g.dec), BOX('ICRS',35, -74, 1, 1))=1
    """

    adt = ADQLQueryTranslator(query)
    pgq = adt.to_postgresql()
    print(pgq)

    iob = {'spoint': ((('gdr1', 'tgas_source', 'ra'),
                       ('gdr1', 'tgas_source', 'dec'), 'point'),)}
    qp = PostgreSQLQueryProcessor(indexed_objects = {})
    qp.set_query(pgq)
    qp.process_query()

    print(qp.query)


def f3():
    query = """
    SELECT Böning AS a FROM gdr2.gaia_source AS q;
    """
    qp = PostgreSQLQueryProcessor()
    qp.set_query(query)
    qp.process_query()

    print(qp.query)
    print(qp.columns)
    print(qp.display_columns)
    print(qp.tables)
    print(qp.keywords)
    print(qp.functions)

f3()
exit()

alpha = (13 + 26 / 60 + 47.28 / 3600) * 15 - 180
delta = -(47 + 28 / 60 + 46.1 / 3600)
D = 0.5
a = D / 4
b = np.sqrt(3) * a
coords = ((alpha - b, delta + a),
          (alpha, delta + 2 * a),
          (alpha + b, delta + a),
          (alpha + b, delta - a),
          (alpha, delta - 2 * a),
          (alpha - b, delta - a))

print(', '.join(['(%.3fd,%.3fd)' % i for i in coords]))

