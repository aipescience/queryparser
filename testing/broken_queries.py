# -*- coding: utf-8 -*-
queries = [
    (
        """
        SELECr a,b FROM db.tab;
        """,
        ('db.tab.a', 'db.tab.b'),
        (),
        ()
    ),
    (
        """
        SELECT A.a,B.`b@FROM db.tab1 A,db.tab2 B;
        """,
        ('db.tab1.a', 'db.tab2.b'),
        (),
        ()
    ),
    (
        """
        SELECT `fi@1, fi2
            FROM db..test_table WHERE foo = a'1'
        UNION foobar
        SELECT fi1, fi2
            RFOM bd.test_table WHERE bar == '1';
        """,
        ('db.test_table.fi@1', 'db.test_table.fi2', 'bd.test_table.fi1',
         'bd.test_table.fi2', 'db.test_table.foo', 'bd.test_table.bar'),
        ('where', 'union'),
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
                SELECT bdmId FROM Bolshoi.BDMV
                 WHERE bdmId =
                         (SELECT bdmId FROM Bolshoi.BDMV
                          WHERE snapnum=416 ORDER BY Mvir DESC LIMIT 1)
                       OR
                       bdmId = 
                         (SELECT bdmId FROM Bolshoi.BDMV
                          WHERE snapnum=416 ORDER BY Mvir DESC LIMIT 1,2))
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
        SELECT * FROM Users WHERE UserId = 105; DROP TABLE Suppliers
        """,
        (),
        (),
        ()
    )
]
