###############################################################################

all: python2 python3

###############################################################################

python2: lib/python2/queryparser

lib/python2/queryparser: \
		lib/python2/queryparser/__init__.py \
		lib/python2/queryparser/adql \
		lib/python2/queryparser/exceptions \
		lib/python2/queryparser/mysql \
		lib/python2/queryparser/postgresql \
		lib/python2/queryparser/testing

lib/python2/queryparser/%.py: src/queryparser/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/python2/queryparser/adql: \
		lib/python2/queryparser/adql/ADQLParser.py \
		lib/python2/queryparser/adql/adqltranslator.py \
		lib/python2/queryparser/adql/__init__.py

lib/python2/queryparser/adql/ADQLParser.py: src/queryparser/adql/*.g4
	python generate.py -l adql -p 2

lib/python2/queryparser/adql/%.py: src/queryparser/adql/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/python2/queryparser/exceptions: \
	lib/python2/queryparser/exceptions/__init__.py

lib/python2/queryparser/exceptions/%.py: src/queryparser/exceptions/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/python2/queryparser/mysql: \
		lib/python2/queryparser/mysql/MySQLParser.py \
		lib/python2/queryparser/mysql/mysqlprocessor.py \
		lib/python2/queryparser/mysql/mysqllisteners.py \
		lib/python2/queryparser/mysql/__init__.py

lib/python2/queryparser/mysql/MySQLParser.py: src/queryparser/mysql/*.g4
	python generate.py -l mysql -p 2

lib/python2/queryparser/mysql/%.py: src/queryparser/mysql/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/python2/queryparser/postgresql: \
		lib/python2/queryparser/postgresql/PostgreSQLParser.py \
		lib/python2/queryparser/postgresql/postgresqlprocessor.py \
		lib/python2/queryparser/postgresql/postgresqllisteners.py \
		lib/python2/queryparser/postgresql/__init__.py

lib/python2/queryparser/postgresql/PostgreSQLParser.py: src/queryparser/postgresql/*.g4
	python generate.py -l postgresql -p 2

lib/python2/queryparser/postgresql/%.py: src/queryparser/postgresql/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/python2/queryparser/testing: \
	lib/python2/queryparser/testing/__init__.py \
	lib/python2/queryparser/testing/test_adql.py \
	lib/python2/queryparser/testing/test_mysql.py \
	lib/python2/queryparser/testing/test_postgresql.py

lib/python2/queryparser/testing/%.py: src/queryparser/testing/%.py
	mkdir -p `dirname $@`
	cp $< $@

###############################################################################

python3: lib/python3/queryparser

lib/python3/queryparser: \
		lib/python3/queryparser/__init__.py \
		lib/python3/queryparser/adql \
		lib/python3/queryparser/exceptions \
		lib/python3/queryparser/mysql \
		lib/python3/queryparser/postgresql \
		lib/python3/queryparser/testing

lib/python3/queryparser/%.py: src/queryparser/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/python3/queryparser/adql: \
		lib/python3/queryparser/adql/ADQLParser.py \
		lib/python3/queryparser/adql/adqltranslator.py \
		lib/python3/queryparser/adql/__init__.py

lib/python3/queryparser/adql/ADQLParser.py: src/queryparser/adql/*.g4
	python generate.py -l adql -p 3

lib/python3/queryparser/adql/%.py: src/queryparser/adql/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/python3/queryparser/exceptions: \
	lib/python3/queryparser/exceptions/__init__.py

lib/python3/queryparser/exceptions/%.py: src/queryparser/exceptions/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/python3/queryparser/mysql: \
		lib/python3/queryparser/mysql/MySQLParser.py \
		lib/python3/queryparser/mysql/mysqlprocessor.py \
		lib/python3/queryparser/mysql/mysqllisteners.py \
		lib/python3/queryparser/mysql/__init__.py

lib/python3/queryparser/mysql/MySQLParser.py: src/queryparser/mysql/*.g4
	python generate.py -l mysql -p 3

lib/python3/queryparser/mysql/%.py: src/queryparser/mysql/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/python3/queryparser/postgresql: \
		lib/python3/queryparser/postgresql/PostgreSQLParser.py \
		lib/python3/queryparser/postgresql/postgresqlprocessor.py \
		lib/python3/queryparser/postgresql/postgresqllisteners.py \
		lib/python3/queryparser/postgresql/__init__.py

lib/python3/queryparser/postgresql/PostgreSQLParser.py: src/queryparser/postgresql/*.g4
	python generate.py -l postgresql -p 3

lib/python3/queryparser/postgresql/%.py: src/queryparser/postgresql/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/python3/queryparser/testing: \
	lib/python3/queryparser/testing/__init__.py \
	lib/python3/queryparser/testing/test_adql.py \
	lib/python3/queryparser/testing/test_mysql.py \
	lib/python3/queryparser/testing/test_postgresql.py

lib/python3/queryparser/testing/%.py: src/queryparser/testing/%.py
	mkdir -p `dirname $@`
	cp $< $@

###############################################################################

clean:
	rm -fr lib

.PHONY: all python2 python3 clean

###############################################################################
