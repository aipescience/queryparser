export CLASSPATH=".:/usr/local/lib/antlr-4.5.2-complete.jar:$CLASSPATH"

all: MySQLLexer.g4 MySQLParser.g4
	java -jar /usr/local/lib/antlr-4.5.2-complete.jar -Dlanguage=Python3 MySQLLexer.g4
	java -jar /usr/local/lib/antlr-4.5.2-complete.jar -Dlanguage=Python3 MySQLParser.g4
