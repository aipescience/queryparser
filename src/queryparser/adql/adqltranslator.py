# -*- coding: utf-8 -*-

from __future__ import absolute_import

import antlr4
from antlr4.error.ErrorListener import ErrorListener

from .ADQLLexer import ADQLLexer
from .ADQLParser import ADQLParser
from .ADQLParserVisitor import ADQLParserVisitor
from .ADQLParserListener import ADQLParserListener

from ..exceptions import QueryError, QuerySyntaxError


# Function names need to be trecognized because there whitespace
# between the name and left parenthesis is not allowed and needs to be
# deleted.
adql_function_names = ('ABS', 'CEILING', 'DEGREES', 'EXP', 'FLOOR', 'LOG',
                       'LOG10', 'MOD', 'PI', 'POWER', 'RADIANS', 'RAND',
                       'SQRT', 'TRUNCATE', 'COUNT', 'ACOS', 'ASIN', 'ATAN',
                       'ATAN2', 'COS', 'COT', 'SIN', 'TAN')


def _remove_children(ctx):
    for i in range(ctx.getChildCount() - 1):
        ctx.removeLastChild()


def _process_regular_identifier(ctx_text, sql_output):
    if sql_output == 'mysql':
        ri = ctx_text.rstrip("'").lstrip("'").rstrip('"').lstrip('"')
        return '`' + ri + '`'
    elif sql_output == 'postgresql':
        return ctx_text
    else:
        return ri


class SyntaxErrorListener(ErrorListener):
    def __init__(self):
        super(SyntaxErrorListener, self).__init__()
        self.syntax_errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.syntax_errors.append((line, column, offendingSymbol.text))


class ADQLGeometryTranslationVisitor(ADQLParserVisitor):
    """
    1) Find the rule we need to translate. Point, for example.
    2) After processing it, get rid of all off its children except the first
       one. This still keeps a token in the stream so it can be accessed later
       by other visitors or listeners. Otherwise is impossible (or hard?) to
       stick a new token in the stream so the walking works flawlessly.
    3) Hash the replacement string in the contexts dictionary. Use the context
       as a hash. This way we can return the hashed string instead the
       token so we effectively translate the rule.

    :param conunits:
        What should we be converting the units to. If no conversion is
        necessary, just pass an empty string.

    """
    def __init__(self, output_sql, conunits="RADIANS"):
        self.contexts = {}
        self.output_sql = output_sql
        self.conunits = conunits

    def _convert_values(self, ctx, cidx):
        """
        Values inside the ADQL functions can be floats, expressions, or
        strings. Strings need to be treated differently because
        mysql-sphere syntax differs slightly if we pass a column name
        instead of a value.

        :param ctx:
            antlr context.

        :param cidx:
            Context child index.

        """
        vals = []
        for i in ctx.children[cidx].getText().split(','):
            try:
                val = float(i)
            except ValueError:
                try:
                    val = float(eval(i))
                except (AttributeError, ValueError, NameError, SyntaxError):
                    if self.output_sql == 'mysql':
                        val = '.'.join('`{0}`'.format(v.rstrip("'").
                                                      lstrip("'").
                                                      rstrip('"').lstrip('"'))
                                       for v in i.split('.'))
                    elif self.output_sql == 'postgresql':
                        val = '.'.join('{0}'.format(v)
                                       for v in i.split('.'))

            vals.append(val)

        return vals

    def visitRegular_identifier(self, ctx):
        if isinstance(ctx.parentCtx,
                      ADQLParser.User_defined_function_nameContext):
            return
        ri = _process_regular_identifier(ctx.getText(), self.output_sql)
        self.contexts[ctx] = ri

    def visitSchema_name(self, ctx):
        ri = _process_regular_identifier(ctx.getText(), self.output_sql)
        self.contexts[ctx] = ri

    def visitAs_clause(self, ctx):
        # We need to visit the AS clause to avoid aliases being treated same
        # as regular identifiers and backticked.
        try:
            ri = _process_regular_identifier(ctx.children[1].getText(),
                                             self.output_sql)
            alidx = 1
        except IndexError:
            ri = _process_regular_identifier(ctx.children[0].getText(),
                                             self.output_sql)
            alidx = 0

        if ctx.children[alidx].getText()[0] != '"':
            if self.output_sql == 'mysql':
                ri = ri.replace('`', '')
        _remove_children(ctx)
        self.contexts[ctx] = 'AS ' + ri

    def visitPoint(self, ctx):
        coords = []
        for j in (2, 4):
            coords.extend(self._convert_values(ctx, j))
        if len(coords) == 3:
            coords = coords[1:]

        if self.output_sql == 'mysql':
            ctx_text = "spoint( %s(%s), %s(%s) )" % (self.conunits, coords[0],
                                                     self.conunits, coords[1])
        elif self.output_sql == 'postgresql':
            ctx_text = "spoint( %s(%s), %s(%s) )" % (self.conunits, coords[0],
                                                     self.conunits, coords[1])
        else:
            ctx_text = ''

        _remove_children(ctx)
        self.contexts[ctx] = ctx_text

    def visitBox(self, ctx):
        s = 4
        pars = []
        for j in range(0, 5, 2):
            pars.extend(self._convert_values(ctx, s + j))

        try:
            topright_x = float(pars[0]) + float(pars[2])
            topright_y = float(pars[1]) + float(pars[3])
        except ValueError:
            raise QueryError('sbox values incorrect')

        if self.output_sql in ('mysql', 'postgresql'):
            ctx_text = "sbox( spoint(%s(%s),%s(%s)),spoint(%s(%s),%s(%s)) )" %\
                (self.conunits, pars[0], self.conunits, pars[1],
                 self.conunits, '%.12f' % topright_x, self.conunits,
                 '%.12f' % topright_y)
        else:
            ctx_text = ''

        _remove_children(ctx)
        self.contexts[ctx] = ctx_text

    def visitCircle(self, ctx):
        s = 4
        pars = []
        for j in range(0, 3, 2):
            pars.extend(self._convert_values(ctx, s + j))

        if self.output_sql in ('mysql', 'postgresql'):
            ctx_text = "scircle( spoint(%s(%s), %s(%s)), %s(%s) )" %\
                (self.conunits, pars[0], self.conunits, pars[1],
                 self.conunits, pars[2])
        else:
            ctx_text = ''

        _remove_children(ctx)
        self.contexts[ctx] = ctx_text

    def visitPolygon(self, ctx):
        s = 4

        j = 0
        pars = []
        while True:
            try:
                pars.append(self._convert_values(ctx, s + j))
                s += 2
            except IndexError:
                break

        ustr = ''
        if self.conunits == "RADIANS":
            ustr = 'd'

        if self.output_sql in ('mysql', 'postgresql'):
            ctx_text = "spoly('{"
            for p in pars:
                ctx_text += '(%s%s,%s%s),' % (str(p[0]), ustr, str(p[1]), ustr)
            ctx_text = ctx_text[:-1] + "}')"
        else:
            ctx_text = ''

        _remove_children(ctx)
        self.contexts[ctx] = ctx_text


class ADQLContainsVisitor(ADQLParserVisitor):
    def __init__(self):
        self.contains = []

    def visitContains(self, ctx):
        if ctx.getText().lower()[:8] == 'contains':
            self.contains.append(ctx)


class ADQLComparisonPredicateVisitor(ADQLParserVisitor):
    # Get rid of "1=" in 1=CONTAINS() statement
    def visitComparison_predicate(self, ctx):
        contains_visitor = ADQLContainsVisitor()
        contains_visitor.visit(ctx)
        if len(contains_visitor.contains):
            if ctx.children[0].getText().lower()[:8] == 'contains':
                ctx.children[1].removeLastChild()
                ctx.children[2].removeLastChild()
            elif ctx.children[2].getText().lower()[:8] == 'contains':
                ctx.children[0].removeLastChild()
                ctx.children[1].removeLastChild()


class ADQLFunctionsTranslationVisitor(ADQLParserVisitor):
    """
    Run this visitor after the geometry has already been processed.

    :param contexts:
        A dictionary that was created in the previous run and includes
        the replaced geometry chunks.

    """
    def __init__(self, contexts, output_sql, conunits="DEGREES"):
        self.contexts = contexts
        self.output_sql = output_sql
        self.conunits = conunits

    def visitArea(self, ctx):
        #  arg = self.contexts[ctx.children[2].children[0].children[0]]
        arg = self.contexts[ctx.children[2].children[0]]

        if self.output_sql == 'mysql':
            ctx_text = 'sarea(%s)' % arg
        elif self.output_sql == 'postgresql':
            ctx_text = 'area(%s)' % arg
        else:
            ctx_text = ''

        for i in range(ctx.getChildCount() - 1):
            ctx.removeLastChild()
        self.contexts[ctx] = ctx_text

    def visitCentroid(self, ctx):
        """
        Works only for circles.

        """
        #  arg = self.contexts[ctx.children[2].children[0].children[0]]
        arg = self.contexts[ctx.children[2].children[0]]

        if self.output_sql == 'mysql':
            ctx_text = 'scenter(%s)' % arg
        elif self.output_sql == 'postgresql':
            ctx_text = 'center(%s)' % arg
        else:
            ctx_text = ''

        _remove_children(ctx)
        self.contexts[ctx] = ctx_text

    def visitContains(self, ctx):
        arg = (self.contexts[ctx.children[2].children[0]],
               self.contexts[ctx.children[4].children[0]])

        if self.output_sql == 'mysql':
            ctx_text = 'srcontainsl(%s, %s)' % arg
        elif self.output_sql == 'postgresql':
            ctx_text = '%s @ %s' % arg
        else:
            ctx_text = ''

        _remove_children(ctx)
        self.contexts[ctx] = ctx_text

    def visitDistance(self, ctx):
        try:
            arg = (self.contexts[ctx.children[2].children[0]],
                   self.contexts[ctx.children[4].children[0]])
        except KeyError:
            raise QueryError('Distance in the current implementation is ' +
                             'possible only between to explicitly defined' +
                             'points.')

        if self.output_sql == 'mysql':
            ctx_text = '%s(sdist(%s, %s))' % ((self.conunits, ) + arg)
        elif self.output_sql == 'postgresql':
            ctx_text = '%s(%s <-> %s)' % ((self.conunits, ) + arg)
        else:
            ctx_text = ''

        for i in range(ctx.getChildCount() - 1):
            ctx.removeLastChild()
        self.contexts[ctx] = ctx_text

    def visitIntersects(self, ctx):
        arg = (self.contexts[ctx.children[2].children[0]],
               self.contexts[ctx.children[4].children[0]])

        if self.output_sql == 'mysql':
            ctx_text = 'soverlaps(%s, %s)' % arg
        elif self.output_sql == 'postgresql':
            ctx_text = '%s && %s' % arg
        else:
            ctx_text = ''

        _remove_children(ctx)
        self.contexts[ctx] = ctx_text

    def visitMath_function(self, ctx):
        ctx_text = ctx.getText()
        if self.output_sql == 'postgresql' and ctx_text[:5].lower() == 'log10':
            _remove_children(ctx)
            self.contexts[ctx] = 'LOG' + ctx_text[5:]
        elif self.output_sql == 'postgresql' and ctx_text[:3].lower() == 'log':
            _remove_children(ctx)
            self.contexts[ctx] = 'LN' + ctx_text[3:]


class SelectQueryListener(ADQLParserListener):
    def __init__(self):
        self.limit_visitor = LimitVisitor()
        self.limit_contexts = {}

    def enterSelect_query(self, ctx):
        self.limit_visitor.visit(ctx)
        self.limit_contexts.update(self.limit_visitor.limit_contexts)


class LimitVisitor(ADQLParserVisitor):
    def __init__(self, remove=False):
        self.limit_terminal_visitor = LimitTerminalVisitor()
        self.limit_contexts = {}

    def visitSet_limit(self, ctx):
        try:
            self.limit = int(ctx.children[1].getText())
            ctx.removeLastChild()
            ctx.removeLastChild()

            self.limit_terminal_visitor.visit(ctx.parentCtx)
            lstr = 'LIMIT %d' % self.limit
            self.limit_contexts[self.limit_terminal_visitor.terminal] = lstr
        except IndexError:
            pass


class LimitTerminalVisitor(ADQLParserVisitor):
    def __init__(self):
        self.terminal = None

    def visitTerminal(self, ctx):
        self.terminal = ctx


class FormatListener(ADQLParserListener):
    """
    Used for formating the output query.

    """
    def __init__(self, parser, contexts, limit_contexts):
        self._parser = parser
        self.nodes = []
        self.contexts = contexts
        self.limit_contexts = limit_contexts

    def visitTerminal(self, node):
        try:
            if node.parentCtx.INTERSECT():
                raise QueryError('INTERSECT operator not supported. Please ' +
                                 'rewrite query using WHERE statement.')
        except AttributeError:
            pass

        try:
            if node.parentCtx.EXCEPT():
                raise QueryError('EXCEPT operator not supported. Please ' +
                                 'rewrite query using WHERE statement.')
        except AttributeError:
            pass

        try:
            if node.parentCtx.WITH():
                raise QueryError('WITH clause not supported.')

        except AttributeError:
            pass

        try:
            nd = self.contexts[node.parentCtx]
        except KeyError:
            nd = node.getText()
            if isinstance(node.parentCtx,
                          ADQLParser.Character_string_literalContext):
                if nd == "'":
                    nd = None

        if nd is not None:
            if isinstance(node.parentCtx, ADQLParser.Set_function_typeContext)\
                or isinstance(node.parentCtx.parentCtx,
                              ADQLParser.User_defined_function_nameContext)\
                    or nd.upper() in adql_function_names:
                nd += '_'

            self.nodes.append(nd)

        try:
            nd = self.limit_contexts[node]
            self.nodes.append(nd)
        except KeyError:
            pass

    def format_query(self):
        query = ' '.join(self.nodes).rstrip(';')
        query = query.replace('_ ', '')
        query = query.replace(' . ', '.')
        query = query.replace(' , ', ', ')
        query = query.replace('( ', '(')
        query = query.replace(' )', ')')
        query = query.rstrip()
        return '%s;' % query.rstrip()


class ADQLQueryTranslator(object):
    """
    The main translator object used to do the actual translation.

    :param query:
        ADQL query string.

    """
    def __init__(self, query=None):
        self._query = None

        if query is not None:
            self.set_query(query)

    def parse(self):
        """
        Parse the input query and store the output in self.tree.

        """
        inpt = antlr4.InputStream(self.query)
        lexer = ADQLLexer(inpt)
        self.stream = antlr4.CommonTokenStream(lexer)
        self.parser = ADQLParser(self.stream)
        self.syntax_error_listener = SyntaxErrorListener()
        self.parser._listeners = [self.syntax_error_listener]

        self.tree = self.parser.query()

        if len(self.syntax_error_listener.syntax_errors):
            raise QuerySyntaxError(self.syntax_error_listener.syntax_errors)

        self.walker = antlr4.ParseTreeWalker()

    @property
    def query(self):
        """
        Get the query string.

        """
        return self._query

    def set_query(self, query):
        """
        Set the query string. A semicolon is added in case it is missing.

        :param value:
            Query string.

        """
        self._query = query.lstrip('\n').rstrip().rstrip(';') + ';'
        self.parse()

    def translate(self, translator_visitor):

        select_query_listener = SelectQueryListener()
        self.walker.walk(select_query_listener, self.tree)

        format_listener = FormatListener(self.parser,
                                         translator_visitor.contexts,
                                         select_query_listener.limit_contexts)
        self.walker.walk(format_listener, self.tree)
        return format_listener.format_query()

    def to_mysql(self):
        """
        Translate ADQL query to a MySQL query using mysql_sphere plugin
        for the spherical functions.

        """
        if self._query is None:
            raise QueryError('No query given.')

        self.parse()

        translator_visitor = ADQLGeometryTranslationVisitor(output_sql='mysql')
        translator_visitor.visit(self.tree)
        translator_visitor = \
            ADQLFunctionsTranslationVisitor(translator_visitor.contexts,
                                            output_sql='mysql')
        translator_visitor.visit(self.tree)

        translated_query = self.translate(translator_visitor)
        # fix wrapper functions:
        for func in (('CENTROID ', 'scenter'), ('DISTANCE ', 'sdist')):
            translated_query = translated_query.replace(*func)
        return translated_query

    def to_postgresql(self):
        """
        Translate ADQL query to a PostgreSQL query using pg_sphere plugin
        for the spherical functions.

        """
        if self._query is None:
            raise QueryError('No query given.')

        self.parse()

        comp_visitor = ADQLComparisonPredicateVisitor()
        comp_visitor.visit(self.tree)

        translator_visitor = ADQLGeometryTranslationVisitor(
                output_sql='postgresql')
        translator_visitor.visit(self.tree)
        translator_visitor = \
            ADQLFunctionsTranslationVisitor(translator_visitor.contexts,
                                            output_sql='postgresql')
        translator_visitor.visit(self.tree)

        translated_query = self.translate(translator_visitor)
        return translated_query
