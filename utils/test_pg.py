from queryparser.postgresql import PostgreSQLQueryProcessor


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
