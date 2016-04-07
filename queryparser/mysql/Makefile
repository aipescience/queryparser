export CLASSPATH=".:/usr/local/lib/antlr-4.5.2-complete.jar:$CLASSPATH"

python: MySQLLexer.g4 MySQLParser.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar -Dlanguage=Python3 MySQLLexer.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar -Dlanguage=Python3 MySQLParser.g4

python2: MySQLLexer.g4 MySQLParser.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar -Dlanguage=Python2 MySQLLexer.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar -Dlanguage=Python2 MySQLParser.g4
	mv MySQLLexer.py MySQLLexer2.py
	mv MySQLParser.py MySQLParser2.py
	mv MySQLParserListener.py MySQLParserListener2.py

java: MySQLLexer.g4 MySQLParser.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar MySQLLexer.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar MySQLParser.g4
