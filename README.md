queryparser
===========

**Tool for parsing and processing of (MySQL\*)/PostgreSQL and translation of
ADQL SELECT-like queries**

Designed to be used in conjunction with [django-daiquri](https://github.com/django-daiquiri/daiquiri)
as a query processing backend but it can be easily used as a stand-alone tool
or integrated into another project.

**\*NOTE: Since version 0.7.0 MySQL is not supported (maintained) anymore.**


[![pytest Workflow Status](https://github.com/aipescience/queryparser/actions/workflows/pytest.yml/badge.svg)](https://github.com/aipescience/queryparser/actions/workflows/pytest.yml)
[![Coverage Status](https://coveralls.io/repos/aipescience/queryparser/badge.svg?branch=master&service=github)](https://coveralls.io/github/aipescience/queryparser?branch=master)
[![License](http://img.shields.io/badge/license-APACHE-blue.svg?style=flat)](https://github.com/aipescience/queryparser/blob/master/LICENSE)
[![Latest Version](https://img.shields.io/pypi/v/queryparser-python3.svg?style=flat)](https://pypi.org/project/queryparser-python3/)



Installation
------------

The easiest way to install the package is by using the pip tool:

```bash
python -m pip install queryparser-python3
```

Alternatively, you can clone the repository and install it from there.
However, this step also requires generating the parser which is a slightly
more elaborate process (see below).


Generating the parser from the git repository
---------------------------------------------

To generate the parsers you need `python3` , `java` above version
7, and `antlr4` (`antlr-4.*-complete.jar` has to be installed inside the
`/usr/local/lib/`, `/usr/local/bin/`  or root directory of the project).

The current version of `antlr-4.*-complete.jar` can be downloaded via

```bash
wget http://www.antlr.org/download/antlr-4.13.1-complete.jar
```

After cloning the project run

```bash
make
```

and a `lib` directory will be created. After that, run

```bash
python -m pip install .
```

to install the generated parser in your virtual environment.


Additional requirements
-----------------------
The queryparser assumes that the PostgreSQL database has the extension
[pg_sphere](https://github.com/kimakan/pgsphere/tree/aiprdbms16) installed.
Although the `pg_sphere` is not required for the python module, the PostgreSQL
**queries will not run** without this extension installed on the database.


Parsing MySQL and PostgreSQL
----------------------------

**Since version 0.7, MySQL part of the parser is not maintained anymore.
Thus, the MySQL related functionality cannot be guaranteed!**

Parsing and processing of MySQL queries can be done by creating an instance
of the `MySQLQueryProcessor` class

```python
from queryparser.mysql import MySQLQueryProcessor
qp = MySQLQueryProcessor()
```

feeding it a MySQL query

```python
sql = "SELECT a FROM db.tab;"
qp.set_query(sql)
```

and running it with

```python
qp.process_query()
```

After the processing is completed, the processor object `qp` will include
tables, columns, functions, and keywords used in the query or will raise a
`QuerySyntaxError` if there are any syntax errors in the query.

Alternatively, passing the query at initialization automatically processes it.

PostgreSQL parsing is very similar to MySQL, except it requires importing
the `PostgreSQLProcessor` class:

```python
from queryparser.postgresql import PostgreSQLQueryProcessor
qp = PostgreSQLQueryProcessor()
```

The rest of the functionality remains the same.


Translating ADQL
----------------

Translation of ADQL queries is done similarly by first creating an instance of
the `ADQLQueryTranslator` class

```python
from queryparser.adql import ADQLQueryTranslator
adql = "SELECT TOP 100 POINT('ICRS', ra, de) FROM db.tab;"
adt = ADQLQueryTranslator(adql)
```

and calling

```python
adt.to_postgresql()
```

which returns a translated string representing a valid MySQL query if
the ADQL query had no errors. The PostgreSQL query can then be parsed with the
`PostgreSQLQueryProcessor` in the same way as shown above.

Testing
-------

First in the root directory of the project, install optional dependencies 
(`PyYAML` and `pytest`) by running

```bash
python -m pip install .[test]
```

then run the test suite with

```bash
python -m pytest lib/
```

