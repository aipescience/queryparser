Development notes
=================

Let us first clone the repository:

```bash
git clone git@github.com:aipescience/queryparser.git
```

and then create a virtual environment inside of which we can install the
package and activate it:

```bash
python -m venv qpenv
source qpenv /bin/activate
```

After the virtual environment has been activated we can install the package
from the root directory of the package with

```bash
pip install -r requirements.txt .
```

Testing
-------

All tests from the test suite can be executed with 

```bash
pytest lib
```

Indivual dialect functionality (MySQL in this case) with increased verbosity
can be tested with

```bash
pytest /lib/queryparser/testing/test_mysql.py -v
```

Individual tests (20th MySQL test in this case) are ran with

```bash
pytest /lib/queryparser/testing/test_mysql.py -k t20
```

Grammar development
-------------------

queryparser's grammar is written in antlr4 language. Each dialect's grammar
consist of a couple of files, a lexer that defines the symbols and words,
and a parser that defines the rules. Both files can be edited with any
text editor, however, PyCharm has an integrated antlr functionality and it 
makes development and grammar debugging much easier.

PyCharm offers a plugin for antlr4 (it can be installed under File>Settings>Plugins).
Once installed, a right click on any of the rules inside of the parser
grammar file can be tested. A very helpful feature when testing rules this way
is the displayed query tree structure.

Processor and translator development
------------------------------------

Currently, queryparser package consists of two processors (MySQL and PostgreSQL),
and an ADQL translator. The processors accept ant SELECT-like query and
after the process_query() method has been executed, several elements of
the query are extracted (all touch columns and tables, used keywords and functions).
Before the processing the query is validated and invalid queries are rejected.
The ADQL translator allows translating valid ADQL queries to MySQL or PostgreSQL.

Most of the processor code is shared between MySQL and PostgreSQL and is
therefore merged together inside of the `common.py`. This file consists
of several listeners and the main SQLQueryProcessor class that also implements
the process_query() method.

Individual additions to the common stack for MySQL and PostgreSQL are in
their respective sub-directories.
