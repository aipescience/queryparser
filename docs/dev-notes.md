## ADQL
#### Missing functions
`CAST` function is not supported at all


## PostgreSQL
#### Missing functions 
Functions that are supported in pg14 but are not processed py the queryparser

###### Mathematical Functions
 - `factorial`
 - `gcd`
 - `lcm`
 - `log10`
 - `min_scale`
 - `truncate` is not supported in pg14 anymore!
 - `trunc`
 - `width_bucket`

###### Random Functions
 - `setseed` - not sure whether this functions must be implemented...

###### Trigonometric Functions
 - `acosd`
 - `asind`
 - `atand`
 - `atan2d`
 - `cosd`
 - `cotd`
 - `sind`
 - `tand`

###### Hyperbolic Functions
 - `sinh`
 - `cosh`
 - `tanh`
 - `asinh`
 - `acosh`
 - `atanh`

###### SQL String Functions and Operators
 - `||`, concatenates two strings, e.g. 'Post' || "greSQL" -> PostgreSQL, if 
 one of the inputs is a non-string, then it's converted to string
 - `IS [NOT] NORMALIZED`, see https://www.postgresql.org/docs/14/functions-string.html
 - `character_length`, same as `char_length`
 - `normalize`
 - `octet_length`
 - `overlay`
 - `position`
 - `trim`

###### Other String Functions
 - `btrim`
 - `format`
 - `initcap`
 - `parse_ident`
 - all `quote_*` functions were not implemented, although already present in pg9
 - all `regex_*` functions were not implemented, although already present in pg9
 - `split_part`
 - `strpos`
 - `starts_with`
 - `string_to_array`
 - `string_to_table`
 - `to_ascii`
 - `unistr`


###### Binary String Functions and Operators
 
