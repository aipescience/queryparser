export CLASSPATH=".:/usr/local/lib/antlr-4.5.2-complete.jar:$CLASSPATH"

python: ADQLLexer.g4 ADQLParser.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar -visitor -Dlanguage=Python3 ADQLLexer.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar -visitor -Dlanguage=Python3 ADQLParser.g4

java: ADQLLexer.g4 ADQLParser.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar ADQLLexer.g4
	java -jar /usr/local/lib/antlr-4.5.3-complete.jar ADQLParser.g4
