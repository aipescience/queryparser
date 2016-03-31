# Queryparser
Let's parse some MySQL (and ADQL)!

## Generate parser
First the grammar files need to be passed through antlr4 for the
parser to be built. Run
```
$ make python
```
inside the mysql or adql directory. You have to have antrl4 inside the
/usr/local/lib/ directory (get the 4.5.3 version from [here](http://www.antlr.org)).
Alternatively, you can also make the java version and then use PyCharm
with the antlr plugin to parse interactively (watch the parse tree
change as you type):
```
$ make java
```
Get pycharm from [Jetbrains](http://www.jetbrains.com). Once installed, go to
File - Settings - Plugins - Browse Repositories and find the antlr plugin.
Then open the parser grammar file, find the query rule, right click on it and
choose Test Rule query.


## Parsing
To run the parser you have to install the python3 runtime for antlr4
```
$ pip install antlr4-python3-runtime
```
