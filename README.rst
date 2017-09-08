queryparser
===========

**Tool for parsing and processing MySQL and ADQL queries**

Designed to be used in conjunction with `django-daiquri <http://github.com/aipescience/django-daiquiri/>`_
as a query processing backend but it can be easily used as a stand-alone tool or integrated into another project.

.. image:: https://travis-ci.org/aipescience/queryparser.svg?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/aipescience/queryparser

.. image:: https://coveralls.io/repos/github/aipescience/queryparser/badge.svg?branch=master
   :alt: Coverage Status
   :target: https://coveralls.io/github/aipescience/queryparser?branch=master

.. image:: https://img.shields.io/pypi/v/queryparser-python3.svg?style=flat
   :alt: Latest Version
   :target: https://pypi.python.org/pypi/queryparser-python3/

.. image:: http://img.shields.io/badge/license-APACHE-blue.svg?style=flat
    :target: https://github.com/adrn/schwimmbad/blob/master/LICENSE


Parsing MySQL
-------------

Parsing and processing of MySQL queries can be done by creating an instance
of the ``MySQLQueryProcessor`` class

.. code-block:: python

    from queryparser.mysql import MySQLQueryProcessor

    qp = MySQLQueryProcessor()

feeding it a MySQL query

.. code-block:: python

    sql = "SELECT a FROM db.tab;"
    qp.set_query(sql)

and running it with

.. code-block:: python

    qp.process_query()

After the processing, the processor object ``qp`` will include columns,
functions, and keywords used in the query or will raise a ``QuerySyntaxError``
if there are any syntax errors in the query.

Alternatively, passing the query at initialization automatically processes it.


Translating ADQL
----------------

Translation of ADQL queries is done similarly by first creating an instance of the ``ADQLQueryTranslator`` class

.. code-block:: python

    from queryparser.adql import ADQLQueryTranslator

    adql = 'SELECT TOP 100 POINT("ICRS", ra, de) FROM db.tab'
    adt = ADQLQueryTranslator(adql)

and calling

.. code-block:: python

    adt.to_mysql()

which returns a translated string representing a valid MySQL query if
the ADQL query had no errors. The MySQL query can then be parsed with the
``MySQLQueryProcessor`` in the same way as shown above.


Generating the parser from the git repository
---------------------------------------------

To generate the parsers you need `python` (either 2 or 3), `java` above version 7, and `antlr4` (which
has to be installed inside the `/usr/local/lib/` or `/usr/local/bin/` directories).

After cloning the project, run

.. code-block:: bash

    make

and a `lib` directory will be created with the complete source for python2 and python3. After that, run:

.. code-block:: bash

    python setup.py install

to install the generated parser in you virtual env.


Testing
-------

First, install `pytest`

.. code-block:: bash

    pip install pytest

then, run the test suite:

.. code-block:: bash
    
    pytest
