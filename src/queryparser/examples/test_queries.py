# Test if the output of the parser really is what it's suppose to be.
# The parser should spit out all columns being accessed in the shape
#    database.table.column
# and all clauses used.

queries = [
    (
        """
        SELECT db.tab.a AS col1 FROM db.tab;
        """,
        ('db.tab.a',),
        (),
        ()
    ),
    (
        """
        SELECT a FROM tab1, tab2;
        """,
        ('tab1.a', 'tab2.a'),
        (),
        ()
    ),
    (
        """
        SELECT (((((((1+2)*3)/4)^5)%6)&7)>>8) FROM tab;
        """,
        ('tab.NULL',),
        (),
        ()
    ),
    (
        """
        SELECT COUNT(*), a*2,b,100 FROM db.tab;
        """,
        ('db.tab.a', 'db.tab.b', 'db.tab.NULL'),
        (),
        ('COUNT',)
    ),
    (
        """
        SELECT ABS(a),AVG(b) FROM db.tab;
        """,
        ('db.tab.a', 'db.tab.b'),
        (),
        ('AVG', 'ABS')
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
        SELECT 0.25*(0.5+FLOOR(LOG10(Mvir)/0.25)) AS log_mass,
               COUNT(*) AS num
        FROM MDR1.BDMV
        WHERE snapnum=85 
        GROUP BY FLOOR(LOG10(x)/0.25)
        ORDER BY log_mass
        """,
        ('MDR1.BDMV.Mvir', 'MDR1.BDMV.snapnum', 'MDR1.BDMV.NULL',
         'MDR1.BDMV.x'),
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
        # This is a shit query but it demonstrates how comments are
        # ignored and that it's possible to parse nested queries in
        # a reasonable amount of time.
        SELECT bdmId, Rbin, mass, dens FROM Bolshoi.BDMVProf
        WHERE bdmId =
                (SELECT bdmId FROM Bolshoi.BDMV
                 WHERE snapnum=416 ORDER BY Mvir DESC LIMIT 1)
              OR
              bdmId = 
                (SELECT bdmId FROM Bolshoi.BDMV
                 WHERE bdmId =
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
         'Bolshoi.BDMV.bdmId','Bolshoi.BDMV.snapnum','Bolshoi.BDMV.Mvir'),
        ('where', 'order by', 'limit'),
        ('STD',)
    ),
    (
        """
        SELECT r.`RAVE_OBS_ID`, r.`RAVEID`, r.`RAdeg`, r.`DEdeg`,
        r.`Glon`, r.`Glat`, r.`HRV`, r.`eHRV`, r.`CorrelationCoeff`,
        r.`PeakHeight`, r.`PeakWidth`, r.`CorrectionRV`, r.`SkyHRV`,
        r.`eSkyHRV`, r.`SkyCorrelationCoeff`, r.`ZeroPointFLAG`,
        r.`STN_SPARV`, r.`ID_TYCHO2`, r.`Dist_TYCHO2`,
        r.`XidQualityFLAG_TYCHO2`, r.`pmRA_TYCHO2`, r.`epmRA_TYCHO2`,
        r.`pmDE_TYCHO2`, r.`epmDE_TYCHO2`, r.`ID_UCAC2`, r.`Dist_UCAC2`,
        r.`XidQualityFLAG_UCAC2`, r.`pmRA_UCAC2`, r.`epmRA_UCAC2`,
        r.`pmDE_UCAC2`, r.`epmDE_UCAC2`, r.`ID_UCAC3`,
        r.`Dist_UCAC3`, r.`XidQualityFLAG_UCAC3`, r.`pmRA_UCAC3`,
        r.`epmRA_UCAC3`, r.`pmDE_UCAC3`, r.`epmDE_UCAC3`, r.`ID_UCAC4`,
        r.`Dist_UCAC4`, r.`XidQualityFLAG_UCAC4`, r.`pmRA_UCAC4`,
        r.`epmRA_UCAC4`, r.`pmDE_UCAC4`, r.`epmDE_UCAC4`, r.`ID_PPMXL`,
        r.`Dist_PPMXL`, r.`XidQualityFLAG_PPMXL`, r.`pmRA_PPMXL`,
        r.`epmRA_PPMXL`, r.`pmDE_PPMXL`, r.`epmDE_PPMXL`, r.`Obsdate`,
        r.`FieldName`, r.`PlateNumber`, r.`FiberNumber`, r.`Teff_K`,
        r.`eTeff_K`, r.`logg_K`, r.`elogg_K`, r.`Met_K`, r.`Met_N_K`,
        r.`eMet_K`, r.`SNR_K`, r.`Algo_Conv_K`, r.`Al`, r.`Al_N`, r.`Si`,
        r.`Si_N`, r.`Fe`, r.`Fe_N`, r.`Ti`, r.`Ti_N`, r.`Ni`, r.`Ni_N`,
        r.`Mg`, r.`Mg_N`, r.`CHISQ_c`, r.`Teff_SPARV`, r.`logg_SPARV`,
        r.`alpha_SPARV`, r.`ID_2MASS`, r.`Dist_2MASS`,
        r.`XidQualityFLAG_2MASS`, r.`Jmag_2MASS`,
        r.`eJmag_2MASS`, r.`Hmag_2MASS`, r.`eHmag_2MASS`, r.`Kmag_2MASS`,
        r.`eKmag_2MASS`, r.`ID_DENIS`, r.`Dist_DENIS`,
        r.`XidQualityFLAG_DENIS`, r.`Imag_DENIS`, r.`eImag_DENIS`,
        r.`Jmag_DENIS`, r.`eJmag_DENIS`, r.`Kmag_DENIS`, r.`eKmag_DENIS`,
        r.`ID_USNOB1`, r.`Dist_USNOB1`, r.`XidQualityFLAG_USNOB1`,
        r.`B1mag_USNOB1`, r.`R1mag_USNOB1`, r.`B2mag_USNOB1`,
        r.`R2mag_USNOB1`,  r.`Imag_USNOB1`, r.`parallax`, r.`e_parallax`,
        r.`dist`, r.`e_dist`, r.`DistanceModulus_Binney`,
        r.`eDistanceModulus_Binney`, r.`Av`, r.`e_Av`, r.`age`, r.`e_age`,
        r.`mass`, r.`e_mass`, r.`c1`, r.`c2`, r.`c3`, r.`c4`, r.`c5`,
        r.`c6`, r.`c7`, r.`c8`, r.`c9`, r.`c10`, r.`c11`, r.`c12`, r.`c13`,
        r.`c14`, r.`c15`, r.`c16`, r.`c17`, r.`c18`, r.`c19`, r.`c20`,
        ra.`B`, ra.`eB` , ra.`V` , ra.`eV` , ra.`g`, ra.`eg` , ra.`r` ,
        ra.`er` , ra.`i` , ra.`ei`
        FROM `RAVE_DR4` r
        JOIN `RAVE_APASS` ra ON (r.`RAVE_OBS_ID` = ra.`RAVE_OBS_ID`);
        """,
        ('RAVE_DR4.XidQualityFLAG_TYCHO2', 'RAVE_DR4.Jmag_2MASS',
         'RAVE_DR4.PeakHeight', 'RAVE_DR4.Si', 'RAVE_DR4.Mg_N',
         'RAVE_DR4.pmDE_TYCHO2', 'RAVE_DR4.eTeff_K', 'RAVE_DR4.Glon',
         'RAVE_DR4.c14', 'RAVE_DR4.c17', 'RAVE_DR4.Obsdate', 'RAVE_DR4.c11',
         'RAVE_DR4.STN_SPARV', 'RAVE_DR4.c13', 'RAVE_DR4.c12', 'RAVE_DR4.c19',
         'RAVE_DR4.c18', 'RAVE_DR4.eMet_K', 'RAVE_DR4.age', 'RAVE_DR4.Fe_N',
         'RAVE_DR4.ZeroPointFLAG', 'RAVE_DR4.pmDE_PPMXL',
         'RAVE_DR4.Dist_2MASS', 'RAVE_DR4.Algo_Conv_K', 'RAVE_DR4.Av',
         'RAVE_DR4.pmDE_UCAC4', 'RAVE_DR4.ID_UCAC2', 'RAVE_DR4.ID_UCAC3',
         'RAVE_DR4.ID_UCAC4', 'RAVE_DR4.XidQualityFLAG_2MASS',
         'RAVE_DR4.pmDE_UCAC3', 'RAVE_DR4.pmDE_UCAC2', 'RAVE_DR4.c9',
         'RAVE_DR4.c8', 'RAVE_DR4.e_dist', 'RAVE_DR4.Met_K',
         'RAVE_DR4.c1', 'RAVE_DR4.c3', 'RAVE_DR4.Al', 'RAVE_DR4.c5',
         'RAVE_DR4.c4', 'RAVE_DR4.c7', 'RAVE_DR4.c6', 'RAVE_DR4.DEdeg',
         'RAVE_DR4.epmRA_PPMXL', 'RAVE_DR4.SNR_K', 'RAVE_DR4.RAVEID',
         'RAVE_DR4.ID_USNOB1', 'RAVE_APASS.RAVE_OBS_ID', 'RAVE_DR4.mass',
         'RAVE_DR4.pmRA_PPMXL', 'RAVE_DR4.e_mass', 'RAVE_DR4.Al_N',
         'RAVE_DR4.eKmag_DENIS', 'RAVE_DR4.Imag_DENIS', 'RAVE_DR4.c15',
         'RAVE_DR4.eJmag_2MASS', 'RAVE_DR4.elogg_K', 'RAVE_DR4.ID_PPMXL',
         'RAVE_DR4.DistanceModulus_Binney', 'RAVE_DR4.Dist_PPMXL',
         'RAVE_DR4.PlateNumber', 'RAVE_DR4.c16',
         'RAVE_DR4.eDistanceModulus_Binney', 'RAVE_DR4.e_parallax',
         'RAVE_DR4.c10', 'RAVE_DR4.c2', 'RAVE_DR4.XidQualityFLAG_DENIS',
         'RAVE_DR4.Dist_UCAC4', 'RAVE_DR4.Dist_UCAC3', 'RAVE_DR4.Dist_UCAC2',
         'RAVE_DR4.logg_SPARV', 'RAVE_DR4.Jmag_DENIS', 'RAVE_DR4.eHRV',
         'RAVE_DR4.Kmag_2MASS', 'RAVE_DR4.pmRA_TYCHO2', 'RAVE_APASS.i',
         'RAVE_DR4.ID_2MASS', 'RAVE_DR4.Dist_USNOB1', 'RAVE_APASS.g',
         'RAVE_DR4.R1mag_USNOB1', 'RAVE_DR4.R2mag_USNOB1', 'RAVE_DR4.Met_N_K',
         'RAVE_APASS.r', 'RAVE_DR4.e_Av', 'RAVE_DR4.Teff_SPARV',
         'RAVE_DR4.Si_N', 'RAVE_DR4.CorrectionRV', 'RAVE_APASS.B',
         'RAVE_DR4.RAVE_OBS_ID', 'RAVE_APASS.V', 'RAVE_DR4.Ti', 'RAVE_DR4.Mg',
         'RAVE_DR4.epmRA_TYCHO2', 'RAVE_DR4.RAdeg', 'RAVE_APASS.eB',
         'RAVE_DR4.epmRA_UCAC4', 'RAVE_DR4.epmRA_UCAC3',
         'RAVE_DR4.epmRA_UCAC2', 'RAVE_DR4.Dist_DENIS', 'RAVE_APASS.eV',
         'RAVE_DR4.CHISQ_c', 'RAVE_APASS.ei', 'RAVE_DR4.Hmag_2MASS',
         'RAVE_DR4.PeakWidth', 'RAVE_APASS.eg', 'RAVE_DR4.c20',
         'RAVE_DR4.XidQualityFLAG_PPMXL', 'RAVE_DR4.Kmag_DENIS', 'RAVE_DR4.Ni',
         'RAVE_DR4.epmDE_PPMXL', 'RAVE_DR4.XidQualityFLAG_USNOB1',
         'RAVE_DR4.ID_DENIS', 'RAVE_APASS.er', 'RAVE_DR4.B1mag_USNOB1',
         'RAVE_DR4.eHmag_2MASS', 'RAVE_DR4.XidQualityFLAG_UCAC4',
         'RAVE_DR4.epmDE_TYCHO2', 'RAVE_DR4.dist', 'RAVE_DR4.eKmag_2MASS',
         'RAVE_DR4.XidQualityFLAG_UCAC3', 'RAVE_DR4.XidQualityFLAG_UCAC2',
         'RAVE_DR4.epmDE_UCAC3', 'RAVE_DR4.epmDE_UCAC2', 'RAVE_DR4.Glat',
         'RAVE_DR4.epmDE_UCAC4', 'RAVE_DR4.Teff_K', 'RAVE_DR4.Imag_USNOB1',
         'RAVE_DR4.B2mag_USNOB1', 'RAVE_DR4.ID_TYCHO2', 'RAVE_DR4.FiberNumber',
         'RAVE_DR4.logg_K', 'RAVE_DR4.SkyCorrelationCoeff',
         'RAVE_DR4.FieldName', 'RAVE_DR4.Fe', 'RAVE_DR4.SkyHRV',
         'RAVE_DR4.e_age', 'RAVE_DR4.Ni_N', 'RAVE_DR4.parallax',
         'RAVE_DR4.Dist_TYCHO2', 'RAVE_DR4.eSkyHRV',
         'RAVE_DR4.CorrelationCoeff', 'RAVE_DR4.pmRA_UCAC4',
         'RAVE_DR4.pmRA_UCAC3', 'RAVE_DR4.pmRA_UCAC2', 'RAVE_DR4.alpha_SPARV',
         'RAVE_DR4.eJmag_DENIS', 'RAVE_DR4.HRV', 'RAVE_DR4.eImag_DENIS',
         'RAVE_DR4.Ti_N'
        ),
        ('join',),
        ()
    ),
    (
        """
        SELECT Data FROM Users WHERE Name ="" or ""="" AND Pass ="" or ""=""
        """,
        ('Users.Data', 'Users.Name', 'Users.Pass'),
        ('where',),
        ()
    ),
    (
        """
        SELECT
            CONVERT(`ra`,DECIMAL(12,9)) as ra2, `ra` as ra1
        FROM 
            GDR1.gaia_source 
        WHERE 
            `dec` BETWEEN 51 AND 51.5 AND 
            `ra` BETWEEN 126.25 AND 127.25
        """,
        ('GDR1.gaia_source.ra', 'GDR1.gaia_source.dec'),
        ('where',),
        ()
    ),
    (
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
        ('RAVEPUB_DR5.RAVE_DR5.RAVE_OBS_ID', 'RAVEPUB_DR5.RAVE_DR5.HEALPix', 
         'RAVEPUB_DR5.RAVE_ON.TEFF', 'RAVEPUB_DR5.RAVE_Gravity_SC.logg_SC',
         'RAVEPUB_DR5.RAVE_ON.RAVE_OBS_ID',
         'RAVEPUB_DR5.RAVE_Gravity_SC.RAVE_OBS_ID'),
        ('join', 'limit'),
        ()
    ),
    (
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
]
