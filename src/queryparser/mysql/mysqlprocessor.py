# -*- coding: utf-8 -*-
"""
MySQL processor. Its task is to check if a query has any syntax errors and
to extract all accessed columns as well as keywords and functions being
used in a query.

"""

from __future__ import (absolute_import, print_function)

__all__ = ["MySQLQueryProcessor"]

import logging
import re

import antlr4
from antlr4.error.ErrorListener import ErrorListener

from .MySQLLexer import MySQLLexer
from .MySQLParser import MySQLParser
from .MySQLParserListener import MySQLParserListener

from queryparser import QueryError


def parse_alias(alias):
    """
    Extract the alias if available.

    :param alias:
        antlr context.

    """
    if alias:
        #  try:
        alias = alias.ID().getText().strip('`')
        #  except AttributeError:
            #  alias = None
    else:
        alias = None
    return alias


def process_column_name(column_name_listener, walker, ctx):
    cn = []
    column_name_listener.column_name = []
    walker.walk(column_name_listener, ctx)
    if column_name_listener.column_name:
        for i in column_name_listener.column_name:
            cni = [None, None, None]
            if i.schema_name():
                cni[0] = i.schema_name().getText().replace('`', '')
            if i.table_name():
                cni[1] = i.table_name().getText().replace('`', '')
            if i.column_name():
                cni[2] = i.column_name().getText().replace('`', '')
            cn.append(cni)
    else:
        try:
            ctx.ASTERISK()
            ts = ctx.table_spec()
            cn = [[None, None, '*']]
            if ts.schema_name():
                cn[0][0] = ts.schema_name().getText().replace('`', '')
            if ts.table_name():
                cn[0][1] = ts.table_name().getText().replace('`', '')
        except AttributeError:
            cn = [[None, None, None]]

    return cn


class QueryListener(MySQLParserListener):
    """
    Extract all select_expressions.

    """
    def __init__(self):
        self.select_expressions = []
        self.select_list = None
        self.keywords = []
        self.subquery_aliases = {}

    def enterSelect_statement(self, ctx):
        if ctx.UNION_SYM():
            self.keywords.append('union')

    def enterSelect_expression(self, ctx):
        # we need to keep track of unions as they act as subqueries
        self.select_expressions.append(ctx)

        parent = ctx.parentCtx.parentCtx
        if isinstance(parent, MySQLParser.SubqueryContext):
            try:
                alias = parent.parentCtx.alias()
                alias = parse_alias(alias)
                self.subquery_aliases[ctx] = alias
            except AttributeError:
                pass

    def enterSelect_list(self, ctx):
        if not self.select_list:
            self.select_list = ctx


class RemoveSubqueriesListener(MySQLParserListener):
    """
    Remove nested select_expressions.

    """
    def __init__(self, depth):
        self.depth = depth
        #  self.subquery_aliases = []

    def enterSelect_expression(self, ctx):
        parent = ctx.parentCtx.parentCtx

        if isinstance(parent, MySQLParser.SubqueryContext) and ctx.depth() >\
                self.depth:
            try:
                alias = parent.parentCtx.alias()
            except AttributeError:
                alias = None

            # subquery alias
            alias = parse_alias(alias)
            #  self.subquery_aliases.append([alias, ctx.depth()])
            ctx.parentCtx.removeLastChild()


class ColumnNameListener(MySQLParserListener):
    """
    Get all column names.

    """
    def __init__(self):
        self.column_name = []

    def enterColumn_spec(self, ctx):
        self.column_name.append(ctx)


class TableNameListener(MySQLParserListener):
    """
    Get table names.

    """
    def __init__(self):
        self.table_names = []
        self.table_aliases = []

    def enterTable_atom(self, ctx):
        self.table_names.append(ctx)

    def enterAlias(self, ctx):
        alias = parse_alias(ctx)
        self.table_aliases.append(alias)


class ColumnKeywordFunctionListener(MySQLParserListener):
    """
    Extract columns, keywords and functions.

    """
    def __init__(self):
        self.tables = []
        self.columns = []
        self.column_aliases = []
        self.keywords = []
        self.functions = []
        self.column_name_listener = ColumnNameListener()
        self.table_name_listener = TableNameListener()
        self.walker = antlr4.ParseTreeWalker()

        self.data = []

    def _process_alias(self, ctx):
        try:
            alias = ctx.alias()
        except AttributeError:
            alias = None
        alias = parse_alias(alias)
        return alias

    def _extract_column(self, ctx, append=True, join_columns=False):
        cn = process_column_name(self.column_name_listener, self.walker,
                                 ctx)
        alias = self._process_alias(ctx)
        
        if len(cn) > 1:
            if join_columns:
                columns = [[i, None, join_columns] for i in cn]
            else:
                columns = [[i, None] for i in cn]

        else:
            if join_columns:
                columns = [[cn[0], alias, join_columns]]
            else:
                columns = [[cn[0], alias]]

        if not append:
            return alias, columns

        if alias is not None:
            self.column_aliases.append(alias)

        if cn[0] not in self.column_aliases:
            self.columns.extend(columns)

    def enterTable_references(self, ctx):
        self.walker.walk(self.table_name_listener, ctx)
        tas = self.table_name_listener.table_aliases
        if len(tas):
            logging.info(ctx.depth(), ctx.__class__.__name__, tas)
            self.data.append([ctx.depth(), ctx, tas])
        else:
            logging.info(ctx.depth(), ctx.__class__.__name__)
            self.data.append([ctx.depth(), ctx])

    def enterTable_atom(self, ctx):
        alias = parse_alias(ctx.alias())
        ts = ctx.table_spec()
        if ts:
            tn = [None, None]
            if ts.schema_name():
                tn[0] = ts.schema_name().getText().replace('`', '')
            if ts.table_name():
                tn[1] = ts.table_name().getText().replace('`', '')
            self.tables.append((alias, tn, ctx.depth()))

            logging.info(ctx.depth(), ctx.__class__.__name__, [tn, alias])
            self.data.append([ctx.depth(), ctx, [tn, alias]])

    def enterDisplayed_column(self, ctx):
        logging.info(ctx.depth(), ctx.__class__.__name__,
                     self._extract_column(ctx, append=False)[1])
        self.data.append([ctx.depth(), ctx,
                          self._extract_column(ctx, append=False)[1]])
        self._extract_column(ctx)
        if ctx.ASTERISK():
            self.keywords.append('*')

    def enterSelect_expression(self, ctx):
        logging.info(ctx.depth(), ctx.__class__.__name__)
        self.data.append([ctx.depth(), ctx])
       
    #  def enterQuery(self, ctx):
        #  logging.info(ctx.depth(), ctx.__class__.__name__)
        #  self.data.append([ctx.depth(), ctx])

    def enterSelect_list(self, ctx):
        if ctx.ASTERISK():
            logging.info(ctx.depth(), ctx.__class__.__name__,
                         [[None, None, '*'], None])
            self.data.append([ctx.depth(), ctx, [[[None, None, '*'], None]]])
            self.columns.append(('*', None))
            self.keywords.append('*')

    def enterFunctionList(self, ctx):
        self.functions.append(ctx.getText())

    def enterGroup_functions(self, ctx):
        self.functions.append(ctx.getText())

    def enterGroupby_clause(self, ctx):
        self.keywords.append('group by')
        col = self._extract_column(ctx, append=False)
        if col[1][0][0][2] not in self.column_aliases:
            self._extract_column(ctx)
        logging.info(ctx.depth(), ctx.__class__.__name__,
                     self._extract_column(ctx, append=False)[1])
        self.data.append([ctx.depth(), ctx,
                          self._extract_column(ctx, append=False)[1]])

    def enterWhere_clause(self, ctx):
        self.keywords.append('where')
        self._extract_column(ctx)
        logging.info(ctx.depth(), ctx.__class__.__name__,
                     self._extract_column(ctx, append=False)[1])
        self.data.append([ctx.depth(), ctx,
                          self._extract_column(ctx, append=False)[1]])

    def enterOrderby_clause(self, ctx):
        self.keywords.append('order by')
        col = self._extract_column(ctx, append=False)
        if col[1][0][0][2] not in self.column_aliases:
            self._extract_column(ctx)
        logging.info(ctx.depth(), ctx.__class__.__name__,
                     self._extract_column(ctx, append=False)[1])
        self.data.append([ctx.depth(), ctx,
                          self._extract_column(ctx, append=False)[1]])

    def enterLimit_clause(self, ctx):
        self.keywords.append('limit')

    def enterJoin_condition(self, ctx):
        self.keywords.append('join')
        self._extract_column(ctx, join_columns=ctx)
        logging.info(ctx.depth(), ctx.__class__.__name__,
                     self._extract_column(ctx, append=False)[1])
        self.data.append([ctx.depth(), ctx,
                          self._extract_column(ctx, append=False)[1]])


class SyntaxErrorListener(ErrorListener):
    def __init__(self):
        super(SyntaxErrorListener, self).__init__()
        self.syntax_errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.syntax_errors.append((line, column, offendingSymbol.text))


class MySQLQueryProcessor(object):
    """
    Object used for processing MySQL queries. Its objective is query validation
    (syntax error detection )and extraction of used columns, keywords and
    functions.

    :param query:
        MySQL query string.

    """
    def __init__(self, query=None):
        self.walker = antlr4.ParseTreeWalker()

        self.columns = set()
        self.keywords = set()
        self.functions = set()
        self.display_columns = []
        self.syntax_error_listener = SyntaxErrorListener()
        self.syntax_errors = []
        if query is not None:
            self._query = query.rstrip(';') + ';'
            self.process_query()

    def _extract_instances(self, column_keyword_function_listener):
        select_list_columns = []
        other_columns = []
        go_columns = []
        column_aliases = []
        select_list_tables = []
        select_list_table_references = []
        join = 0
        join_using = None

        for i in column_keyword_function_listener.data:
            if isinstance(i[1], MySQLParser.Displayed_columnContext):
                # this happens if there is an expression involving
                # more columns
                if len(i[2]) > 1:
                    for j in i[2]:
                        other_columns.append([j])
                else:
                    select_list_columns.append(i[2])
                alias = parse_alias(i[1].alias())
                if alias is not None:
                    column_aliases.append(alias)

            if isinstance(i[1], MySQLParser.Table_atomContext):
                select_list_tables.append([i[2], i[0]])
            if isinstance(i[1], MySQLParser.Table_referencesContext):
                if len(i) > 2:
                    select_list_table_references.extend(i[2])
            if isinstance(i[1], MySQLParser.Select_listContext):
                if len(i) == 3:
                    select_list_columns.append(i[2])
            if isinstance(i[1], MySQLParser.Where_clauseContext):
                if len(i[2]) > 1:
                    for j in i[2]:
                        other_columns.append([j])
                else:
                    other_columns.append(i[2])
            if isinstance(i[1], MySQLParser.Join_conditionContext):
                join = i[0]
                if len(i[2]) > 1:
                    for j in i[2]:
                        other_columns.append([j])
                join_using = i[2]

            if isinstance(i[1], MySQLParser.Orderby_clauseContext):
                if len(i[2]) > 1:
                    for j in i[2]:
                        go_columns.append([j])
                else:
                    go_columns.append(i[2])
            if isinstance(i[1], MySQLParser.Groupby_clauseContext):
                if len(i[2]) > 1:
                    for j in i[2]:
                        go_columns.append([j])
                else:
                    go_columns.append(i[2])

        return select_list_columns, select_list_tables,\
                select_list_table_references, other_columns, go_columns, join,\
                join_using, column_aliases

    def _extract_columns(self, columns, select_list_tables, ref_dict, join,
                         touched_columns=None):

        # Here we store all columns that might have references somewhere
        # higer up in the tree structure. We'll revisit them later.
        missing_columns = []

        for i, col in enumerate(columns):
            c = col[0]

            tab = [[None, None], None]
            try:
                tab = select_list_tables[0][0]
            except IndexError:
                pass

            try:
                # ref can be a table or a budget of columns
                ref = ref_dict[c[0][1]]

                if isinstance(ref[0], int):
                    # ref is a budget column
                    for bc in ref[2]:
                        if c[0][2] == bc[0][2]:
                            tab = [[bc[0][0], bc[0][1]], 'None']
                else:
                    # ref is a table
                    tab = ref[0]

            except KeyError:
                # we don't need to bother if there are no selected columns
                if c[0][2] is not None and c[0][1] is not None:
                    missing_columns.append(c)
                    columns[i] = [[c[0][0], c[0][1], c[0][2]], c[1]]
                    continue

                elif c[0][2] is not None and c[0][1] is None and\
                        len(ref_dict.keys()) > 1 and not join:
                    raise QueryError('Column `%s` is ambiguous.' % c[0][2])

            if touched_columns is not None:
                touched_columns.append([[tab[0][0], tab[0][1], c[0][2]], c[1]])
            else:
                columns[i] = [[tab[0][0], tab[0][1], c[0][2]], c[1]]

        return missing_columns

    def process_query(self):
        """
        Parses and processes the query. After a successful run it fills up
        columns, keywords, functions and syntax_errors lists.

        """

        # Antlr objects
        inpt = antlr4.InputStream(self.query)
        lexer = MySQLLexer(inpt)
        stream = antlr4.CommonTokenStream(lexer)
        parser = MySQLParser(stream)
        parser._listeners = [self.syntax_error_listener]

        # Parse the query
        tree = parser.query()

        query_listener = QueryListener()
        subquery_aliases = [None]
        query_names = []
        keywords = []
        functions = []

        self.walker.walk(query_listener, tree)
        keywords.extend(query_listener.keywords)
        subquery_aliases = query_listener.subquery_aliases

        # Columns that are accessed by the query
        touched_columns = []
        # List we use to propage the columns through the tree
        budget = []
        # Are there any joins in the query?
        join = 0

        missing_columns = []

        # Check if we have non-unique subquery aliases
        if len(set(subquery_aliases.values())) !=\
                len(subquery_aliases.values()):
            raise QueryError('Query includes non-unique subquery aliases.')

        # Iterate through subqueries starting with the lowerst level
        for ccc, ctx in enumerate(query_listener.select_expressions[::-1]):
            remove_subquieries_listener = RemoveSubqueriesListener(ctx.depth())
            column_keyword_function_listener = ColumnKeywordFunctionListener()

            # Remove nested subqueries from select_expressions
            self.walker.walk(remove_subquieries_listener, ctx)
            
            # Extract table and column names, keywords, functions
            self.walker.walk(column_keyword_function_listener, ctx)

            keywords.extend(column_keyword_function_listener.keywords)
            functions.extend(column_keyword_function_listener.functions)

            # Let's make sure we have a select expression context
            #  if not isinstance(column_keyword_function_listener.data[0][1],
                              #  MySQLParser.Select_expressionContext):
                #  continue

            # Does the subquery has an alias?
            try:
                subquery_alias = subquery_aliases[ctx]
            except KeyError:
                subquery_alias = None

            current_depth = column_keyword_function_listener.data[0][0]

            # We get the columns from the select list along with all
            # other touched columns and any posible join conditions
            select_list_columns, select_list_tables,\
                select_list_table_references, other_columns, go_columns, join,\
                join_using, column_aliases =\
                self._extract_instances(column_keyword_function_listener)

            # Then we need to connect the column names s with tables and
            # databases

            ref_dict = {}
            
            for ref in select_list_table_references:
                ref_found = False
                for tab in select_list_tables:
                    if ref == tab[0][1]:
                        ref_dict[ref] = tab
                        ref_found = True

                if not ref_found:
                    for b in budget:
                        if ref == b[1]:
                            ref_dict[ref] = b
                            #  ref_found = True

                #  if not ref_found:
                    #  raise QueryError('Missing table reference %s.' % ref)

            if not len(select_list_table_references):
                for table in select_list_tables:
                    ref_dict[table[0][0][1]] = table

            #  if len(select_list_tables) > len(ref_dict.keys()) + 1:
                #  raise QueryError('Some columns are ambiguous.')

            mc = self._extract_columns(select_list_columns, select_list_tables,
                                       ref_dict, join)
            missing_columns.extend([[i] for i in mc])

            touched_columns.extend(select_list_columns)
            budget.append([current_depth, subquery_alias, select_list_columns])

            aliases = [i[1] for i in select_list_columns] + column_aliases
            for col in go_columns:
                if col[0][0][2] not in aliases:
                    other_columns.append(col)

            mc = self._extract_columns(other_columns, select_list_tables,
                                       ref_dict, join, touched_columns)
            missing_columns.extend([[i] for i in mc])

            if join:
                join_columns = []
                join_columns.append(budget.pop(-1))
                if len(join_using) == 1:
                    for tab in select_list_tables:
                        touched_columns.append([[tab[0][0][0], tab[0][0][1],
                                                 join_using[0][0][2]], None])
                bp = []
                for b in budget[::-1]:
                    if b[0] > current_depth:
                        bp.append(budget.pop(-1)[2])
                    else:
                        break

                # check if the join_column is in each sub select_list
                for b in bp:
                    if join_using[0][0][2] not in [i[0][2] for i in b]:
                        raise QueryError('Missing join column `%s`.' %
                                         join_using[0][0][2])
                budget.extend(join_columns)

        if len(missing_columns):
            mc = self._extract_columns(missing_columns, select_list_tables,
                                       ref_dict, join, touched_columns)

            if len(mc):
                unref_cols = ', '.join(['.'.join([j for j in i[0] if j])
                                        for i in mc])
                raise QueryError('Unreferenced column(s): %s' % unref_cols)
        
        touched_columns = set([tuple(i[0]) for i in touched_columns
                               if not None in i[0]])
        display_columns = []
        if len(budget):
            for i in budget[-1][2]:
                if i[0][2] is not None:
                    alias = i[1] if i[1] is not None else i[0][2]
                    display_columns.append([alias, i[0]])

        # Let's get rid of all columns that are already covered by
        # db.tab.*. Figure out a better way to do it and replace the code
        # below.
        asterisk_columns = []
        del_columns = []
        for col in touched_columns:
            if col[2] == '*':
                asterisk_columns.append(col)

        for acol in asterisk_columns:
            for col in touched_columns:
                if acol[0] == col[0] and acol[1] == col[1] and \
                        acol[2] != col[2]:
                    del_columns.append(col)

        if not len(self.syntax_error_listener.syntax_errors):
            self.columns = list(set(touched_columns).difference(del_columns))
            self.keywords = list(set(keywords))
            self.functions = list(set(functions))
            self.display_columns = [(i[0], i[1]) for i in display_columns]
        else:
            self.syntax_errors = self.syntax_error_listener.syntax_errors

    @property
    def query(self):
        """
        Get the query string.

        """
        return self._query

    def set_query(self, query):
        """
        Helper to set the query string.

        """
        self.columns = set()
        self.keywords = set()
        self.functions = set()
        self.display_columns = []
        self.syntax_errors = []
        self._query = query.rstrip(';') + ';'
