# Test if the output of the parser really is what it's suppose to be.
# The parser should spit out all columns being accessed in the shape
#    database.table.column
# and all clauses used.

queries = [
    (
        """
        SELECT a,b FROM db.tab;
        """,
        ('db.tab.a', 'db.tab.b'),
        ()
    ),
    (
        """
        SELECT A.a,B.* FROM db.tab1 A,db.tab2 AS B LIMIT 10;
        """,
        ('db.tab1.a', 'db.tab2.*'),
        ('limit', '*')
    ),
    (
        """
        SELECT fofid, x, y, z, vx, vy, vz
        FROM MDR1.FOF
        WHERE snapnum=85 
        ORDER BY mass DESC
        LIMIT 20
        """,
        ('MDR1.FOF.fofid', 'MDR1.FOF.x', 'MDR1.FOF.y', 'MDR1.FOF.z',
         'MDR1.FOF.vx', 'MDR1.FOF.vy', 'MDR1.FOF.vz', 'MDR1.FOF.snapnum',
         'MDR1.FOF.mass'),
        ('where', 'order by', 'limit')
    ),
    (
        """
        SELECT article, dealer, price
        FROM   world.shop s
        WHERE  price=(SELECT MAX(price) FROM universe.shop);
        """,
        ('world.shop.article', 'world.shop.dealer', 'world.shop.price',
         'universe.shop.price'),
        ('where',)
    ),
    (
        """
        SELECT article, dealer, price
        FROM   db.shop s1
        WHERE  price=(SELECT MAX(s2.price)
                      FROM db.shop s2
                      WHERE s1.article = s2.article);
        """,
        ('db.shop.article','db.shop.dealer', 'db.shop.price'),
        ('where',)
    ),
    (
        """
        SELECT A.*, B.* FROM db1.table1 A LEFT JOIN db2.table1 B
        ON A.id = B.id;
        """,
        ('db1.table1.*', 'db2.table1.*'),
        ('join', '*')
    ),
    (
        """
        SELECT * FROM mmm.products 
        WHERE (price BETWEEN 1.0 AND 2.0) AND
              (quantity BETWEEN 1000 AND 2000);
        """,
        ('mmm.products.*',),
        ('where', '*')
    ),
    (
        """
        SELECT `fi@1`, fi2
            FROM db.test_table WHERE foo = '1'
        UNION
        SELECT fi1, fi2
            FROM bd.test_table WHERE bar = '1';
        """,
        ('db.test_table.fi@1', 'db.test_table.fi2', 'bd.test_table.fi1',
         'bd.test_table.fi2', 'db.test_table.foo', 'bd.test_table.bar'),
        ('where', 'union')
    ),
    (
        """
        SELECT t.table_name AS tname, t.description AS tdesc,
            h.column_name AS hcol,
            j.column_name AS jcol,
            k.column_name AS kcol
        FROM tap_schema.tabs AS t
        JOIN (SELECT table_name, column_name
            FROM tap_schema.cols
            JOIN (SELECT a, b FROM db.tab) AS foo USING (a)
            WHERE ucd='phot.mag;em.IR.H') AS h USING (table_name)
        JOIN (SELECT table_name, column_name
            FROM tap_schema.cols
            WHERE ucd='phot.mag;em.IR.J') AS j USING (table_name)
        JOIN (SELECT table_name, column_name
            FROM tap_schema.cols
            WHERE ucd='phot.mag;em.IR.K') AS k USING (table_name)
        """,
        ('tap_schema.tabs.table_name', 'tap_schema.tabs.description',
         'tap_schema.cols.table_name', 'tap_schema.cols.column_name',
         'tap_schema.cols.ucd', 'db.tab.a', 'db.tab.b',
         'tap_schema.cols.a'),
        ('join', 'where')
    ),
    (
        """
        SELECT DISTINCT t.table_name
        FROM tap_schema.tabs AS t
        JOIN tap_schema.cols AS c USING (table_name)
        WHERE (t.description LIKE '%qso%' OR t.description LIKE '%quasar%')
        AND c.ucd LIKE '%em.X-ray%'
        """,
        ('tap_schema.tabs.table_name', 'tap_schema.cols.table_name',
         'tap_schema.tabs.description', 'tap_schema.cols.ucd'),
        ('join', 'where')
    ),
    (
        """
        SELECT s.* FROM db.person p INNER JOIN db.shirt s
           ON s.owner = p.id
         WHERE p.name LIKE 'Lilliana%'
           AND s.color <> 'white';
        """,
        ('db.shirt.*', 'db.person.id', 'db.person.name'),
        ('join', 'where', '*')
    )
]
