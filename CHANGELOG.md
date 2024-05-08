## 0.7.0 (XXXX-XX-XX)

major overhaul for ADQL 2.1 recommendation 2023-12-15
 - COOSYS is not required for the geometry constructors
 - the geometry constructors return the correct datatype (doube precission[]) 
 and correct units (degrees)
 - drop the maintenance/support for the translation from ADQL to MySQL. 
 - fix `BOX` constructor
 - new requirements for the `pg_sphere` and postgreSQL
 - ...

## 0.6.1 (2022-11-17)

- fixed the `ORDER BY` clause for the dot-separated column references

## 0.6.0 (2022-11-04)

- bump the version of `antlr4-python3-runtime` to 4.11.1
- added support for two custom functions - `gaia_healpix_index`, `pdist`
- added support for `DISTINCT ON` , [Issue#11](https://github.com/aipescience/queryparser/issues/11)
- added the `ILIKE` operator 
- fix installation of requirements.txt (e.g., the required version of 
antlr4-python3-runtime was overwritten by the most current one)

