# -*- coding: utf-8 -*-

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
            ('db.tab.a', 'db.tab.b', 'db.tab.None'),
            (),
            ('COUNT',),
            ('None: db.tab.None', 'a: db.tab.a', 'b: db.tab.b',
             'None: db.tab.None')
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
            ('MDR1.FOF.snapnum', 'MDR1.FOF.None'),
            ('group by',),
            ('log10', 'COUNT'),
            ('None: MDR1.FOF.None', 'snapnum: MDR1.FOF.snapnum')
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
            ('MDR1.BDMV.Mvir', 'MDR1.BDMV.snapnum', 'MDR1.BDMV.x',
             'MDR1.BDMV.None'),
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
                SELECT sc.`RAVE_OBS_ID`, `logg_SC`, k.`TEFF`
                FROM `RAVEPUB_DR5`.`RAVE_Gravity_SC` sc
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

    def test_query042(self):
        self._test_mysql_parsing(
            """
            SELECT a, b
            FROM (
                SELECT (alpha + beta) AS a, gamma / delta AS b
                FROM db.tab AS foo
                INNER JOIN db.bar AS bas
                ON foo.id = bas.id 
                WHERE zeta > 10
            ) AS sub
            GROUP BY a ASC, b DESC WITH ROLLUP
            """,
            ('db.tab.alpha', 'db.tab.beta', 'db.tab.gamma', 'db.tab.delta',
             'db.tab.zeta', 'db.tab.id', 'db.bar.id'),
            ('group by', 'where', 'join'),
            (),
            ('a: None.None.a', 'b: None.None.b')
        )

    def test_query043(self):
        self._test_mysql_parsing(
            """
            SELECT a, sub.a AS qqq, de, sub.de, bar, sub.bar
            FROM (
                SELECT ra a, de, foo AS bar
                FROM db.tab
                LIMIT 10
            ) AS sub
            """,
            ('db.tab.ra', 'db.tab.de', 'db.tab.foo'),
            ('limit',),
            (),
            ('a: db.tab.ra', 'qqq: db.tab.ra', 'de: db.tab.de',
             'de: db.tab.de', 'bar: db.tab.foo', 'bar: db.tab.foo')
        )

    def test_query044(self):
        self._test_mysql_parsing(
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
        )

    def test_query045(self):
        self._test_mysql_parsing(
            """
            SELECT
            g_min_ks_index / 10 AS g_min_ks,
            g_mag_abs_index / 10 AS g_mag_abs,
            count(*) AS n
            FROM (
                SELECT gaia.source_id,
                floor((gaia.phot_g_mean_mag+5*log10(gaia.parallax)-10) * 10)
                    AS g_mag_abs_index,
                floor((gaia.phot_g_mean_mag-tmass.ks_m) * 10)
                    AS g_min_ks_index
                FROM gaiadr1.tgas_source AS gaia
                INNER JOIN gaiadr1.tmass_best_neighbour AS xmatch
                ON gaia.source_id = xmatch.source_id
                INNER JOIN gaiadr1.tmass_original_valid AS tmass
                ON tmass.tmass_oid = xmatch.tmass_oid
                WHERE gaia.parallax/gaia.parallax_error >= 5 AND
                xmatch.ph_qual = 'AAA' AND
                sqrt(power(2.5 / log(10) * gaia.phot_g_mean_flux_error
                    / gaia.phot_g_mean_flux, 2)) <= 0.05 AND
                sqrt(power(2.5 / log(10) * gaia.phot_g_mean_flux_error
                    / gaia.phot_g_mean_flux, 2)
                + power(tmass.ks_msigcom, 2)) <= 0.05
            ) AS subquery
            GROUP BY g_min_ks_index, g_mag_abs_index
            """,
            ('gaiadr1.tgas_source.source_id',
             'gaiadr1.tgas_source.parallax',
             'gaiadr1.tgas_source.parallax_error',
             'gaiadr1.tgas_source.phot_g_mean_flux',
             'gaiadr1.tgas_source.phot_g_mean_flux_error',
             'gaiadr1.tgas_source.phot_g_mean_mag',
             'gaiadr1.tmass_best_neighbour.ph_qual',
             'gaiadr1.tmass_best_neighbour.source_id',
             'gaiadr1.tmass_best_neighbour.tmass_oid',
             'gaiadr1.tmass_original_valid.ks_m',
             'gaiadr1.tmass_original_valid.ks_msigcom',
             'gaiadr1.tmass_original_valid.tmass_oid',
             ),
            ('where', 'join', 'group by'),
            ('sqrt', 'log10', 'log', 'count', 'floor', 'power'),
            ('g_min_ks: None.None.g_min_ks_index',
             'g_mag_abs: None.None.g_mag_abs_index',
             'n: None.None.None')
        )

    def test_query046(self):
        self._test_mysql_parsing(
            """
            SELECT ra, sub.qqq, t1.bar
            FROM db.tab t1
            JOIN (
                SELECT subsub.col1 AS qqq, subsub.col2, subsub.id, bar 
                FROM (
                    SELECT col1, col2, id, foo AS bar
                    FROM db.blem
                    LIMIT 10
                ) AS subsub
            ) sub USING(id);
            """,
            ('db.blem.col1', 'db.blem.col2', 'db.blem.id', 'db.blem.foo',
             'db.tab.ra', 'db.tab.bar', 'db.tab.id'),
            ('join', 'limit'),
            (),
            (),
        )

    def test_query047(self):
        self._test_mysql_parsing(
            """
            SELECT t1.a, t2.b, t3.c, t4.z
            FROM d.tab t1, `db2`.`tab` t2, foo.tab t3, x.y t4
            """,
            ('foo.tab.a', 'bar.tab.b', 'bas.tab.c', 'x.y.z'),
            (),
            (),
            (),
            replace_schema_name={'d': 'foo', 'db2': 'bar', 'foo': 'bas'}
        )

    def test_query048(self):
        self._test_mysql_parsing(
            """
            SELECT *, AVG(par) as apar
            FROM db.tab;
            """,
            ('db.tab.*',),
            (),
            ('AVG',),
            ('*: db.tab.*', 'apar: db.tab.par'),
        )

    def test_syntax_error_001(self):
        q = """SELECR a FROM db.tab;"""
        with self.assertRaises(QuerySyntaxError):
            self._test_mysql_parsing(q)

    def test_syntax_error_002(self):
        q = """SELECR a, *, b FROM db.tab;"""
        with self.assertRaises(QuerySyntaxError):
            self._test_mysql_parsing(q)

    def test_query_error_001(self):
        q = """SELECT a FROM db.tab1, db.tab2"""
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

    def test_query_error_005(self):
        q = """
            SELECT b
            FROM (
                SELECT a FROM db.tab
            ) AS sub
            """
        with self.assertRaises(QueryError):
            self._test_mysql_parsing(q)

    def test_query_error_006(self):
        q = """
            SELECT sub.b
            FROM (
                SELECT a FROM db.tab
            ) AS sub
            """
        with self.assertRaises(QueryError):
            self._test_mysql_parsing(q)

    def test_query_error_007(self):
        q = """
            SELECT a FROM tab
            """
        with self.assertRaises(QueryError):
            self._test_mysql_parsing(q)

    def test_query_error_008(self):
        q = """
            SELECT a, b FROM db.tab1
            JOIN (
                SELECT id, col AS b FROM db.tab2
            ) AS sub USING(id)
            """
        with self.assertRaises(QueryError):
            self._test_mysql_parsing(q)
