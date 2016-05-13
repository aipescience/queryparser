# Queryparser
Let's parse some MySQL and ADQL!

## Requirements
To generate the parsers you need python (either 2 or 3), java and antlr4 (which
has to be installed inside the /usr/local/lib/ or /usr/local/bin/ directories). 

## Instalation
After cloning the project, run
```
python setup.py install
```
This also takes care of installing the required antlr runtime package.

## Parsing
Processing of MySQL queries is done by first creating an instance of the
```
qp = MySQLQueryProcessor()
```
feeding it a MySQL query
```
sql = "SELECT a FROM b;"
qp.set_query(sql)
```
and running it
```
qp.process_query()
```
After the processing, the processor object will include columns, functions,
and keywords used in the query.

Alternatively, passing the query at initialization automatically processes it.


Translation of ADQL queries is done similarly by first creating and instance
of the translator object,
```
query = ...
adt = ADQLQueryTranslator(query)
```
and calling
```
adt.to_mysql()
```
which returns a translated string.

## TODO
ADQL coordinate systems
