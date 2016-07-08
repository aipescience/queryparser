# Queryparser

Let's parse some MySQL and ADQL!

## Requirements

To generate the parsers you need `python` (either 2 or 3), `java` and `antlr4` (which
has to be installed inside the `/usr/local/lib/` or `/usr/local/bin/` directories).

For running the parsers, only runtime libraries that are installed
automatically are needed.

## Instalation

After cloning the project, run

```
python setup.py install
```

This also takes care of installing the required antlr runtime package.

## Parsing

### MySQL

Processing of MySQL queries is done by first creating an instance of the

```python
from queryparser.mysql import MySQLQueryProcessor
qp = MySQLQueryProcessor()
```

feeding it a MySQL query

```python
sql = "SELECT a FROM b;"
qp.set_query(sql)
```

and running it with

```python
qp.process_query()
```

After the processing, the processor object will include columns, functions,
and keywords used in the query.

Alternatively, passing the query at initialization automatically processes it.

### ADQL

Translation of ADQL queries is done similarly by first creating an instance
of the translator object,

```python
from queryparser.adql import ADQLQueryTranslator
adql = "SELECT TOP 100 a,b FROM c"
adt = ADQLQueryTranslator(adql)
```

and calling

```python
adt.to_mysql()
```

which returns a translated string.

### Examples

There are some example queries in the queryparser/examples directory. Have a look there, edit `run.py` (just comment out/uncomment the line you want in `main`) and run it:

```
python queryparser/examples/run.py
```

This will parse a number of queries (specified in the corresponding example-files) and print the query, the parsed columns and the parsing time.

## TODO

* Documentation
* ADQL coordinate systems
* ADQL mixed coordinates
* antlr search path
