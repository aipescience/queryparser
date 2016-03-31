queries = [
    (
        """
        SELECr a,b FROM db.tab;
        """,
        ('db.tab.a', 'db.tab.b'),
        ()
    ),
    (
        """
        SELECT A.a,B.`b¥` FROM db.tab1 A,db.tab2 B;
        """,
        ('db.tab1.a', 'db.tab2.b'),
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
        ('where', 'union')
    ),
]
