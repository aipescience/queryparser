## 0.6.1 (2022-11-17)

- fixed the `ORDER BY` clause for the dot-separated column references

## 0.6.0 (2022-11-04)

- bump the version of `antlr4-python3-runtime` to 4.11.1
- added support for two custom functions - `gaia_healpix_index`, `pdist`
- added support for `DISTINCT ON` , [Issue#11](https://github.com/aipescience/queryparser/issues/11)
- added the `ILIKE` operator 
- fix installation of requirements.txt (e.g., the required version of 
antlr4-python3-runtime was overwritten by the most current one)

