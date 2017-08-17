from old_test_queries import queries

with open('mysql_queries.py', 'w') as f:

    for i, query in enumerate(queries):
        f.write('''
    def test_query%.3i(self):
        self._test_mysql_parsing(
            """
            %s
            """,
            %s,
            %s,
            %s
        )
''' % (i, query[0].strip(), query[1], query[2], query[3]))
