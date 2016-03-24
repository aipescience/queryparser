import sys
import antlr4
from antlr4.error.ErrorListener import ErrorListener
from MySQLLexer import MySQLLexer
from MySQLParser import MySQLParser
from MySQLParserListener import MySQLParserListener


def parse_alias(alias):
    if alias:
        alias = alias.ID().getText().strip('`')
    return alias


class QueryListener(MySQLParserListener):
    """
    Extract all select_expressions.

    """
    def __init__(self):
        self.select_expressions = []

    def enterSelect_expression(self, ctx:MySQLParser.Select_expressionContext):
        self.select_expressions.append(ctx)


class RemoveSubqueriesListener(MySQLParserListener):
    """
    Remove nested select_expressions.

    """
    def __init__(self, depth):
        self.depth = depth
        self.subquery_aliases = []

    def enterSelect_expression(self, ctx:MySQLParser.Select_expressionContext):
        parent = ctx.parentCtx.parentCtx
        if isinstance(parent, MySQLParser.SubqueryContext) and ctx.depth() >\
                self.depth:
            try:
                alias = parent.parentCtx.alias()
            except AttributeError:
                alias = None
            alias = parse_alias(alias)
            self.subquery_aliases.append(alias)
            print('removing', ctx.getText())
            ctx.parentCtx.removeLastChild()


class ColumnNameListener(MySQLParserListener):
    def __init__(self):
        self.column_name = None

    def enterColumn_spec(self, ctx:MySQLParser.Column_specContext):
        self.column_name = ctx.getText()


class SelectExpressionListener(MySQLParserListener):
    """
    Extract table_names, column_names, and their aliases.

    """
    def __init__(self):
        self.tables = []
        self.columns = []
        self.column_name_listener = ColumnNameListener()
        self.walker = antlr4.ParseTreeWalker()

    def enterTable_atom(self, ctx:MySQLParser.Table_atomContext):
        alias = parse_alias(ctx.alias())
        ts = ctx.table_spec()
        if ts:
            self.tables.append((ts.getText().replace('`',''), alias))

    def enterDisplayed_column(self, ctx:MySQLParser.Displayed_columnContext):
        try:
            alias = ctx.alias()
        except AttributeError:
            alias = None
        alias = parse_alias(alias)

        cn = ctx.getText()
        self.column_name_listener.column_name = None
        self.walker.walk(self.column_name_listener, ctx)
        if self.column_name_listener.column_name:
            cn = self.column_name_listener.column_name.replace('`', '')
        else:
            cn = ctx.getText()
        self.columns.append((cn, alias))


class MyErrorListener(ErrorListener):
    def __init__(self):
        super(MyErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception("syntax: %s" % (offendingSymbol))

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact,
                        ambigAlts, configs):
        raise Exception("ambiguity")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex,
                                    stopIndex, conflictingAlts, configs):
        raise Exception("fullcontext: %d:%d" % (startIndex, stopIndex))

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex,
                                 prediction, configs):
        raise Exception("sensitivity")


def main(argv):
    input = antlr4.FileStream(argv[1])
    lexer = MySQLLexer(input)
    stream = antlr4.CommonTokenStream(lexer)
    parser = MySQLParser(stream)
    # parser._listeners = [MyErrorListener()]

    try:
        tree = parser.query()
    except:
        raise

    walker = antlr4.ParseTreeWalker()
    query_listener = QueryListener()
    subquery_aliases = []

    walker.walk(query_listener, tree)
    for ctx in query_listener.select_expressions:
        remove_subquieries_listener = RemoveSubqueriesListener(ctx.depth())
        select_expression_listener = SelectExpressionListener()

        walker.walk(remove_subquieries_listener, ctx)
        subquery_aliases.extend(remove_subquieries_listener.subquery_aliases)

        walker.walk(select_expression_listener, ctx)
        print(select_expression_listener.tables)
        print(select_expression_listener.columns)
        print()

    print(subquery_aliases)


if __name__ == '__main__':
    main(sys.argv)
