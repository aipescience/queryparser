import sys
import antlr4
from antlr4.error.ErrorListener import ErrorListener
from MySQLLexer import MySQLLexer
from MySQLParser import MySQLParser
from MySQLParserListener import MySQLParserListener

import test_queries
import time


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
            #  print('removing', ctx.getText())
            ctx.parentCtx.removeLastChild()


class ColumnNameListener(MySQLParserListener):
    def __init__(self):
        self.column_name = None

    def enterColumn_spec(self, ctx:MySQLParser.Column_specContext):
        self.column_name = ctx.getText()
        print(self.column_name)


class TableColumnKeywordListener(MySQLParserListener):
    """
    Extract table_names, column_names, and their aliases.

    """
    def __init__(self):
        self.tables = []
        self.columns = []
        self.keywords = []
        self.column_name_listener = ColumnNameListener()
        self.walker = antlr4.ParseTreeWalker()
    
    def _process_column_name(self, ctx):
        cn = ctx.getText()
        self.column_name_listener.column_name = None
        self.walker.walk(self.column_name_listener, ctx)
        if self.column_name_listener.column_name:
            cn = self.column_name_listener.column_name.replace('`', '')
        else:
            cn = ctx.getText()
        return cn

    def _process_alias(self, ctx):
        try:
            alias = ctx.alias()
        except AttributeError:
            alias = None
        alias = parse_alias(alias)
        return alias
    
    def _extract_column(self, ctx):
        cn = self._process_column_name(ctx)
        alias = self._process_alias(ctx)
        self.columns.append((cn, alias))

    def enterTable_atom(self, ctx:MySQLParser.Table_atomContext):
        alias = parse_alias(ctx.alias())
        ts = ctx.table_spec()
        if ts:
            self.tables.append((ts.getText().replace('`',''), alias))

    def enterDisplayed_column(self, ctx:MySQLParser.Displayed_columnContext):
        self._extract_column(ctx)

    def enterWhere_clause(self, ctx:MySQLParser.Where_clauseContext):
        self.keywords.append('where')
        print(ctx.getText())
        self._extract_column(ctx)

    def enterOrderby_clause(self, ctx:MySQLParser.Orderby_clauseContext):
        self.keywords.append('order by')
        self._extract_column(ctx)

    def enterLimit_clause(self, ctx:MySQLParser.Limit_clauseContext):
        self.keywords.append('limit')

    def enterJoin_condition(self, ctx:MySQLParser.Join_conditionContext):
        self.keywords.append('join')
        self._extract_column(ctx)


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


def process_query(query):
    inpt = antlr4.InputStream(query)
    lexer = MySQLLexer(inpt)
    stream = antlr4.CommonTokenStream(lexer)
    parser = MySQLParser(stream)
    # parser._listeners = [MyErrorListener()]

    try:
        tree = parser.query()
        #  print(tree.toStringTree(recog=parser))
    except:
        raise

    walker = antlr4.ParseTreeWalker()
    query_listener = QueryListener()
    subquery_aliases = []
    query_names = []
    keywords = []

    walker.walk(query_listener, tree)

    for ctx in query_listener.select_expressions:
        remove_subquieries_listener = RemoveSubqueriesListener(ctx.depth())
        table_column_keyword_listener= TableColumnKeywordListener()

        # Remove nested subqueries from select_expressions
        walker.walk(remove_subquieries_listener, ctx)
        subquery_aliases.extend(remove_subquieries_listener.subquery_aliases)

        # Extract table and column names and keywords
        walker.walk(table_column_keyword_listener, ctx)

        query_names.append([table_column_keyword_listener.tables,
                            table_column_keyword_listener.columns])
        keywords.extend(table_column_keyword_listener.keywords)

    columns = []
    for qn in query_names:
        tab_dict = {}
        tab = []
        for i in qn[0]:
            if i[1]:
                tab_dict[i[1]] = i[0]
            else:
                tab.append(i[0])
        for i in qn[1]:
            parts = i[0].split('.')

            if len(parts) == 3:
                columns.append(i[0])

            if len(parts) == 2 and parts[0] not in subquery_aliases:
                # we need to replace the table name alias
                try:
                    update = tab_dict[parts[0]]
                    columns.append('%s.%s' % (update, parts[1]))
                except KeyError:
                    pass

            if len(parts) == 1:
                dvs = list(tab_dict.values())
                if len(dvs) > 1 or len(tab) > 1:
                    #  raise Exception("Not sure from which table I am suppose" +\
                            #  " to get the columns... %s" % str(dvs or tab))
                    for k in dvs:
                        columns.append('%s.%s' % (k, parts[0]))
                    for k in tab:
                        columns.append('%s.%s' % (k, parts[0]))

                else:
                    if len(dvs):
                        columns.append('%s.%s' % (dvs[0], parts[0]))
                    else:
                        columns.append('%s.%s' % (tab[0], parts[0]))

    columns = set(columns)
    keywords = set(keywords)
    return columns, keywords


if __name__ == '__main__':
    for q in test_queries.queries[-1:]:
        s = time.time()
        cols, keys = process_query(q[0])
        s = time.time() - s
        for i in cols:
            print(i)
        print(cols.symmetric_difference(q[1]))
        print(keys.symmetric_difference(q[2]))
        print('Done in %.2fs' % s)
        print()
