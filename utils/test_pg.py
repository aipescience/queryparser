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
    query = 'SELECT count(*) FROM gdr1.gaia_source WHERE pg_sphere_point @ sbox(spoint(0.0174533, 0.0174533), spoint(2.0*0.0174533, 2.0*0.0174533));'

    #  adt = ADQLQueryTranslator(query)
    #  pgq = adt.to_postgresql()
    #  print(pgq)
    qp = PostgreSQLQueryProcessor()
    qp.set_query(query)
    qp.process_query()
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

    adt = ADQLQueryTranslator(query)
    #  adt.set_indexed_objects(iob)
    pgq = adt.to_postgresql()
    print(pgq)

    iob = {'spoint': ((('gdr1', 'gaia_source', 'ra'),
                       ('gdr1', 'gaia_source', 'dec'), 'point'),)}
    qp = PostgreSQLQueryProcessor(indexed_objects = iob)
    qp.set_query(pgq)
    qp.process_query()

    print(qp.query)

f2()
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

