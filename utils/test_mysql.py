from queryparser.mysql import MySQLQueryProcessor
import numpy as np


def f3():
    query = """
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
            """
    query = """
        SELECT t1.a, t2.b, t3.c, t4.z
          FROM d.tab t1, `db2`.`tab` t2, foo.tab t3, x.y t4
    """
    qp = MySQLQueryProcessor()
    qp.set_query(query)
    qp.process_query(replace_schema_name={'d': 'foo', 'db2': 'bar', 'foo': 'bas'})

    print(qp.query)
    for i in qp.columns:
        print(i)
    print(qp.keywords)
    print(qp.functions)
    print(qp.display_columns)
    print(qp.tables)

f3()
