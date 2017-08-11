queryparser
===========

**Let's parse some MySQL and ADQL!**


Parsing MySQL
-------------

Processing of MySQL queries is done by first creating an instance of the ``MySQLQueryProcessor`` class

.. code-block:: python

    from queryparser.mysql import MySQLQueryProcessor

    qp = MySQLQueryProcessor()

feeding it a MySQL query

.. code-block:: python

    sql = "SELECT a FROM b;"
    qp.set_query(sql)

and running it with

.. code-block:: python

    qp.process_query()

After the processing, the processor object will include columns, functions, and keywords used in the query.

Alternatively, passing the query at initialization automatically processes it.


Translating ADQL
----------------

Translation of ADQL queries is done similarly by first creating an instance of the ``ADQLQueryTranslator`` class

.. code-block:: python

    from queryparser.adql import ADQLQueryTranslator

    adql = "SELECT TOP 100 a,b FROM c"
    adt = ADQLQueryTranslator(adql)

and calling

.. code-block:: python

    adt.to_mysql()

which returns a translated string.


Generating the parser from the git repository
---------------------------------------------

To generate the parsers you need `python` (either 2 or 3), `java` above version 7, and `antlr4` (which
has to be installed inside the `/usr/local/lib/` or `/usr/local/bin/` directories).

After cloning the project, run

.. code-block:: bash

    python make.py

and a `lib` directory will be created with the complete source for python2 and python3. After that, run:

.. code-block:: bash

    python setup.py install

to install the generated parser in you virtual env.


Testing
-------

There are some example queries in the ``testing`` directory. Have a look there, edit `run.py` (just comment out/uncomment the line you want in `main`) and run it:

.. code-block:: bash

    python testing/run.py

This will parse a number of queries (specified in the corresponding example-files) and print the query, the parsed columns and the parsing time.


TODO
----

* more Documentation
* ADQL coordinate systems
* ADQL mixed coordinates
