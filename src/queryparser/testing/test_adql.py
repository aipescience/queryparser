from . import TestCase

class ADQLTestCase(TestCase):

    pass

    # def test_point(self):
    #     self._test_mysql_parsing(
    #         """
    #         SELECT POINT('icrs', 10, 10) FROM b
    #         """,
    #         """

    #         """
    #     )

    # def test_circle(self):
    #     self._test_mysql_parsing(
    #         """
    #         SELECT CIRCLE('ICRS', RA, -20/4., 1) FROM b
    #         """,
    #         """

    #         """
    #     )

# """SELECT BOX('ICRS', 25.4, -20, 1, 1) FROM b""",
# """SELECT TOP 10 AREA(CIRCLE('ICRS', "bla".RA, -20, 1)) FROM b""",
# """SELECT TOP 10 CONTAINS(POINT('ICRS', 0, 0), CIRCLE('ICRS', 0, 0, 1)) FROM b""",
# """SELECT DISTANCE(POINT('ICRS', 0, 0), POINT('ICRS', 0, 1)) FROM b""",
# """SELECT INTERSECTS(CIRCLE('ICRS', 0, 0, 10), BOX('ICRS', 2, 0, 10, 10)) FROM b""",
# """SELECT TOP 10 AREA(CIRCLE('ICRS',  25.4, -20, 1)) FROM b""",
# """SELECT CENTROID(CIRCLE('ICRS', "bla".RA, -20/4., 1)) FROM b""",
# """
# SELECT TOP 10 DISTANCE(POINT('ICRS',0,0), POINT('ICRS',"VII/233/xsc".RAJ2000,"VII/233/xsc".DEJ2000))
# FROM "VII/233/xsc"
# """,
# """
# SELECT *
# FROM "II/246/out"
# WHERE 1=CONTAINS(POINT('ICRS',"II/246/out".RAJ2000,"II/246/out".DEJ2000), CIRCLE('ICRS',0,0, 10/60))
# """,
# """
# SELECT *
# FROM "II/295/SSTGC","II/293/glimpse"
# WHERE 1=CONTAINS(POINT('ICRS',"II/295/SSTGC".RAJ2000,"II/295/SSTGC".DEJ2000), BOX('GALACTIC', 0, 0, 30/60., 10/60.)) 
#   AND 1=CONTAINS(POINT('ICRS',"II/295/SSTGC".RAJ2000,"II/295/SSTGC".DEJ2000), CIRCLE('ICRS',"II/293/glimpse".RAJ2000,"II/293/glimpse".DEJ2000, 2/3600.))
# """,
# """
# SELECT RA,DE FROM "tycho2"
# WHERE 1=CONTAINS(POINT('ICRS', "tycho2".RA, "tycho2".DE), CIRCLE('ICRS', 75.35, -69.7, 10))
# """,
# """
# SELECT TOP 1 source_id, ra, dec, DISTANCE(POINT('ICRS',ra,dec), 
#        POINT('ICRS',266.41683,-29.00781)) AS dist
#    FROM GDR1.gaia_source 
#    WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',266.41683,-29.00781, 0.08333333))
# """,
# """SELECT polygon('ICRS', 0, 0, 0, 1, 1, 1, 1, 0) FROM b""",
# """SELECT a FROM a limit 10"""
