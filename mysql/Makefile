export CLASSPATH=".:/usr/local/lib/antlr-4.5.2-complete.jar:$CLASSPATH"

python: MySQLLexer.g4 MySQLParser.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar -Dlanguage=Python3 MySQLLexer.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar -Dlanguage=Python3 MySQLParser.g4

java: MySQLLexer.g4 MySQLParser.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar MySQLLexer.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar MySQLParser.g4
