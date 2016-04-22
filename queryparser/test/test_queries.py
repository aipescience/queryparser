# Test if the output of the parser really is what it's suppose to be.
# The parser should spit out all columns being accessed in the shape
#    database.table.column
# and all clauses used.

queries = [
    (
        """
        # blablabla
        SELECT COUNT(*), a*2,b,100 FROM db.tab;
        """,
        ('db.tab.a', 'db.tab.b', 'db.tab.NULL'),
        (),
        ('COUNT',)
    ),
    (
        """
        SELECT a,AVG(b) FROM db.tab;
        """,
        ('db.tab.a', 'db.tab.b'),
        (),
        ('AVG',)
    ),
    (
        """
        SELECT AVG(((((b & a) << 1) + 1) / a) ^ 4.5) FROM db.tab;
        """,
        ('db.tab.a', 'db.tab.b'),
        (),
        ('AVG',)
    ),
    (
        """
        SELECT A.a,B.* FROM db.tab1 A,db.tab2 AS B LIMIT 10;
        """,
        ('db.tab1.a', 'db.tab2.*'),
        ('limit', '*'),
        ()
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
        ('where', 'order by', 'limit'),
        ()
    ),
    (
        """
        SELECT article, dealer, price
        FROM   world.shop s
        WHERE  price=(SELECT MAX(price) FROM universe.shop);
        """,
        ('world.shop.article', 'world.shop.dealer', 'world.shop.price',
         'universe.shop.price'),
        ('where',),
        ('MAX', )
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
        ('where',),
        ('MAX', )
    ),
    (
        """
        SELECT A.*, B.* FROM db1.table1 A LEFT JOIN db2.table1 B
        ON A.id = B.id;
        """,
        ('db1.table1.*', 'db2.table1.*'),
        ('join', '*'),
        ()
    ),
    (
        """
        SELECT * FROM mmm.products 
        WHERE (price BETWEEN 1.0 AND 2.0) AND
              (quantity BETWEEN 1000 AND 2000);
        """,
        ('mmm.products.*',),
        ('where', '*'),
        ()
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
        ('where', 'union'),
        ()
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
        ('join', 'where'),
        ()
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
        ('join', 'where'),
        ()
    ),
    (
        """
        SELECT s.* FROM db.person p INNER JOIN db.shirt s
           ON s.owner = p.id
         WHERE p.name LIKE 'Lilliana%'
           AND s.color <> 'white';
        """,
        ('db.shirt.*', 'db.person.id', 'db.person.name'),
        ('join', 'where', '*'),
        ()
    ),
    (
        """
        SELECT x, y, z, mass 
        FROM MDR1.FOF
        LIMIT 10
        """,
        ('MDR1.FOF.x', 'MDR1.FOF.y', 'MDR1.FOF.z', 'MDR1.FOF.mass'),
        ('limit',),
        ()
    ),
    (
        """
        SELECT x, y, z, mass
        FROM MDR1.FOF
        LIMIT 100,200
        """,
        ('MDR1.FOF.x', 'MDR1.FOF.y', 'MDR1.FOF.z', 'MDR1.FOF.mass'),
        ('limit',),
        ()
    ),
    (
        """
        SELECT x, y, z, mass
        FROM MDR1.FOF
        ORDER BY mass DESC
        LIMIT 10
        """,
        ('MDR1.FOF.x', 'MDR1.FOF.y', 'MDR1.FOF.z', 'MDR1.FOF.mass'),
        ('limit', 'order by'),
        ()
    ),
    (
        """
        SELECT COUNT(*) 
        FROM MDR1.FOF3 
        GROUP BY snapnum
        ORDER BY snapnum
        """,
        ('MDR1.FOF3.snapnum', 'MDR1.FOF3.NULL'),
        ('group by', 'order by'),
        ('COUNT',)
    ),
    (
        """
        SELECT log10(mass)/sqrt(x) AS logM 
        FROM MDR1.FOF
        """,
        ('MDR1.FOF.mass', 'MDR1.FOF.x'),
        (),
        ('log10', 'sqrt')
    ),
    (
        """
        SELECT log10(ABS(x)) AS log_x 
        FROM MDR1.FOF
        """,
        ('MDR1.FOF.x',),
        (),
        ('log10', 'ABS')
    ),
    (
        """
        SELECT log10(COUNT(*)), snapnum
        FROM MDR1.FOF 
        GROUP BY snapnum
        """,
        ('MDR1.FOF.NULL', 'MDR1.FOF.snapnum'),
        ('group by',),
        ('log10', 'COUNT')
    ),
    (
        """
        SELECT bdmId, Rbin, mass, dens FROM Bolshoi.BDMVProf
        WHERE bdmId =
                (SELECT bdmId FROM Bolshoi.BDMV
                 WHERE snapnum=416 ORDER BY Mvir DESC LIMIT 1)
              OR
              bdmId = 
                (SELECT bdmId FROM Bolshoi.BDMV
                 WHERE snapnum=416 ORDER BY Mvir DESC LIMIT 1,2)
        ORDER BY Rbin 
        """,
        ('Bolshoi.BDMVProf.bdmId', 'Bolshoi.BDMVProf.Rbin',
         'Bolshoi.BDMVProf.mass', 'Bolshoi.BDMVProf.dens',
         'Bolshoi.BDMV.bdmId','Bolshoi.BDMV.snapnum','Bolshoi.BDMV.Mvir'),
        ('where', 'order by', 'limit'),
        ()
    ),
    (
            
        """
        SELECT h.Mvir, h.spin, g.diskMassStellar,
               g.diskMassStellar/h.Mvir AS mass_ratio
        FROM MDPL2.Rockstar AS h, MDPL2.Galacticus AS g
        WHERE g.rockstarId = h.rockstarId 
        AND h.snapnum=125 AND g.snapnum=125
        AND h.Mvir>1.e10
        ORDER BY g.diskMassStellar/h.Mvir
        """,
        ('MDPL2.Rockstar.Mvir', 'MDPL2.Galacticus.diskMassStellar',
         'MDPL2.Rockstar.rockstarId', 'MDPL2.Galacticus.rockstarId',
         'MDPL2.Rockstar.snapnum', 'MDPL2.Galacticus.snapnum',
         'MDPL2.Rockstar.spin'),
        ('where', 'order by'),
        ()
    ),
    (
        """
        SELECT 0.25*(0.5+FLOOR(LOG10(Mvir)/0.25)) AS log_mass, COUNT(*) AS num
        FROM MDR1.BDMV
        WHERE snapnum=85 
        GROUP BY FLOOR(LOG10(x)/0.25)
        ORDER BY log_mass
        """,
        ('MDR1.BDMV.Mvir', 'MDR1.BDMV.snapnum', 'MDR1.BDMV.log_mass',
         'MDR1.BDMV.NULL', 'MDR1.BDMV.x'),
        ('where', 'group by', 'order by'),
        ('COUNT', 'FLOOR', 'LOG10')
    ),
    (
        """
        SELECT d.snapnum AS snapnum, d.dens AS dens 
        FROM 
          (SELECT snapnum, dens FROM Bolshoi.Dens256_z0) AS d
        LIMIT 100
        """,
        ('Bolshoi.Dens256_z0.dens', 'Bolshoi.Dens256_z0.snapnum'),
        ('limit', ),
        ()
    ),
    (
        """
        SELECT d.snapnum AS snapnum, r.zred AS zred, d.dens AS dens
        FROM Bolshoi.Dens256 AS d, 
             Bolshoi.Redshifts AS r
        WHERE d.snapnum=r.snapnum
        AND d.snapnum=36
        LIMIT 100
        """,
        ('Bolshoi.Dens256.dens', 'Bolshoi.Dens256.snapnum',
         'Bolshoi.Redshifts.zred', 'Bolshoi.Redshifts.snapnum'),
        ('limit', 'where'),
        ()
    ),
    (
        """
        SELECT d.snapnum AS snapnum, r.zred AS zred, d.dens AS dens
        FROM Bolshoi.Dens256_z0 AS d, 
             (SELECT snapnum, zred FROM Bolshoi.Redshifts) AS r
        WHERE d.snapnum=r.snapnum
        LIMIT 100
        """,
        ('Bolshoi.Dens256_z0.dens', 'Bolshoi.Dens256_z0.snapnum',
         'Bolshoi.Redshifts.zred', 'Bolshoi.Redshifts.snapnum'),
        ('limit', 'where'),
        ()
    ),
    (
        """
        SELECT p.fofTreeId, p.treeSnapnum, p.mass, p.np
        FROM MDR1.FOFMtree AS p, 
        (SELECT fofTreeId, mainLeafId FROM MDR1.FOFMtree 
            WHERE fofId=85000000000) AS mycl
        WHERE p.fofTreeId BETWEEN mycl.fofTreeId AND mycl.mainLeafId
        ORDER BY p.treeSnapnum 
        """,
        ('MDR1.FOFMtree.fofTreeId', 'MDR1.FOFMtree.fofId',
         'MDR1.FOFMtree.mainLeafId', 'MDR1.FOFMtree.mass', 'MDR1.FOFMtree.np',
         'MDR1.FOFMtree.treeSnapnum'),
        ('where', 'order by'),
        ()
    ),
    (
        """
        SELECT d.snapnum AS snapnum, r.zred AS zred, r.aexp AS aexp 
        FROM 
          (SELECT DISTINCT snapnum FROM Bolshoi.Dens256_z0) AS d,
          (SELECT DISTINCT snapnum, zred, aexp FROM Bolshoi.Redshifts) AS r
        WHERE r.snapnum = d.snapnum 
        ORDER BY snapnum
       """,
        ('Bolshoi.Dens256_z0.snapnum', 'Bolshoi.Redshifts.aexp',
         'Bolshoi.Redshifts.zred', 'Bolshoi.Redshifts.snapnum'),
        ('order by', 'where'),
        ()
    ),
    (
       """
        SELECT d.dens,h.bdmId,h.x,h.y,h.z,h.Mvir,h.Rvir,h.hostFlag 
        FROM MDR1.Dens512_z0 d, MDR1.BDMV h
        WHERE d.dens<1 AND h.snapnum=85 AND h.Mvir>1.e12
        AND h.phkey/8. = d.phkey
        ORDER BY d.dens
       """,
        ('MDR1.BDMV.Mvir', 'MDR1.BDMV.snapnum', 'MDR1.BDMV.x',
         'MDR1.BDMV.Rvir', 'MDR1.BDMV.phkey', 'MDR1.BDMV.y', 'MDR1.BDMV.z',
         'MDR1.BDMV.bdmId', 'MDR1.BDMV.hostFlag',
         'MDR1.Dens512_z0.dens', 'MDR1.Dens512_z0.phkey'),
        ('order by', 'where'),
        ()
    ),
    (
        """
        SELECT x, y, mass
        FROM MDR1.FOF
        WHERE snapnum <= 1
        """,
        ('MDR1.FOF.x', 'MDR1.FOF.y', 'MDR1.FOF.snapnum', 'MDR1.FOF.mass'),
        ('where',),
        ()
    ),
    (
        """
        SELECT bdmId, Rbin, mass, dens FROM Bolshoi.BDMVProf
        WHERE bdmId =
                (SELECT bdmId FROM Bolshoi.BDMV
                 WHERE snapnum=416 ORDER BY Mvir DESC LIMIT 1)
              OR
              bdmId = 
                (SELECT bdmId FROM Bolshoi.BDMV
                 WHERE bdmId =
                         (SELECT bdmId FROM Bolshoi.BDMV
                          WHERE snapnum=416 ORDER BY Mvir DESC LIMIT 1)
                       OR
                       bdmId = 
                         (SELECT bdmId FROM Bolshoi.BDMV
                          WHERE snapnum=STD(Mvir))
                )
        ORDER BY Rbin 
        """,
        ('Bolshoi.BDMVProf.bdmId', 'Bolshoi.BDMVProf.Rbin',
         'Bolshoi.BDMVProf.mass', 'Bolshoi.BDMVProf.dens',
         'Bolshoi.BDMV.bdmId','Bolshoi.BDMV.snapnum','Bolshoi.BDMV.Mvir'),
        ('where', 'order by', 'limit'),
        ('STD',)
    ),
]
