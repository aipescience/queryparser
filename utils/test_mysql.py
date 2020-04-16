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
            SELECT A.*, B.*
            FROM db1.table1 A
            LEFT JOIN db2.table1 B
            ON A.id = B.id;
    """
    qp = MySQLQueryProcessor()
    qp.set_query(query)
    qp.process_query()

    print(qp.query)
    for i in qp.columns:
        print(i)
    print(qp.display_columns)
    print(qp.tables)
    # print(qp.keywords)
    # print(qp.functions)

f3()
