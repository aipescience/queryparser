# Changelog

## 0.7.3 (2025-05-30)

- Add tests for failure
- Add psql native functions 'point' and 'polygon'

## 0.7.2 (2025-05-19)

- Feature: accept custom udf names for query processing

## 0.7.1 (2025-05-14)

- Fix adql translation for 'contains' and 'intersects'

## 0.7.0 (2024-05-21)

major overhaul for ADQL 2.1 recommendation 2023-12-15

- COOSYS is not required for the geometry constructors anymore, since it's deprecated
- the geometry constructors return the correct datatype (double precision[])
  and correct units (degrees)
- droped the maintenance/support for the translation from ADQL to MySQL.
- bumped the version of `antlr4-python3-runtime` to 4.13.1
- fixed `BOX` constructor, although it's deprecated in ADQL 2.1
- fixed `CONTAINS` for the case `0=CONTAINS()`
- fixed `INTERSECTS` for the case `0=INTERSECTS()`
- new requirements for the `pg_sphere` extension
  ([pg_sphere](https://github.com/kimakan/pgsphere/tree/aiprdbms16))
- removed not supported optional ADQL functions, such as `CENTROID`, `REGION`, etc.
- replaced `setup.py` by `pyproject.toml` since `python setup.py install` is deprecated

## 0.6.1 (2022-11-17)

- fixed the `ORDER BY` clause for the dot-separated column references

## 0.6.0 (2022-11-04)

- bump the version of `antlr4-python3-runtime` to 4.11.1
- added support for two custom functions - `gaia_healpix_index`, `pdist`
- added support for `DISTINCT ON` , [Issue#11](https://github.com/aipescience/queryparser/issues/11)
- added the `ILIKE` operator
- fix installation of requirements.txt (e.g., the required version of
  antlr4-python3-runtime was overwritten by the most current one)
