all: python2 python3

python2: lib/python2/queryparser/adql/ADQLParser.py lib/python2/queryparser/mysql/MySQLParser.py

python3: lib/python3/queryparser/adql/ADQLParser.py lib/python3/queryparser/mysql/MySQLParser.py

lib/python2/queryparser/adql/ADQLParser.py: src/queryparser/adql/*.g4 src/queryparser/adql/*.py
	python generate.py -l adql -p 2

lib/python2/queryparser/mysql/MySQLParser.py: src/queryparser/mysql/*.g4 src/queryparser/mysql/*.py
	python generate.py -l mysql -p 2

lib/python3/queryparser/adql/ADQLParser.py: src/queryparser/adql/*.g4 src/queryparser/adql/*.py
	python generate.py -l adql -p 3

lib/python3/queryparser/mysql/MySQLParser.py: src/queryparser/mysql/*.g4 src/queryparser/mysql/*.py
	python generate.py -l mysql -p 3

clean:
	rm -r lib

.PHONY: all python2 python3 clean
