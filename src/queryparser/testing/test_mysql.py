from . import TestCase
from queryparser.exceptions import QueryError, QuerySyntaxError


class MysqlTestCase(TestCase):

    def test_query000(self):
        self._test_mysql_parsing(
            """
            SELECT tab.a AS col1 FROM db.tab;
            """,
            ('db.tab.a',),
            (),
            (),
            ('col1: db.tab.a',)
        )

    def test_query001(self):
        self._test_mysql_parsing(
            """
            SELECT t.a FROM db.tab1 as t, db.tab2;
            """,
            ('db.tab1.a',),
            (),
            (),
            ('a: db.tab1.a',)
        )

    def test_query002(self):
        self._test_mysql_parsing(
            """
            SELECT (((((((1+2)*3)/4)^5)%6)&7)>>8) FROM db.tab;
            """,
            (),
            (),
            ()
        )

    def test_query003(self):
        self._test_mysql_parsing(
            """
            SELECT COUNT(*), a*2, b, 100 FROM db.tab;
            """,
            ('db.tab.a', 'db.tab.b'),
            (),
            ('COUNT',),
            ('None: db.tab.None', 'a: db.tab.a', 'b: db.tab.b')
        )

    def test_query004(self):
        self._test_mysql_parsing(
            """
            SELECT ABS(a),AVG(b) FROM db.tab;
            """,
            ('db.tab.a', 'db.tab.b'),
            (),
            ('AVG', 'ABS'),
            ()
        )

    def test_query005(self):
        self._test_mysql_parsing(
            """
            SELECT AVG(((((b & a) << 1) + 1) / a) ^ 4.5) FROM db.tab;
            """,
            ('db.tab.a', 'db.tab.b'),
            (),
            ('AVG',),
            ()
        )

    def test_query006(self):
        self._test_mysql_parsing(
            """
            SELECT A.a,B.* FROM db.tab1 A,db.tab2 AS B LIMIT 10;
            """,
            ('db.tab1.a', 'db.tab2.*'),
            ('limit', '*'),
            (),
            ('a: db.tab1.a', '*: db.tab2.*')
        )

    def test_query007(self):
        self._test_mysql_parsing(
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
            (),
            ('fofid: MDR1.FOF.fofid', 'x: MDR1.FOF.x', 'y: MDR1.FOF.y',
             'z: MDR1.FOF.z', 'vx: MDR1.FOF.vx', 'vy: MDR1.FOF.vy',
             'vz: MDR1.FOF.vz'),
        )

    def test_query008(self):
        self._test_mysql_parsing(
            """
            SELECT article, dealer, price
            FROM world.shop s
            WHERE price=(SELECT MAX(price) FROM universe.shop);
            """,
            ('world.shop.article', 'world.shop.dealer', 'world.shop.price',
             'universe.shop.price'),
            ('where',),
            ('MAX',),
            ('article: world.shop.article', 'dealer: world.shop.dealer',
             'price: world.shop.price')
        )

    def test_query009(self):
        self._test_mysql_parsing(
            """
            SELECT dealer, price
            FROM db.shop s1
            WHERE price=(SELECT MAX(s2.price)
                         FROM db.warehouse s2
                         WHERE s1.article = s2.article
                         AND s1.foo = s2.bar);
            """,
            ('db.shop.article', 'db.shop.dealer', 'db.shop.price',
             'db.warehouse.price', 'db.warehouse.article',
             'db.shop.foo', 'db.warehouse.bar'),
            ('where',),
            ('MAX',),
            ('price: db.shop.price', 'dealer: db.shop.dealer')
        )

    def test_query010(self):
        self._test_mysql_parsing(
            """
            SELECT A.*, B.*
            FROM db1.table1 A
            LEFT JOIN db2.table1 B
            ON A.id = B.id;
            """,
            ('db1.table1.*', 'db2.table1.*'),
            ('join', '*'),
            (),
            ('*: db1.table1.*', '*: db2.table1.*')
        )

    def test_query011(self):
        self._test_mysql_parsing(
            """
            SELECT * FROM mmm.products
            WHERE (price BETWEEN 1.0 AND 2.0)
            AND (quantity BETWEEN 1000 AND 2000);
            """,
            ('mmm.products.*',),
            ('where', '*'),
            (),
            ('*: mmm.products.*',)
        )

    def test_query012(self):
        self._test_mysql_parsing(
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
            (),
            ('fi@1: db.test_table.fi@1', 'fi2: db.test_table.fi2')
        )

    def test_query013(self):
        self._test_mysql_parsing(
            """
            SELECT t.table_name AS tname, t.description AS tdesc,
                   h.column_name AS hcol,
                   j.column_name AS jcol,
                   k.column_name AS kcol
            FROM tap_schema.tabs AS t
            JOIN (
                SELECT table_name, column_name
                FROM tap_schema.cols
                WHERE ucd='phot.mag;em.IR.H'
            ) AS h USING (table_name)
            JOIN (
                SELECT table_name, column_name
                FROM tap_schema.cols
                WHERE ucd='phot.mag;em.IR.J'
            ) AS j USING (table_name)
            JOIN (
                SELECT table_name, column_name
                FROM tap_schema.cols
                WHERE ucd='phot.mag;em.IR.K'
            ) AS k USING (table_name)
            """,
            ('tap_schema.tabs.table_name', 'tap_schema.tabs.description',
             'tap_schema.cols.table_name', 'tap_schema.cols.column_name',
             'tap_schema.cols.ucd'),
            ('join', 'where'),
            (),
            ('tname: tap_schema.tabs.table_name',
             'tdesc: tap_schema.tabs.description',
             'hcol: tap_schema.cols.column_name',
             'jcol: tap_schema.cols.column_name',
             'kcol: tap_schema.cols.column_name')
        )

    def test_query014(self):
        self._test_mysql_parsing(
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
            (),
            ('table_name: tap_schema.tabs.table_name',)
        )

    def test_query015(self):
        self._test_mysql_parsing(
            """
            SELECT s.* FROM db.person p INNER JOIN db.shirt s
            ON s.owner = p.id
            WHERE p.name LIKE 'Lilliana%'
            AND s.color <> 'white';
            """,
            ('db.shirt.*', 'db.person.id', 'db.person.name'),
            ('join', 'where', '*'),
            (),
            ('*: db.shirt.*',)
        )

    def test_query016(self):
        self._test_mysql_parsing(
            """
            SELECT x, y, z, mass
            FROM MDR1.FOF
            GROUP BY snapnum
            ORDER BY mass DESC
            LIMIT 10
            """,
            ('MDR1.FOF.x', 'MDR1.FOF.y', 'MDR1.FOF.z', 'MDR1.FOF.mass',
             'MDR1.FOF.snapnum'),
            ('limit', 'order by', 'group by'),
            (),
            ('x: MDR1.FOF.x', 'y: MDR1.FOF.y', 'z: MDR1.FOF.z',
             'mass: MDR1.FOF.mass'),
        )

    def test_query017(self):
        self._test_mysql_parsing(
            """
            SELECT x, y, z, mass
            FROM MDR1.FOF
            LIMIT 100, 200
            """,
            ('MDR1.FOF.x', 'MDR1.FOF.y', 'MDR1.FOF.z', 'MDR1.FOF.mass'),
            ('limit',),
            (),
            ('x: MDR1.FOF.x', 'y: MDR1.FOF.y', 'z: MDR1.FOF.z',
             'mass: MDR1.FOF.mass'),
        )

    def test_query020(self):
        self._test_mysql_parsing(
            """
            SELECT log10(mass)/sqrt(x) AS logM
            FROM MDR1.FOF
            """,
            ('MDR1.FOF.mass', 'MDR1.FOF.x'),
            (),
            ('log10', 'sqrt'),
            ()
        )

    def test_query021(self):
        self._test_mysql_parsing(
            """
            SELECT log10(ABS(x)) AS log_x
            FROM MDR1.FOF
            """,
            ('MDR1.FOF.x',),
            (),
            ('log10', 'ABS'),
            ('log_x: MDR1.FOF.x',)
        )

    def test_query022(self):
        self._test_mysql_parsing(
            """
            SELECT log10(COUNT(*)), snapnum
            FROM MDR1.FOF
            GROUP BY snapnum
            """,
            ('MDR1.FOF.snapnum',),
            ('group by',),
            ('log10', 'COUNT'),
            ()
        )

    def test_query023(self):
        self._test_mysql_parsing(
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
             'Bolshoi.BDMV.bdmId', 'Bolshoi.BDMV.snapnum',
             'Bolshoi.BDMV.Mvir'),
            ('where', 'order by', 'limit'),
            (),
            ('bdmId: Bolshoi.BDMVProf.bdmId', 'Rbin: Bolshoi.BDMVProf.Rbin',
             'mass: Bolshoi.BDMVProf.mass', 'dens: Bolshoi.BDMVProf.dens')
        )

    def test_query024(self):
        self._test_mysql_parsing(
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
            (),
            ('Mvir: MDPL2.Rockstar.Mvir',
             'diskMassStellar: MDPL2.Galacticus.diskMassStellar',
             'spin: MDPL2.Rockstar.spin')
        )

    def test_query025(self):
        self._test_mysql_parsing(
            """
            SELECT 0.25*(0.5+FLOOR(LOG10(Mvir)/0.25)) AS log_mass,
               COUNT(*) AS num
            FROM MDR1.BDMV
            WHERE snapnum=85
            GROUP BY FLOOR(LOG10(x)/0.25)
            ORDER BY log_mass
            """,
            ('MDR1.BDMV.Mvir', 'MDR1.BDMV.snapnum', 'MDR1.BDMV.x'),
            ('where', 'group by', 'order by'),
            ('COUNT', 'FLOOR', 'LOG10'),
            ('log_mass: MDR1.BDMV.Mvir', 'num: MDR1.BDMV.None')
        )

    def test_query026(self):
        self._test_mysql_parsing(
            """
            SELECT d.snapnum snapnum, d.dens AS dens
            FROM (
                SELECT snapnum, dens FROM Bolshoi.Dens256_z0
            ) AS d
            LIMIT 100
            """,
            ('Bolshoi.Dens256_z0.dens', 'Bolshoi.Dens256_z0.snapnum'),
            ('limit',),
            (),
            ('dens: Bolshoi.Dens256_z0.dens',
             'snapnum: Bolshoi.Dens256_z0.snapnum')
        )

    def test_query027(self):
        self._test_mysql_parsing(
            """
            SELECT d.snapnum AS snapnum, r.zred AS zred, d.dens AS dens
            FROM Bolshoi.Dens256 AS d, Bolshoi.Redshifts AS r
            WHERE d.snapnum=r.snapnum
            AND d.snapnum=36
            LIMIT 100
            """,
            ('Bolshoi.Dens256.dens', 'Bolshoi.Dens256.snapnum',
             'Bolshoi.Redshifts.zred', 'Bolshoi.Redshifts.snapnum'),
            ('limit', 'where'),
            (),
            ('dens: Bolshoi.Dens256.dens', 'snapnum: Bolshoi.Dens256.snapnum',
             'zred: Bolshoi.Redshifts.zred')
        )

    def test_query028(self):
        self._test_mysql_parsing(
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
            (),
            ('dens: Bolshoi.Dens256_z0.dens',
             'snapnum: Bolshoi.Dens256_z0.snapnum',
             'zred: Bolshoi.Redshifts.zred')
        )

    def test_query029(self):
        self._test_mysql_parsing(
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
        )

    def test_query030(self):
        self._test_mysql_parsing(
            """
            SELECT d.snapnum AS snapnum, r.zred AS zred, r.aexp AS aexp
            FROM
                (SELECT DISTINCT snapnum FROM Bolshoi.Dens256_z0) AS d,
                (SELECT DISTINCT snapnum, zred, aexp FROM Bolshoi.Redshifts)
                AS r
            WHERE r.snapnum = d.snapnum
            ORDER BY snapnum
            """,
            ('Bolshoi.Dens256_z0.snapnum', 'Bolshoi.Redshifts.aexp',
             'Bolshoi.Redshifts.zred', 'Bolshoi.Redshifts.snapnum'),
            ('order by', 'where'),
            (),
            ('snapnum: Bolshoi.Dens256_z0.snapnum',
             'aexp: Bolshoi.Redshifts.aexp', 'zred: Bolshoi.Redshifts.zred')
        )

    def test_query031(self):
        self._test_mysql_parsing(
            """
            SELECT d.dens, h.bdmId, h.x, h.y, h.z, h.Mvir, h.Rvir, h.hostFlag
            FROM MDR1.Dens512_z0 d, MDR1.BDMV h
            WHERE d.dens<1 AND h.snapnum=85 AND h.Mvir>1.e12
            AND h.phkey/8. = d.phkey
            ORDER BY d.dens
            """,
            ('MDR1.BDMV.Mvir', 'MDR1.BDMV.snapnum', 'MDR1.BDMV.x',
             'MDR1.BDMV.Rvir', 'MDR1.BDMV.phkey', 'MDR1.BDMV.y', 'MDR1.BDMV.z',
             'MDR1.BDMV.bdmId', 'MDR1.BDMV.hostFlag', 'MDR1.Dens512_z0.dens',
             'MDR1.Dens512_z0.phkey'),
            ('order by', 'where'),
            (),
            ('Mvir: MDR1.BDMV.Mvir', 'x: MDR1.BDMV.x', 'Rvir: MDR1.BDMV.Rvir',
             'y: MDR1.BDMV.y', 'z: MDR1.BDMV.z', 'bdmId: MDR1.BDMV.bdmId',
             'hostFlag: MDR1.BDMV.hostFlag', 'dens: MDR1.Dens512_z0.dens')
        )

    def test_query032(self):
        self._test_mysql_parsing(
            """
            SELECT x, y, mass
            FROM MDR1.FOF
            WHERE snapnum <= 1
            """,
            ('MDR1.FOF.x', 'MDR1.FOF.y', 'MDR1.FOF.snapnum', 'MDR1.FOF.mass'),
            ('where',),
            (),
            ('x: MDR1.FOF.x', 'y: MDR1.FOF.y', 'mass: MDR1.FOF.mass'),
        )

    def test_query033(self):
        self._test_mysql_parsing(
            """
            # This query demonstrates how the comments are ignored
            SELECT bdmId, Rbin, mass, dens FROM Bolshoi.BDMVProf
            WHERE bdmId =
                (SELECT bdmId FROM Bolshoi.BDMV
                 WHERE snapnum=416 ORDER BY Mvir DESC LIMIT 1)
            OR
                  bdmId =
                (SELECT bdmId FROM Bolshoi.BDMV
                 WHERE bdmId =
                          # another subquery
                         (SELECT bdmId FROM Bolshoi.BDMV #comment
                          WHERE snapnum=416 ORDER BY Mvir DESC LIMIT 1)
                       OR
                       #comment
                       bdmId =
                         (SELECT bdmId FROM Bolshoi.BDMV
                          WHERE snapnum=STD(Mvir))
                )
            ORDER BY Rbin
            """,
            ('Bolshoi.BDMVProf.bdmId', 'Bolshoi.BDMVProf.Rbin',
             'Bolshoi.BDMVProf.mass', 'Bolshoi.BDMVProf.dens',
             'Bolshoi.BDMV.bdmId', 'Bolshoi.BDMV.snapnum',
             'Bolshoi.BDMV.Mvir'),
            ('where', 'order by', 'limit'),
            ('STD',),
            ('bdmId: Bolshoi.BDMVProf.bdmId', 'Rbin: Bolshoi.BDMVProf.Rbin',
             'mass: Bolshoi.BDMVProf.mass', 'dens: Bolshoi.BDMVProf.dens')
        )

    def test_query034(self):
        self._test_mysql_parsing(
            """
            SELECT DEGREES(sdist(spoint(RADIANS(0.0), RADIANS(0.0)),
                                 spoint(RADIANS(`VII/233/xsc`.`RAJ2000`),
                                 RADIANS(`VII/233/xsc`.`DEJ2000`))))
            FROM `db`.`VII/233/xsc` LIMIT 10;
            """,
            ('db.VII/233/xsc.DEJ2000', 'db.VII/233/xsc.RAJ2000'),
            ('limit',),
            ('DEGREES', 'RADIANS', 'sdist', 'spoint'),
            ()
        )

    def test_query035(self):
        self._test_mysql_parsing(
            """
            SELECT Data FROM db.Users
            WHERE Name ="" or ""="" AND Pass ="" or ""=""
            """,
            ('db.Users.Data', 'db.Users.Name', 'db.Users.Pass'),
            ('where',),
            (),
            ('Data: db.Users.Data',)
        )

    def test_query036(self):
        self._test_mysql_parsing(
            """
            SELECT CONVERT(`ra`,DECIMAL(12,9)) as ra2, `ra` as ra1
            FROM GDR1.gaia_source
            WHERE `dec` BETWEEN 51 AND 51.5
            AND `ra` BETWEEN 126.25 AND 127.25
            """,
            ('GDR1.gaia_source.ra', 'GDR1.gaia_source.dec'),
            ('where',),
            (),
            ('ra1: GDR1.gaia_source.ra', 'ra2: GDR1.gaia_source.ra')
        )

    def test_query037(self):
        self._test_mysql_parsing(
            """
            SELECT t.RAVE_OBS_ID AS c1, t.HEALPix AS c2,
                   h.`logg_SC` AS c3, h.`TEFF` AS c4
            FROM `RAVEPUB_DR5`.`RAVE_DR5` AS t
            JOIN (
                SELECT `RAVE_OBS_ID`, `logg_SC`, k.`TEFF`
                FROM `RAVEPUB_DR5`.`RAVE_Gravity_SC`
                JOIN (
                    SELECT `RAVE_OBS_ID`, `TEFF`
                    FROM `RAVEPUB_DR5`.`RAVE_ON`
                    LIMIT 1000
                ) AS k USING (`RAVE_OBS_ID`)
            ) AS h USING (`RAVE_OBS_ID`)
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
             'c4: RAVEPUB_DR5.RAVE_ON.TEFF')
        )

    def test_query038(self):
        self._test_mysql_parsing(
            """
            SELECT DEGREES(sdist(spoint(RADIANS(`ra`), RADIANS(`dec`)),
                             spoint(RADIANS(266.41683), RADIANS(-29.00781))))
            AS dist
            FROM `GDR1`.`gaia_source`
            WHERE 1 = srcontainsl(spoint(RADIANS(`ra`), RADIANS(`dec`)),
                                  scircle(spoint(RADIANS(266.41683),
                                                 RADIANS(-29.00781)),
                                          RADIANS(0.08333333)))
            ORDER BY `dist` ASC
            """,
            ('GDR1.gaia_source.ra', 'GDR1.gaia_source.dec'),
            ('where', 'order by'),
            ('sdist', 'scircle', 'RADIANS', 'spoint', 'srcontainsl', 'DEGREES')
        )

    def test_query039(self):
        self._test_mysql_parsing(
            """
            SELECT db.tab.a FROM db.tab;
            """,
            ('db.tab.a',),
            (),
            (),
            ('a: db.tab.a',)
        )

    def test_query040(self):
        self._test_mysql_parsing(
            """
            SELECT `db`.`tab`.* FROM `db`.`tab`;
            """,
            ('db.tab.*',),
            ('*'),
            (),
            ('*: db.tab.*',)
        )

    def test_query041(self):
        self._test_mysql_parsing(
            """
            SELECT * FROM db.A
            JOIN (
                SELECT * FROM db.B
            ) AS sub USING(id)
            """,
            ('db.A.*', 'db.B.*'),
            (),
            (),
            ('*: db.A.*',)
        )

    def test_syntax_error(self):
        q = """SELECR a FROM db.tab;"""
        with self.assertRaises(QuerySyntaxError):
            self._test_mysql_parsing(q)

    def test_query_error_001(self):
        q = """SELECT a FROM db.tab1, db.tab2"""
        with self.assertRaises(QueryError):
            self._test_mysql_parsing(q)

    def test_query_error_002(self):
        q = """SELECT a FROM db.tab1
               JOIN (
                   SELECT ra, dec
                   FROM db.tab2
               ) AS sub USING (b)"""
        with self.assertRaises(QueryError):
            self._test_mysql_parsing(q)

    def test_query_error_003(self):
        q = """
            SELECT a.b, a.c
            FROM (
                SELECT ra, dec
                FROM db.tab
            ) AS sub
            """
        with self.assertRaises(QueryError):
            self._test_mysql_parsing(q)

    def test_query_error_004(self):
        q = """
            SELECT a FROM db.tab
            JOIN (
                SELECT a FROM db.foo
            ) AS sub USING(a)
            JOIN (
                SELECT a FROM db.bar
            ) AS sub USING(a)
            """
        with self.assertRaises(QueryError):
            self._test_mysql_parsing(q)
