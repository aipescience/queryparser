all: python2 python3

python2: lib/python2/queryparser/adql/ADQLParser.py \
         lib/python2/queryparser/adql/adqltranslator.py \
         lib/python2/queryparser/adql/__init__.py \
         lib/python2/queryparser/mysql/MySQLParser.py \
         lib/python2/queryparser/mysql/mysqlprocessor.py \
         lib/python2/queryparser/mysql/__init__.py

python3: lib/python3/queryparser/adql/ADQLParser.py \
         lib/python3/queryparser/adql/adqltranslator.py \
         lib/python3/queryparser/adql/__init__.py \
         lib/python3/queryparser/mysql/MySQLParser.py \
         lib/python3/queryparser/mysql/mysqlprocessor.py \
         lib/python3/queryparser/mysql/__init__.py

lib/python2/queryparser/adql/ADQLParser.py: src/queryparser/adql/*.g4
	python generate.py -l adql -p 2

lib/python2/queryparser/mysql/MySQLParser.py: src/queryparser/mysql/*.g4
	mkdir -p `dirname $@`
	cp $< $@

lib/python2/queryparser/adql/%.py: src/queryparser/adql/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/python2/queryparser/mysql/%.py: src/queryparser/mysql/%.py
	mkdir -p `dirname $@`; cp $< $@

lib/python3/queryparser/adql/ADQLParser.py: src/queryparser/adql/*.g4
	python generate.py -l adql -p 3

lib/python3/queryparser/mysql/MySQLParser.py: src/queryparser/mysql/*.g4
	python generate.py -l mysql -p 3

lib/python3/queryparser/adql/%.py: src/queryparser/adql/%.py
	mkdir -p `dirname $@`
	cp $< $@

lib/python3/queryparser/mysql/%.py: src/queryparser/mysql/%.py
	mkdir -p `dirname $@`
	cp $< $@

clean:
	rm -r lib

.PHONY: all python2 python3 clean
