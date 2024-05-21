# Development notes

queryparser is a python tool for parsing of MySQL/PostgreSQL SELECT-like queries.
It checks whether the query is syntactically and structurally correct and 
after traversing the query structure extracts all touched columns (even if
they are aliased multiple times), touched tables, along with all used keywords
and functions. These are accessible to the user after the query has been 
processed and can be used to check, for example, for permissions before the
query is sent to the server.

In addition, queryparser can also work with ADQL queries which can be translated
to either MySQL or PostgreSQL language and then further processed the same
way.

Below is a more detailed description along with instructions for anyone who is
interested in further developing the package.

To start, let us first clone the repository:

```bash
git clone git@github.com:aipescience/queryparser.git
```

and then create a virtual environment (inside of which we will install the
package) and activate it:

```bash
python -m venv qpenv
source qpenv/bin/activate
```

After the virtual environment has been activated we can build and install 
the package from the root directory of the package with

```bash
make
python -m pip install .
```

## Testing

All tests from the test suite can be executed with 

```bash
pytest lib/
```

Individual dialect functionality (MySQL in this case) with increased verbosity
can be tested with

```bash
pytest /lib/queryparser/testing/test_mysql.py -v
```

Individual tests (20th MySQL test in this case, but otherwise any test
that includes the string 't20') are ran with

```bash
pytest /lib/queryparser/testing/test_mysql.py -k t20
```

If the package `pytest-cov` is installed then the detailed coverage report
can be generated with

```bash
pytest --cov=queryparser --cov-report html lib
```

Continuous integration is enabled through GitHub Actions. The configuration is 
specified inside of `.github/workflows/pytest.yml` file. Edit as necessary.
Coverage exclusions are defined within  `.coveragerc`.

### Writing new tests

All tests are found in the `tests.yaml` file. This file stores different types
of tests bunched into several groups. During testing the tests are loaded by each of
the testing stacks (MySQL, PostgreSQL and ADQL). To avoid code repetition
pytest's `mark.parametrize` is used to loop over all the elements in
each group. This also allows for an easy reuse of the common tests that
are shared between MySQL and PostgreSQL.

New tests can be easily added to the existing groups of tests and they
will be automatically picked up on the next test run. The structure of each
test group is given at the beginning of the group in the `tests.yaml` file.
Of course, new groups can be added and then employed in the required stack.
If a new type of test is need, it can be defined in the `__init__.py` file
inside of the `testing` directory.

## Grammar development

queryparser's grammar is written in antlr4 language. Each dialect's grammar
stack consist of two files. A lexer that defines the symbols and words (any
combination of characters), including how to handle white-spaces.
The parser defines the rules of the SQL languages. Both files can be edited with any
text editor, however, PyCharm has an integrated antlr functionality and it 
makes development and grammar debugging much easier.

PyCharm offers a plugin for antlr4. It can be installed under File>Settings>Plugins.
Once installed, a right click on any of the rules inside of the parser
grammar file can be tested. A very helpful feature when testing rules this way
is the displayed query tree structure.

With both lexer and parser defined, antlr4 can generate a parser in a few
different languages, including python. Generating parsers for this project
is done easily with the helper script `generate.py` that can be found in
the root directory of the project.

#### Adding new PostgreSQL function

To add a new PostgreSQL function first edit the `PostgreSQLLexer.g4` file and
register the name of the new function. After the name has been added to the
list of known variables and can be recognized by the lexer, the function can
be added to the list under `custom_functions` in the file
`PostgreSQLParser.g4`.

## Processor and translator development

Currently, queryparser package consists of two processors (MySQL and PostgreSQL),
and an ADQL translator. The processors accept any SELECT-like query and
after the process_query() method has been executed, several elements of
the query are extracted (all touch columns and tables, used keywords and functions).
Before the processing the query is validated and invalid queries are rejected.
The ADQL translator allows translating valid ADQL queries to MySQL or PostgreSQL.

Most of the processor code is shared between MySQL and PostgreSQL and is
therefore merged together inside of the `common.py`. This file consists
of several listeners and the main SQLQueryProcessor class that also implements
the ``process_query()`` method.

Individual additions to the common stack for MySQL and PostgreSQL are in
their respective sub-directories.

The main antlr processing object it the `walker` that traverses the whole query
or another context:

```python
walker = antlr4.ParseTreeWalker()
walker.walk(listener, context)
```

Listener is a class with methods that react each time the walker stumbles upon a rule
defined in the parser part of the grammar. For example, if there is method
called `enterAlias()` defined inside of a listener, it will be called once
the walker reaches an `Alias` (as it is defined in the antlr parser file) in a
query or another context.

The main queryparser class that includes this antlr functionality is called
`SQLQueryProcessor`. Besides the helper functions it includes the 
`process_query()` that binds the processing together. MySQL and PostgreSQL
processors inherit from this class and extend it with their own listeners.


## New releases

### Requirements
Install `build` and `twine` with
```bash
pip install twine
pip install build
```
Make sure you have accounts on `https://pypi.org/` and `https://test.pypi.org/`,
and you are `Maintainer` of the `queryparser-python3` project.

 - https://pypi.org/project/queryparser-python3/
 - https://test.pypi.org/project/queryparser-python3/

### Publishing

1. Change the version number in `src/queryparser/__init__.py`
2. `python -m build .`
3. `twine check dist/*`
4. `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
5. Check whether the project was correctly uploaded on `test.pypi.org` by executing
`python3 -m pip install --index-url https://test.pypi.org/simple/ queryparser-python3`
6. `twine upload dist/*`
7. Create a new release on github.
