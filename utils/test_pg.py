from queryparser.postgresql import PostgreSQLQueryProcessor
from queryparser.adql import ADQLQueryTranslator


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
SELECT TOP 10 gaia.ra , distance(
POINT('ICRS', hip.ra, hip.de),
POINT('ICRS', gaia.ra, gaia.dec)
) AS dist
FROM gdr1.gaia_source AS gaia, gdr1.hipparcos AS hip
WHERE 1=CONTAINS(
        POINT('ICRS', hip.ra, hip.de),
        CIRCLE('ICRS', gaia.ra, gaia.dec, 0.000277777777778)

        )
"""

adt = ADQLQueryTranslator(query)
#  adt.set_indexed_objects(iob)
pgq = adt.to_postgresql()

iob = {'spoint': ((('gdr1', 'gaia_source', 'ra'),
                   ('gdr1', 'gaia_source', 'dec'), 'pg_sphere_point'),)}
qp = PostgreSQLQueryProcessor(indexed_objects = iob)
qp.set_query(pgq)
qp.process_query()

print(qp.query)
