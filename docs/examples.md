# Examples


### A simple PostgreSQL query

```SQL
-- Compute HEALPix value from source_id

SELECT FLOOR(source_id / (POW(2, 35) * POW(4, 6))) AS hpix, radial_velocity AS rv
FROM gdr2.gaia_source
WHERE random_index < 10000000
AND radial_velocity IS NOT NULL;
```

The query is equipped with a comment and it uses a couple of mathematical
functions but is otherwise very straight-forward as it only selects columns
from a single table.

Let us first create the `Processor` object and feed it the above query

```python
qp = PostgreSQLQueryProcessor()
qp.set_query(query)
```

The `query` here can be any multi-line python string. All whitespaces and
line breaks will be ignored.

We run the processing with

```python
qp.process_query()
```

Afterwards, we get

```python
print(qp.columns)
[('gdr2', 'gaia_source', 'source_id'), ('gdr2', 'gaia_source', 'radial_velocity'),
('gdr2', 'gaia_source', 'random_index')]

print(qp.display_columns)
[('hpix', ['gdr2', 'gaia_source', 'source_id']),
('rv', ['gdr2', 'gaia_source', 'radial_velocity'])]

print(qp.tables)
[('gdr2', 'gaia_source')]

print(qp.functions)
['FLOOR', 'POW']

print(qp.keywords)
['where']
```

Besides the touched columns that are stored inside of `qp.columns` we also
get the `display_columns`. These columns are selected (following the SELECT keyword)
and may be aliased which is why it is useful to have a reference to which
exact database column names they are pointing to.


### A more complicated SQL query selecting from multiple tables and having multiple joins

```SQL
SELECT t.RAVE_OBS_ID AS c1, t.HEALPix AS c2,
       h.logg_SC AS c3, h.TEFF AS c4
FROM RAVEPUB_DR5.RAVE_DR5 AS t
JOIN (
    SELECT sc.RAVE_OBS_ID, logg_SC, k.TEFF
    FROM RAVEPUB_DR5.RAVE_Gravity_SC sc
    JOIN (
        SELECT RAVE_OBS_ID, TEFF
        FROM RAVEPUB_DR5.RAVE_ON
        LIMIT 1000
    ) AS k USING (RAVE_OBS_ID)
) AS h USING (RAVE_OBS_ID);
```

When processed using the `MySQLQueryProcessor` or `PostgreSQLQueryProcessor`
it produces the following values

```python
print(qp.columns)
[('RAVEPUB_DR5', 'RAVE_ON', 'TEFF'), ('RAVEPUB_DR5', 'RAVE_DR5', 'HEALPix'),
 ('RAVEPUB_DR5', 'RAVE_Gravity_SC', 'logg_SC'), ('RAVEPUB_DR5', 'RAVE_Gravity_SC', 'RAVE_OBS_ID'),
 ('RAVEPUB_DR5', 'RAVE_DR5', 'RAVE_OBS_ID'), ('RAVEPUB_DR5', 'RAVE_ON', 'RAVE_OBS_ID')]

print(qp.display_columns)
[('c1', ['RAVEPUB_DR5', 'RAVE_DR5', 'RAVE_OBS_ID']),
 ('c2', ['RAVEPUB_DR5', 'RAVE_DR5', 'HEALPix']),
 ('c3', ['RAVEPUB_DR5', 'RAVE_Gravity_SC', 'logg_SC']),
 ('c4', ['RAVEPUB_DR5', 'RAVE_ON', 'TEFF'])]

print(qp.tables)
[('RAVEPUB_DR5', 'RAVE_ON'), ('RAVEPUB_DR5', 'RAVE_DR5'), ('RAVEPUB_DR5', 'RAVE_Gravity_SC')]

print(qp.functions)
[]

print(qp.keywords)
['limit', 'join']
```


### ADQL to PostgreSQL using indexed spoint object

The need indexed objects is explained in the development document. Here we will
demonstrate how to use them.

Let us start with the following ADQL query

```SQL
SELECT gaia.source_id, gaia.ra, gaia.dec, gd.r_est
FROM gdr2.gaia_source gaia, gdr2_contrib.geometric_distance gd
WHERE 1 = CONTAINS(POINT('ICRS', gaia.ra, gaia.dec), 
                   CIRCLE('ICRS',245.8962, -26.5222, 0.5))
AND gaia.phot_g_mean_mag < 15
AND gd.r_est > 1500 AND gd.r_est < 2300
AND gaia.source_id = gd.source_id;
```

We first translate it to PostgreSQL

```python
adt = ADQLQueryTranslator(query)
postgres_query = adt.to_postgresql()
```

which yields

```SQL
SELECT gaia.source_id, gaia.ra, gaia.dec, gd.r_est
FROM gdr2.gaia_source gaia, gdr2_contrib.geometric_distance gd
WHERE spoint(RADIANS(gaia.ra), RADIANS(gaia.dec)) @ scircle(spoint(RADIANS(245.8962), RADIANS(-26.5222)), RADIANS(0.5))
AND gaia.phot_g_mean_mag < 15
AND gd.r_est > 1500 AND gd.r_est < 2300
AND gaia.source_id = gd.source_id;
```

The issue with this query is that the computation of the 

```SQL
spoint(RADIANS(gaia.ra), RADIANS(gaia.dec))
```

can take a very long time if the table we are querying on is large. To avoid
that we can pre-compute its value, however, in that case we need to replace
this `spoint` with the name of the pre-computed column. This can be achieved
by defining the `indexed_objects` dictionary and passing it to the processor.

```python
iob = {'spoint': ((('gdr2', 'gaia_source', 'ra'),
                   ('gdr2', 'gaia_source', 'dec'), 'pos'),)}
qp = PostgreSQLQueryProcessor()
qp.set_query(postgres_query)
qp.process_query(indexed_objects=iob)
```

The `qp.query` string will now give us

```SQL
SELECT gaia.source_id, gaia.ra, gaia.dec, gd.r_est
FROM gdr2.gaia_source gaia, gdr2_contrib.geometric_distance gd
WHERE gaia.pos @ scircle(spoint(RADIANS(245.8962), RADIANS(-26.5222)), RADIANS(0.5))
AND gaia.phot_g_mean_mag < 15
AND gd.r_est > 1500 AND gd.r_est < 2300
AND gaia.source_id = gd.source_id;
```

We see that the `spoint` was replaced with the column `gaia.pos`. Although we
only defined the column as `pos`, we had to attach the alias to it since we
are using this alias for the table in the query. This is done automatically
by the processor.
