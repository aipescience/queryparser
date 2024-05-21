# -*- coding: utf-8 -*-
# All listeners that are with minor modifications shared between PostgreSQL
# and MySQL.
from __future__ import (absolute_import, print_function)

import logging
import re

import antlr4
from antlr4.error.ErrorListener import ErrorListener

from ..exceptions import QueryError, QuerySyntaxError


def parse_alias(alias, quote_char):
    """
    Extract the alias if available.

    :param alias:
        antlr context

    :parma quote_char:
        which string quote character to use

    """
    if alias:
        alias = alias.ID().getText().strip(quote_char)
    else:
        alias = None
    return alias


def process_column_name(column_name_listener, walker, ctx, quote_char):
    '''
    A helper function that strips the quote characters from the column
    names. The returned list includes:

    cn[0] - schema
    cn[1] - table
    cn[2] - column
    cn[3] - ctx

    :param column_name_listener:
        column_name_listener object

    :param walker:
        antlr walker object 

    :param ctx:
        antlr context to walk through

    :param quote_char:
        which quote character are we expecting?

    '''
    cn = []
    column_name_listener.column_name = []
    walker.walk(column_name_listener, ctx)
    if column_name_listener.column_name:
        for i in column_name_listener.column_name:
            cni = [None, None, None, i]
            if i.schema_name():
                cni[0] = i.schema_name().getText().replace(quote_char, '')
            if i.table_name():
                cni[1] = i.table_name().getText().replace(quote_char, '')
            if i.column_name():
                cni[2] = i.column_name().getText().replace(quote_char, '')
            cn.append(cni)
    else:
        try:
            ctx.ASTERISK()
            ts = ctx.table_spec()
            cn = [[None, None, '*', None]]
            if ts.schema_name():
                cn[0][0] = ts.schema_name().getText().replace(quote_char, '')
            if ts.table_name():
                cn[0][1] = ts.table_name().getText().replace(quote_char, '')
        except AttributeError:
            cn = [[None, None, None, None]]
    return cn


def get_column_name_listener(base):

    class ColumnNameListener(base):
        """
        Get all column names.

        """
        def __init__(self):
            self.column_name = []
            self.column_as_array = []

        def enterColumn_spec(self, ctx):
            try:
                if ctx.children[1].getText():
                    self.column_as_array.append(ctx)
                else:
                    self.column_as_array.append(None)
            except IndexError:
                self.column_as_array.append(None)
            self.column_name.append(ctx)

    return ColumnNameListener


def get_table_name_listener(base, quote_char):

    class TableNameListener(base):
        """
        Get table names.

        """
        def __init__(self):
            self.table_names = []
            self.table_aliases = []

        def enterTable_atom(self, ctx):
            self.table_names.append(ctx)

        def enterAlias(self, ctx):
            alias = parse_alias(ctx, quote_char)
            self.table_aliases.append(alias)

    return TableNameListener


def get_schema_name_listener(base, quote_char):

    class SchemaNameListener(base):

        def __init__(self, replace_schema_name):
            self.replace_schema_name = replace_schema_name

        def enterSchema_name(self, ctx):
            ttype = ctx.start.type
            sn = ctx.getTokens(ttype)[0].getSymbol().text
            try:
                nsn = self.replace_schema_name[sn.replace(quote_char, '')]
                try:
                    nsn = unicode(nsn, 'utf-8')
                except NameError:
                    pass
                nsn = re.sub(r'(|{})(?!{})[\S]*[^{}](|{})'.format(
                    quote_char, quote_char, quote_char, quote_char),
                    r'\1{}\2'.format(nsn), sn)
                ctx.getTokens(ttype)[0].getSymbol().text = nsn
            except KeyError:
                pass

    return SchemaNameListener


def get_remove_subqueries_listener(base, base_parser):

    class RemoveSubqueriesListener(base):
        """
        Remove nested select_expressions.

        """
        def __init__(self, depth):
            self.depth = depth

        def enterSelect_expression(self, ctx):
            parent = ctx.parentCtx.parentCtx

            if isinstance(parent, base_parser.SubqueryContext) and \
               ctx.depth() > self.depth:
                # we need to remove all Select_expression instances, not
                # just the last one so we loop over until we get all of them
                # out
                seinstances = [isinstance(i,
                               base_parser.Select_expressionContext)
                               for i in ctx.parentCtx.children]
                while True in seinstances:
                    ctx.parentCtx.removeLastChild()
                    seinstances = [isinstance(i,
                                   base_parser.Select_expressionContext)
                                   for i in ctx.parentCtx.children]

    return RemoveSubqueriesListener


def get_query_listener(base, base_parser, quote_char):

    class QueryListener(base):
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
            if isinstance(parent, base_parser.SubqueryContext):
                try:
                    alias = parent.parentCtx.alias()
                    alias = parse_alias(alias, quote_char)
                    self.subquery_aliases[ctx] = alias
                except AttributeError:
                    pass

        def enterSelect_list(self, ctx):
            if not self.select_list:
                self.select_list = ctx

    return QueryListener


def get_column_keyword_function_listener(base, quote_char):

    class ColumnKeywordFunctionListener(base):
        """
        Extract columns, keywords and functions.

        """
        def __init__(self):
            self.tables = []
            self.columns = []
            self.column_aliases = []
            self.keywords = []
            self.functions = []
            self.column_name_listener = get_column_name_listener(base)()
            self.table_name_listener = get_table_name_listener(
                    base, quote_char)()
            self.walker = antlr4.ParseTreeWalker()

            self.data = []

        def _process_alias(self, ctx):
            try:
                alias = ctx.alias()
            except AttributeError:
                alias = None
            alias = parse_alias(alias, quote_char)
            return alias

        def _extract_column(self, ctx, append=True, join_columns=False):
            cn = process_column_name(self.column_name_listener, self.walker,
                                     ctx, quote_char)
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
                logging.info((ctx.depth(), ctx.__class__.__name__, tas))
                self.data.append([ctx.depth(), ctx, tas])
            else:
                logging.info((ctx.depth(), ctx.__class__.__name__))
                self.data.append([ctx.depth(), ctx])

        def enterTable_atom(self, ctx):
            alias = parse_alias(ctx.alias(), quote_char)
            ts = ctx.table_spec()
            if ts:
                tn = [None, None]
                if ts.schema_name():
                    tn[0] = ts.schema_name().getText().replace(quote_char, '')
                if ts.table_name():
                    tn[1] = ts.table_name().getText().replace(quote_char, '')
                self.tables.append((alias, tn, ctx.depth()))

                logging.info((ctx.depth(), ctx.__class__.__name__,
                             [tn, alias]))
                self.data.append([ctx.depth(), ctx, [tn, alias]])

        def enterDisplayed_column(self, ctx):
            logging.info((ctx.depth(), ctx.__class__.__name__,
                         self._extract_column(ctx, append=False)[1]))
            self.data.append([ctx.depth(), ctx,
                              self._extract_column(ctx, append=False)[1]])
            self._extract_column(ctx)
            if ctx.ASTERISK():
                self.keywords.append('*')

        def enterSelect_expression(self, ctx):
            logging.info((ctx.depth(), ctx.__class__.__name__))
            self.data.append([ctx.depth(), ctx])

        def enterSelect_list(self, ctx):
            if ctx.ASTERISK():
                logging.info((ctx.depth(), ctx.__class__.__name__,
                             [[None, None, '*'], None]))
                self.data.append([ctx.depth(), ctx, [[[None, None, '*'],
                                 None]]])
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
            logging.info((ctx.depth(), ctx.__class__.__name__,
                         self._extract_column(ctx, append=False)[1]))
            self.data.append([ctx.depth(), ctx,
                              self._extract_column(ctx, append=False)[1]])

        def enterWhere_clause(self, ctx):
            self.keywords.append('where')
            self._extract_column(ctx)
            logging.info((ctx.depth(), ctx.__class__.__name__,
                         self._extract_column(ctx, append=False)[1]))
            self.data.append([ctx.depth(), ctx,
                              self._extract_column(ctx, append=False)[1]])

        def enterHaving_clause(self, ctx):
            self.keywords.append('having')
            self._extract_column(ctx)
            logging.info((ctx.depth(), ctx.__class__.__name__,
                         self._extract_column(ctx, append=False)[1]))
            self.data.append([ctx.depth(), ctx,
                              self._extract_column(ctx, append=False)[1]])

        def enterOrderby_clause(self, ctx):
            self.keywords.append('order by')
            col = self._extract_column(ctx, append=False)
            if col[1][0][0][2] not in self.column_aliases:
                self._extract_column(ctx)
            logging.info((ctx.depth(), ctx.__class__.__name__,
                         self._extract_column(ctx, append=False)[1]))
            self.data.append([ctx.depth(), ctx,
                              self._extract_column(ctx, append=False)[1]])

        def enterLimit_clause(self, ctx):
            self.keywords.append('limit')

        def enterJoin_condition(self, ctx):
            self.keywords.append('join')
            self._extract_column(ctx, join_columns=ctx)
            logging.info((ctx.depth(), ctx.__class__.__name__,
                         self._extract_column(ctx, append=False)[1]))
            self.data.append([ctx.depth(), ctx,
                              self._extract_column(ctx, append=False)[1]])

        def enterSpoint(self, ctx):
            self.functions.append('spoint')

        def enterScircle(self, ctx):
            self.functions.append('scircle')

        def enterSline(self, ctx):
            self.functions.append('sline')

        def enterSellipse(self, ctx):
            self.functions.append('sellipse')

        def enterSbox(self, ctx):
            self.functions.append('sbox')

        def enterSpoly(self, ctx):
            self.functions.append('spoly')

        def enterSpath(self, ctx):
            self.functions.append('spath')

        def enterStrans(self, ctx):
            self.functions.append('strans')

    return ColumnKeywordFunctionListener


class SyntaxErrorListener(ErrorListener):
    def __init__(self):
        super(SyntaxErrorListener, self).__init__()
        self.syntax_errors = []

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        if offending_symbol is not None:
            self.syntax_errors.append((line, column, offending_symbol.text))
        else:
            self.syntax_errors.append((line, column, msg))


class SQLQueryProcessor(object):
    """
    Object used for processing MySQL/PostgreSQL queries. Its objective is query
    validation (syntax error detection) and extraction of used columns,
    keywords and functions.

    :param base_lexer:
        Base antlr Lexer class.

    :param base_parser:
        Base antlr Parser class.

    :param base_parser_listener:
        Base antlr ParserListener class.

    :param quote_char:
        Which character is used to quote strings?

    :param query:
        SQL query string.

    :param base_sphere_listener:
        Base sphere listener. For now only pg_sphere is supported but
        other types of listeners can be added.

    """
    def __init__(self, base_lexer, base_parser, base_parser_listener,
                 quote_char, query=None, base_sphere_listener=None):
        self.lexer = base_lexer
        self.parser = base_parser
        self.parser_listener = base_parser_listener
        self.quote_char = quote_char
        self.sphere_listener = base_sphere_listener

        self.walker = antlr4.ParseTreeWalker()
        self.syntax_error_listener = SyntaxErrorListener()

        self.columns = set()
        self.keywords = set()
        self.functions = set()
        self.display_columns = []

        if query is not None:
            self.set_query(query)
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

        # Keep track of the ctx stack
        ctx_stack = []

        for i in column_keyword_function_listener.data:
            if isinstance(i[1], self.parser.Displayed_columnContext):
                # this happens if there is an expression involving
                # more columns
                if len(i[2]) > 1:
                    for j in i[2]:
                        other_columns.append([j])
                else:
                    select_list_columns.append(i[2])
                alias = parse_alias(i[1].alias(), '"')
                if alias is not None:
                    column_aliases.append(alias)
                ctx_stack.append(i)

            if isinstance(i[1], self.parser.Table_atomContext):
                select_list_tables.append([i[2], i[0]])
                ctx_stack.append(i)

            if isinstance(i[1], self.parser.Table_referencesContext):
                if len(i) > 2:
                    select_list_table_references.extend(i[2])
                    ctx_stack.append(i)

            if isinstance(i[1], self.parser.Select_listContext):
                if len(i) == 3:
                    select_list_columns.append([[i[2][0][0] + [i[1]],
                                                i[2][0][1]]])
                    ctx_stack.append(i)

            if isinstance(i[1], self.parser.Where_clauseContext) or\
               isinstance(i[1], self.parser.Having_clauseContext):
                if len(i[2]) > 1:
                    for j in i[2]:
                        other_columns.append([j])
                else:
                    other_columns.append(i[2])
                ctx_stack.append(i)

            if isinstance(i[1], self.parser.Join_conditionContext):
                join = i[0]
                join_using = i[2]

                if i[1].USING_SYM():
                    for ctx in ctx_stack[::-1]:
                        if not isinstance(ctx[1],
                                          self.parser.Table_atomContext):
                            break
                        for ju in join_using:
                            if ju[0][1] is None:
                                other_columns.append([[[ctx[2][0][0],
                                                        ctx[2][0][1],
                                                        ju[0][2],
                                                        ctx[1]], None]])
                elif i[1].ON():
                    if len(i[2]) > 1:
                        for j in i[2]:
                            other_columns.append([j])

                ctx_stack.append(i)

            if isinstance(i[1], self.parser.Orderby_clauseContext):
                if len(i[2]) > 1:
                    for j in i[2]:
                        go_columns.append([j])
                else:
                    go_columns.append(i[2])
                ctx_stack.append(i)

            if isinstance(i[1], self.parser.Groupby_clauseContext):
                if len(i[2]) > 1:
                    for j in i[2]:
                        go_columns.append([j])
                else:
                    go_columns.append(i[2])
                ctx_stack.append(i)

        return select_list_columns, select_list_tables,\
            select_list_table_references, other_columns, go_columns, join,\
            join_using, column_aliases

    def _get_budget_column(self, c, tab, ref):
        cname = c[0][2]
        cctx = c[0][3]
        calias = c[1]
        t = tab

        column_found = False

        for bc in ref:
            if bc[0][2] == '*':
                t = [[bc[0][0], bc[0][1]], 'None']
                column_found = True
                break
            elif bc[1] and c[0][2] == bc[1]:
                t = [[bc[0][0], bc[0][1]], 'None']
                cname = bc[0][2]
                if c[1] is None:
                    calias = c[0][2]
                column_found = True
                break
            elif c[0][2] == bc[0][2] and bc[1] is None:
                t = [[bc[0][0], bc[0][1]], 'None']
                column_found = True
                break

        return cname, cctx, calias, column_found, t

    def _extract_columns(self, columns, select_list_tables, ref_dict, join,
                         budget, column_aliases, touched_columns=None,
                         subquery_contents=None):

        # Here we store all columns that might have references somewhere
        # higher up in the tree structure. We'll revisit them later.
        missing_columns = []
        remove_column_idxs = []
        extra_columns = []

        for i, col in enumerate(columns):
            c = col[0]

            cname = c[0][2]
            cctx = c[0][3]
            calias = c[1]

            # if * is selected we don't care too much
            if c[0][0] is None and c[0][1] is None and c[0][2] == '*'\
                    and not join:
                for slt in select_list_tables:
                    extra_columns.append([[slt[0][0][0], slt[0][0][1], cname,
                                         c[0][3]], calias])
                remove_column_idxs.append(i)
                continue

            # this can happen for example in ... WHERE EXISTS ... clauses
            if cname is None and calias is None:
                remove_column_idxs.append(i)
                continue

            tab = [[None, None], None]
            try:
                tab = select_list_tables[0][0]
                if tab[0][0] is None:
                    raise QueryError('Missing schema specification.')

                # We have to check if we also have a join on the same level
                # and we are actually touching a column from the joined table
                if join and c[0][2] != '*' and\
                        (tab[1] != c[0][1] or
                         (tab[1] is None and c[0][1] is None)):
                    cname, cctx, calias, column_found, tab =\
                            self._get_budget_column(c, tab, budget[-1][2])
                    # raise an ambiguous column
                    if column_found and c[0][1] is None:
                        raise QueryError("Column '%s' is possibly ambiguous."
                                         % c[0][2])

            except IndexError:
                pass

            try:
                # ref can be a table or a budget of columns
                ref = ref_dict[c[0][1]]
                column_found = False

                if isinstance(ref[0], int):
                    # ref is a budget column
                    cname, cctx, calias, column_found, tab =\
                            self._get_budget_column(c, tab, ref[2])

                    ref_cols = [j[0][2] for j in ref[2]]
                    if not column_found and c[0][1] is not None\
                            and c[0][1] != tab[0][1] and '*' not in ref_cols:
                        raise QueryError("Unknown column '%s.%s'." % (c[0][1],
                                                                      c[0][2]))

                else:
                    # ref is a table
                    tab = ref[0]

            except KeyError:
                if None not in c[0][:3]:
                    cname = c[0][2]
                    cctx = c[0][3]
                    calias = c[1]
                    tab = [[c[0][0], c[0][1]]]
                    column_found = True

                # table is either referenced directly or by an alias
                elif c[0][2] is not None and c[0][1] is not None:
                    if subquery_contents is not None:
                        try:
                            contents = subquery_contents[c[0][1]]
                            cname, cctx, calias, column_found, tab =\
                                self._get_budget_column(c, tab, contents)

                        except KeyError:
                            tabs = [j[0][0][:2] for j in
                                    subquery_contents.values()]
                            tabs += [j[0][0] for j in select_list_tables]
                            column_found = False
                            for t in tabs:
                                if t[1] == c[0][1]:
                                    cname = c[0][2]
                                    cctx = c[0][3]
                                    calias = c[1]
                                    tab = [t]
                                    column_found = True

                            if not column_found:
                                missing_columns.append(c)
                                columns[i] = c
                                if touched_columns is not None:
                                    touched_columns.append(c)
                                continue
                    else:
                        if tab[0][1] == c[0][1]:
                            columns[i] = [[tab[0][0], tab[0][1],
                                          c[0][2], c[0][3]], c[1]]
                        else:

                            missing_columns.append(c)
                            columns[i] = c
                            if touched_columns is not None:
                                touched_columns.append(c)
                        continue

                elif c[0][2] is not None and c[0][2] != '*' and c[0][1] is \
                        None and len(ref_dict.keys()) > 1 and not join:
                    raise QueryError("Column '%s' is ambiguous." % c[0][2])

                elif len(budget) and tab[0][0] is None and tab[0][1] is None:
                    ref = budget[-1]
                    column_found = False

                    if isinstance(ref[0], int):
                        cname, cctx, calias, column_found, tab =\
                                self._get_budget_column(c, tab, ref[2])

                        # We allow None.None columns because they are produced
                        # by count(*)
                        if not column_found and c[0][2] is not None\
                                and c[0][2] not in column_aliases:
                            raise QueryError("Unknown column '%s'." % c[0][2])

            if touched_columns is not None:
                touched_columns.append([[tab[0][0], tab[0][1], cname, cctx],
                                        calias])
            else:
                columns[i] = [[tab[0][0], tab[0][1], cname, c[0][3]], calias]

        for i in remove_column_idxs[::-1]:
            columns.pop(i)

        columns.extend(extra_columns)
        return missing_columns

    def process_query(self, replace_schema_name=None, indexed_objects=None):
        """
        Parses and processes the query. After a successful run it fills up
        columns, keywords, functions and syntax_errors lists.

        :param replace_schema_name:
            A new schema name to be put in place of the original.

        :param indexed_objects: Deprecated

        """
        # Antlr objects
        inpt = antlr4.InputStream(self.query)
        lexer = self.lexer(inpt)
        stream = antlr4.CommonTokenStream(lexer)
        parser = self.parser(stream)
        lexer._listeners = [self.syntax_error_listener]
        parser._listeners = [self.syntax_error_listener]

        # Parse the query
        tree = parser.query()
        if len(self.syntax_error_listener.syntax_errors):
            raise QuerySyntaxError(self.syntax_error_listener.syntax_errors)

        if replace_schema_name is not None:
            schema_name_listener = get_schema_name_listener(
                    self.parser_listener, self.quote_char)(replace_schema_name)
            self.walker.walk(schema_name_listener, tree)
            self._query = stream.getText()

        query_listener = get_query_listener(self.parser_listener,
                                            self.parser, self.quote_char)()
        subquery_aliases = [None]
        keywords = []
        functions = []
        tables = []

        self.walker.walk(query_listener, tree)
        keywords.extend(query_listener.keywords)
        subquery_aliases = query_listener.subquery_aliases

        # Columns that are accessed by the query
        touched_columns = []
        # List we use to propagate the columns through the tree
        budget = []
        # Are there any joins in the query?
        join = 0

        missing_columns = []

        column_aliases = []
        column_aliases_from_previous = []

        subquery_contents = {}

        # Iterate through subqueries starting with the lowest level
        for ccc, ctx in enumerate(query_listener.select_expressions[::-1]):
            remove_subquieries_listener = get_remove_subqueries_listener(
                    self.parser_listener, self.parser)(ctx.depth())
            column_keyword_function_listener = \
                get_column_keyword_function_listener(
                    self.parser_listener, self.quote_char)()

            # Remove nested subqueries from select_expressions
            self.walker.walk(remove_subquieries_listener, ctx)

            # Extract table and column names, keywords, functions
            self.walker.walk(column_keyword_function_listener, ctx)

            keywords.extend(column_keyword_function_listener.keywords)
            functions.extend(column_keyword_function_listener.functions)

            # Does the subquery has an alias?
            try:
                subquery_alias = subquery_aliases[ctx]
            except KeyError:
                subquery_alias = None

            current_depth = column_keyword_function_listener.data[0][0]

            # We get the columns from the select list along with all
            # other touched columns and any possible join conditions
            column_aliases_from_previous = [i for i in column_aliases]
            select_list_columns, select_list_tables,\
                select_list_table_references, other_columns, go_columns, join,\
                join_using, column_aliases =\
                self._extract_instances(column_keyword_function_listener)

            tables.extend([i[0] for i in select_list_tables])

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

            if not len(select_list_table_references):
                for table in select_list_tables:
                    ref_dict[table[0][0][1]] = table

            mc = self._extract_columns(select_list_columns, select_list_tables,
                                       ref_dict, join, budget,
                                       column_aliases_from_previous)
            missing_columns.extend([[i] for i in mc])

            touched_columns.extend(select_list_columns)
            current_columns = [i for i in select_list_columns]
            budget.append([current_depth, subquery_alias, select_list_columns])

            aliases = [i[1] for i in select_list_columns] + column_aliases
            for col in go_columns:
                if col[0][0][2] not in aliases:
                    other_columns.append(col)

            mc = self._extract_columns(other_columns, select_list_tables,
                                       ref_dict, join, budget,
                                       column_aliases_from_previous,
                                       touched_columns)

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

                budget.extend(join_columns)

            if subquery_alias is not None:
                subquery_contents[subquery_alias] = current_columns

        if len(missing_columns):
            mc = self._extract_columns(missing_columns, select_list_tables,
                                       ref_dict, join, budget,
                                       column_aliases_from_previous,
                                       touched_columns, subquery_contents)
            if len(mc):
                unref_cols = "', '".join(['.'.join([j for j in i[0][:3] if j])
                                         for i in mc])
                raise QueryError("Unreferenced column(s): '%s'." % unref_cols)

        touched_columns = set([tuple(i[0]) for i in touched_columns])

        # extract display_columns
        display_columns = []
        mc = self._extract_columns([[i] for i in budget[-1][2]],
                                   select_list_tables, ref_dict, join, budget,
                                   column_aliases_from_previous,
                                   display_columns, subquery_contents)

        display_columns = [[i[1] if i[1] else i[0][2], i[0]]
                           for i in display_columns]

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

        columns = list(set(touched_columns).difference(del_columns))
        self.columns = list(set([self._strip_column(i) for i in columns]))
        self.keywords = list(set(keywords))
        self.functions = list(set(functions))
        self.display_columns = [(i[0].lstrip('"').rstrip('"'),
                                list(self._strip_column(i[1])))
                                for i in display_columns]

        self.tables = list(set([tuple([i[0][0].lstrip('"').rstrip('"')
                                      if i[0][0] is not None else i[0][0],
                                      i[0][1].lstrip('"').rstrip('"')
                                      if i[0][1] is not None else i[0][1]])
                                for i in tables]))

    @property
    def query(self):
        """
        Get the query string.

        """
        return self._query

    def _strip_query(self, query):
        return query.lstrip('\n').rstrip().rstrip(';') + ';'

    def _strip_column(self, col):
        scol = [None, None, None]
        for i in range(3):
            if col[i] is not None:
                scol[i] = col[i].lstrip('"').rstrip('"')
        return tuple(scol)

    def set_query(self, query):
        """
        Helper to set the query string.

        """
        self.columns = set()
        self.keywords = set()
        self.functions = set()
        self.display_columns = []
        self.syntax_error_listener = SyntaxErrorListener()
        self._query = self._strip_query(query)
