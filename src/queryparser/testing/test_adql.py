from . import TestCase

class ADQLTestCase(TestCase):

    def test_query000(self):
       self._test_adql_translation(
            """
                SELECT POINT('icrs', 10, 10) FROM db.tab
            """,
            """
                SELECT spoint(RADIANS(10.0), RADIANS(10.0)) FROM `db`.`tab`;
            """
       )

    def test_query001(self):
       self._test_adql_translation(
            """
                SELECT TOP 10 AREA(CIRCLE('ICRS', "tab".RA, -2.23, 176.98)) FROM db.tab
            """,
            """
                SELECT sarea(scircle(spoint(RADIANS(`tab`.`RA`), RADIANS(-2.23)), RADIANS(176.98))) FROM `db`.`tab` LIMIT 10;
            """
       )

    def test_query002(self):
       self._test_adql_translation(
            """
                SELECT BOX('ICRS', 25.4, -20.5, 1.1, 1.2) FROM db.tab
            """,
            """
                SELECT sbox(spoint(RADIANS(25.4),RADIANS(-20.5)),spoint(RADIANS(1.1),RADIANS(1.2))) FROM `db`.`tab`;
            """
       )

    def test_query003(self):
       self._test_adql_translation(
            """
                SELECT TOP 10 CONTAINS(POINT('ICRS', 0, 0), CIRCLE('ICRS', 0, 0, 1)) FROM db.tab
            """,
            """
                SELECT srcontainsl(spoint(RADIANS(0.0), RADIANS(0.0)), scircle(spoint(RADIANS(0.0), RADIANS(0.0)), RADIANS(1.0))) FROM `db`.`tab` LIMIT 10;
            """
       )

    def test_query004(self):
       self._test_adql_translation(
            """
                SELECT DISTANCE(POINT('ICRS', 0, 0), POINT('ICRS', 0, 1)) FROM db.tab
            """,
            """
                SELECT DEGREES(sdist(spoint(RADIANS(0.0), RADIANS(0.0)), spoint(RADIANS(0.0), RADIANS(1.0)))) FROM `db`.`tab`;
            """
       )

    def test_query005(self):
       self._test_adql_translation(
            """
                SELECT INTERSECTS(CIRCLE('ICRS', 0, 0, 10), BOX('ICRS', 2, 0, 10, 10)) FROM db.tab;
            """,
            """
                SELECT soverlaps(scircle(spoint(RADIANS(0.0), RADIANS(0.0)), RADIANS(10.0)), sbox(spoint(RADIANS(2.0),RADIANS(0.0)),spoint(RADIANS(10.0),RADIANS(10.0)))) FROM `db`.`tab`;
            """
       )

    def test_query006(self):
       self._test_adql_translation(
            """
                SELECT CENTROID(CIRCLE('ICRS', "tab".RA, -20/4., 1)) FROM db.tab
            """,
            """
                SELECT scenter(scircle(spoint(RADIANS(`tab`.`RA`), RADIANS(-5.0)), RADIANS(1.0))) FROM `db`.`tab`;
            """
       )

    def test_query020(self):
       self._test_adql_translation(
            """
                SELECT TOP 10 DISTANCE(POINT('ICRS',0,0), POINT('ICRS',"VII/233/xsc".RAJ2000,"VII/233/xsc".DEJ2000))
                FROM db."VII/233/xsc"
            """,
            """
                SELECT DEGREES(sdist(spoint(RADIANS(0.0), RADIANS(0.0)), spoint(RADIANS(`VII/233/xsc`.`RAJ2000`), RADIANS(`VII/233/xsc`.`DEJ2000`)))) FROM `db`.`VII/233/xsc` LIMIT 10;
            """
       )

    def test_query021(self):
       self._test_adql_translation(
            """
                SELECT TOP 1 source_id, ra, dec, DISTANCE(POINT('ICRS',ra,dec), 
                     POINT('ICRS',266.41683,-29.00781)) AS dist
                FROM GDR1.gaia_source 
                WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',266.41683,-29.00781, 0.08333333))
            """,
            """
                SELECT `source_id`, `ra`, `dec`, DEGREES(sdist(spoint(RADIANS(`ra`), RADIANS(`dec`)), spoint(RADIANS(266.41683), RADIANS(-29.00781)))) AS dist FROM `GDR1`.`gaia_source` WHERE 1 = srcontainsl(spoint(RADIANS(`ra`), RADIANS(`dec`)), scircle(spoint(RADIANS(266.41683), RADIANS(-29.00781)), RADIANS(0.08333333))) LIMIT 1;
            """
       )

    def test_query006(self):
       self._test_adql_translation(
            """
                SELECT CENTROID(CIRCLE('ICRS', "tab".RA, -20/4., 1)) FROM db.tab
            """,
            """
                SELECT scenter(scircle(spoint(RADIANS(`tab`.`RA`), RADIANS(-5.0)), RADIANS(1.0))) FROM `db`.`tab`;
            """
       )
