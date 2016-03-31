import sys
import antlr4
from antlr4.error.ErrorListener import ErrorListener
from MySQLLexer import MySQLLexer
from MySQLParser import MySQLParser
from MySQLParserListener import MySQLParserListener

import test_queries
import broken_queries
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
        self.keywords = []
        
    def enterSelect_statement(self, ctx:MySQLParser.Select_statementContext):
        if ctx.UNION_SYM():
            self.keywords.append('union')

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
        self.column_name = []

    def enterColumn_spec(self, ctx:MySQLParser.Column_specContext):
        self.column_name.append(ctx.getText())


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
        #  cn = [ctx.getText()]
        cn = []
        self.column_name_listener.column_name = []
        self.walker.walk(self.column_name_listener, ctx)
        if self.column_name_listener.column_name:
            for i in self.column_name_listener.column_name:
                cn.append(i.replace('`', ''))
        else:
            cn = [ctx.getText()]
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
        if len(cn) > 1:
            self.columns.extend([(i, None) for i in cn])
        else:
            self.columns.append((cn[0], alias))

    def enterTable_atom(self, ctx:MySQLParser.Table_atomContext):
        alias = parse_alias(ctx.alias())
        ts = ctx.table_spec()
        if ts:
            self.tables.append((ts.getText().replace('`',''), alias))

    def enterDisplayed_column(self, ctx:MySQLParser.Displayed_columnContext):
        self._extract_column(ctx)
        if ctx.ASTERISK():
            self.keywords.append('*')

    def enterSelect_list(self, ctx:MySQLParser.Select_listContext):
        if ctx.ASTERISK():
            self.columns.append(('*', None))
            self.keywords.append('*')

    def enterWhere_clause(self, ctx:MySQLParser.Where_clauseContext):
        self.keywords.append('where')
        self._extract_column(ctx)

    def enterOrderby_clause(self, ctx:MySQLParser.Orderby_clauseContext):
        self.keywords.append('order by')
        self._extract_column(ctx)

    def enterLimit_clause(self, ctx:MySQLParser.Limit_clauseContext):
        self.keywords.append('limit')

    def enterJoin_condition(self, ctx:MySQLParser.Join_conditionContext):
        self.keywords.append('join')
        self._extract_column(ctx)


class SyntaxErrorListener(ErrorListener):
    def __init__(self):
        super(SyntaxErrorListener, self).__init__()
        self.syntax_errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.syntax_errors.append((line, column, offendingSymbol.text))


class QueryProcessor(object):
    def __init__(self, query=None):
        self.columns = set()
        self.keywords = set()
        self.syntax_error_listener = SyntaxErrorListener()
        self.syntax_errors = []
        if query is not None:
            self.query = query
            self.process_query()

    def process_query(self):
        inpt = antlr4.InputStream(self.query)
        lexer = MySQLLexer(inpt)
        stream = antlr4.CommonTokenStream(lexer)
        parser = MySQLParser(stream)
        parser._listeners = [self.syntax_error_listener]

        try:
            tree = parser.query()
        except:
            raise

        walker = antlr4.ParseTreeWalker()
        query_listener = QueryListener()
        subquery_aliases = []
        query_names = []
        keywords = []

        walker.walk(query_listener, tree)
        keywords.extend(query_listener.keywords)

        for ctx in query_listener.select_expressions:
            remove_subquieries_listener = RemoveSubqueriesListener(ctx.depth())
            table_column_keyword_listener= TableColumnKeywordListener()

            # Remove nested subqueries from select_expressions
            walker.walk(remove_subquieries_listener, ctx)
            subquery_aliases.extend(
                    remove_subquieries_listener.subquery_aliases)

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
                        elif len(tab):
                            columns.append('%s.%s' % (tab[0], parts[0]))

        # Let's get rid of all columns that are already covered by
        # db.tab.*. Figure out a better way to do it and replace the code
        # below.
        asterisk_columns = []
        del_columns = []
        for col in columns:
            if col.split('.')[-1] == '*':
                asterisk_columns.append(col)
        for acol in asterisk_columns:
            for col in columns:
                if acol != col and acol.split('.')[:-1] == col.split('.')[:-1]:
                    del_columns.append(col)

        if not len(self.syntax_error_listener.syntax_errors):
            self.columns = set(columns).difference(del_columns)
            self.keywords = set(keywords)
        else:
            self.syntax_errors = self.syntax_error_listener.syntax_errors


def pretty_print(q, columns, keywords, process_time, syntax=None,
                 show_diff=True):

    print('+' + '=' * 78 + '+')
    sq = q[0].split('\n')

    proc = '\033[92m\033[1mDone\033[0m'
    offset = [0] * len(sq)
    if len(syntax):
        for se in syntax:
            rep = "\033[91m\033[1m%s\033[0m" % se[2]
            k = se[0] - 1
            orig = sq[k]
            sq[k] = ((orig[:se[1] + offset[k]] + rep + '\033[100m' +
                      orig[se[1] + len(se[2]) + offset[k]:]))

            proc = '\033[91m\033[1mFailed\033[0m'
            offset[se[0] - 1] += 19

    for k, i in enumerate(sq):
        print('|\033[100m' + i + ' ' * (78 - len(i) + offset[k]) + '\033[49m|')

    if not len(syntax):
        print('|' + ' ' * 78 + '|')
        print('|  Columns:' + ' ' * 68 + '|')
        for i in sorted(columns):
            print('|\t' + i + ' ' * (71 - len(i)) + '|')

        if len(keywords):
            print('|' + ' ' * 78 + '|')
            print('|  Keywords:' + ' ' * 67 + '|')
            for i in sorted(keywords):
                print('|\t' + i + ' ' * (71 - len(i)) + '|')

        print('|' + ' ' * 78 + '|')

        if show_diff:
            if cols.symmetric_difference(q[1]) != set():
                print('|  Missing columns:' + ' ' * 60 + '|')
                for i in cols.symmetric_difference(q[1]):
                    print('|\t' + i + ' ' * (71 - len(i)) + '|')
                print('|' + ' ' * 78 + '|')
                proc = '\033[91m\033[1mFailed\033[0m'
            if keys.symmetric_difference(q[2]) != set():
                print('|  Missing keywords:' + ' ' * 59 + '|')
                for i in keys.symmetric_difference(q[2]):
                    print('|\t' + i + ' ' * (71 - len(i)) + '|')
                print('|' + ' ' * 78 + '|')
                proc = '\033[91m\033[1mFailed\033[0m'
    else:
        print('|' + ' ' * 78 + '|')

    tm = '%s in %.2fs' % (proc, process_time)
    if len(syntax) == 1:
        tm += ' - 1 syntax error'
    elif len(syntax) > 1:
        tm += ' - %d syntax errors' % len(syntax)

    print('|  %s' % tm + ' ' * (89 - len(tm)) + '|')
    print('|' + ' ' * 78 + '|')
    print('+' + '-' * 78 + '+')
    print()


if __name__ == '__main__':
    for q in test_queries.queries[-1:]:
        s = time.time()
        qp = QueryProcessor(q[0])
        cols, keys = qp.columns, qp.keywords

        s = time.time() - s
        
        pretty_print(q, cols, keys, s, qp.syntax_errors, show_diff=True)
