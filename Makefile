###############################################################################

all: lib/queryparser

lib/queryparser: \
		lib/queryparser/__init__.py \
		lib/queryparser/adql \
		lib/queryparser/common \
		lib/queryparser/exceptions \
		lib/queryparser/mysql \
		lib/queryparser/postgresql \
		lib/queryparser/testing

lib/queryparser/%.py: src/queryparser/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/queryparser/common: \
	lib/queryparser/common/common.py \
	lib/queryparser/common/__init__.py

lib/queryparser/common/%.py: src/queryparser/common/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/queryparser/adql: \
		lib/queryparser/adql/ADQLParser.py \
		lib/queryparser/adql/adqltranslator.py \
		lib/queryparser/adql/__init__.py

lib/queryparser/adql/ADQLParser.py: src/queryparser/adql/*.g4
	python generate.py -l adql

lib/queryparser/adql/%.py: src/queryparser/adql/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/queryparser/exceptions: \
	lib/queryparser/exceptions/__init__.py

lib/queryparser/exceptions/%.py: src/queryparser/exceptions/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/queryparser/mysql: \
		lib/queryparser/mysql/MySQLParser.py \
		lib/queryparser/mysql/mysqlprocessor.py \
		lib/queryparser/mysql/mysqllisteners.py \
		lib/queryparser/mysql/__init__.py

lib/queryparser/mysql/MySQLParser.py: src/queryparser/mysql/*.g4
	python generate.py -l mysql

lib/queryparser/mysql/%.py: src/queryparser/mysql/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/queryparser/postgresql: \
		lib/queryparser/postgresql/PostgreSQLParser.py \
		lib/queryparser/postgresql/postgresqlprocessor.py \
		lib/queryparser/postgresql/postgresqllisteners.py \
		lib/queryparser/postgresql/__init__.py

lib/queryparser/postgresql/PostgreSQLParser.py: src/queryparser/postgresql/*.g4
	python generate.py -l postgresql

lib/queryparser/postgresql/%.py: src/queryparser/postgresql/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/queryparser/testing: \
	lib/queryparser/testing/__init__.py \
	lib/queryparser/testing/test_adql.py \
	lib/queryparser/testing/test_mysql.py \
	lib/queryparser/testing/test_postgresql.py

lib/queryparser/testing/%.py: src/queryparser/testing/%.py
	mkdir -p `dirname $@`
	cp $< $@

###############################################################################

clean:
	rm -fr lib

.PHONY: all clean

###############################################################################
