# Test if the output of the parser really is what it's suppose to be.
# The parser should spit out all columns being accessed in the shape
#    database.table.column
# and all clauses used.

queries = [
    (
        """
        SELECT a FROM db.tab;
        """,
        ('db.tab.a', 'db.tab.b'),
        ('select', 'from')
    )
]
