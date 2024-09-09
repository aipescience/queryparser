# -*- coding: utf-8 -*-

from __future__ import absolute_import

import antlr4
from antlr4.error.ErrorListener import ErrorListener

from .ADQLLexer import ADQLLexer
from .ADQLParser import ADQLParser
from .ADQLParserVisitor import ADQLParserVisitor
from .ADQLParserListener import ADQLParserListener

from ..exceptions import QueryError, QuerySyntaxError


# Function names need to be recognized because there whitespace
# between the name and left parenthesis is not allowed and needs to be
# deleted.
adql_function_names = ('ABS', 'ACOS', 'ASIN', 'ATAN', 'ATAN2', 'CEILING',
                       'COS', 'DEGREES', 'EXP', 'FLOOR', 'LOG', 'LOG10',
                       'MOD', 'PI', 'POWER', 'RADIANS', 'RAND', 'SIN',
                       'SQRT', 'TAN', 'TRUNCATE')


def _remove_children(ctx):
    for _ in range(ctx.getChildCount() - 1):
        ctx.removeLastChild()

def _convert_values(ctx, cidx, output_sql):
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
                if output_sql == 'mysql':
                    val = '.'.join('`{0}`'.format(v.rstrip("'").
                                                  lstrip("'").
                                                  rstrip('"').lstrip('"'))
                                   for v in i.split('.'))
                elif output_sql == 'postgresql':
                    val = '.'.join('{0}'.format(v)
                                   for v in i.split('.'))
        vals.append(val)
    return vals

def _process_regular_identifier(ctx_text, sql_output):
    if sql_output == 'mysql':
        ri = ctx_text.rstrip("'").lstrip("'").rstrip('"').lstrip('"')
        return '`' + ri + '`'
    elif sql_output == 'postgresql':
        return ctx_text
    else:
        return ri

def _get_ancestor_class_node(ctx, ancestor_class, depth=1):
    """ Returns the ancestor node at 'depth' level above the current node if 
    the node is of type 'ancestor_class'. Otherwise, returns None
    """
    if not hasattr(ctx, 'parentCtx'):
        return None

    if depth > 1:
        return _get_ancestor_class_node(ctx.parentCtx, ancestor_class, depth-1)
    elif depth == 1:
        if isinstance(ctx.parentCtx, ancestor_class):
            return ctx.parentCtx
    return None


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
        self.contexts[ctx.children[0]] = ri

    def visitSchema_name(self, ctx):
        ri = _process_regular_identifier(ctx.getText(), self.output_sql)
        self.contexts[ctx.children[0]] = ri

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
        self.contexts[ctx.children[0]] = 'AS ' + ri
        _remove_children(ctx)

    def visitPoint(self, ctx):
        coords = []
        if len(ctx.children) > 4:
            for j in (2, 4):
                coords.extend(self._convert_values(ctx, j))
        else:
            coords.extend(self._convert_values(ctx, 2))

        if len(coords) == 3:
            coords = coords[1:]

        if self.output_sql == 'mysql':
            ctx_text = "spoint( %s(%s), %s(%s) )" % (self.conunits, coords[0],
                                                     self.conunits, coords[1])
        elif self.output_sql == 'postgresql':
            ctx_text = "spoint( %s(%s), %s(%s) )" % (self.conunits, coords[0],
                                                     self.conunits, coords[1])
            derived_column = _get_ancestor_class_node(
                ctx,
                ADQLParser.Derived_columnContext,
                depth=3
            )
            if derived_column is not None:
                ctx_text = f"spoint_to_array_deg({ctx_text})"
                if not (any([isinstance(child, ADQLParser.As_clauseContext) \
                        for child in derived_column.children])):
                    ctx_text = f"{ctx_text} AS point"
        else:
            ctx_text = ''
        self.contexts[ctx.children[0]] = ctx_text
        _remove_children(ctx)


    def visitBox(self, ctx):
        pars = []
        s = 4 if len(ctx.children) > 8 else 2
        pars.extend(self._convert_values(ctx, s))
        pars.extend(self._convert_values(ctx, s+2))
        pars.extend(self._convert_values(ctx, s+4))

        try:
            pos_cent_ra = float(pars[0])
            pos_cent_dec = float(pars[1])
            dra = float(pars[2])/2
            ddec = float(pars[3])/2
        except ValueError:
            raise QueryError('sbox values incorrect')

        if self.output_sql in ('mysql', 'postgresql'):
            ctx_text = "sbox( spoint(%s(%s),%s(%s)),spoint(%s(%s),%s(%s)) )" %\
                (self.conunits, '%.12f' % (pos_cent_ra - dra),
                 self.conunits, '%.12f' % (pos_cent_dec - ddec),
                 self.conunits, '%.12f' % (pos_cent_ra + dra),
                 self.conunits, '%.12f' % (pos_cent_dec + ddec))

        else:
            ctx_text = ''

        self.contexts[ctx.children[0]] = ctx_text
        _remove_children(ctx)

    def visitCircle(self, ctx):
        ctx_text = ''
        if self.output_sql in ('mysql', 'postgresql'):
            s = 4 if isinstance(ctx.children[2], ADQLParser.Coord_sysContext) else 2
            radius = self._convert_values(ctx, s+2)[0]
            circle_center = ctx.children[s]
            if isinstance(circle_center.children[0], ADQLParser.CoordinatesContext):
                point_parameters = self._convert_values(circle_center, 0)
                point_ctx_text = "spoint(%s(%s), %s(%s))" %\
                    (self.conunits, point_parameters[0],
                     self.conunits, point_parameters[1])
            else:
                point_ctx = circle_center.children[0].children[0].children[0]
                if isinstance(point_ctx, ADQLParser.PointContext):
                    self.visitPoint(point_ctx)
                    point_ctx_text = self.contexts[point_ctx.children[0]]
                else:
                    raise QueryError('In the current implementation, circle ' +
                                     'allows only explicitly defined point as ' +
                                     'the circle center. For instance, ' +
                                     'CIRCLE(POINT(t.ra, r.dec), 0.1)')

            ctx_text = "scircle( %s, %s(%s) )" %\
                (point_ctx_text, self.conunits, radius)
            if self.output_sql == 'postgresql':
                derived_column = _get_ancestor_class_node(
                    ctx,
                    ADQLParser.Derived_columnContext,
                    depth=3
                )
                if derived_column is not None:
                    ctx_text = f"scircle_to_array_deg({ctx_text})"
                    if not (any([isinstance(child, ADQLParser.As_clauseContext) \
                            for child in derived_column.children])):
                        ctx_text = f"{ctx_text} AS circle"
        self.contexts[ctx.children[0]] = ctx_text
        _remove_children(ctx)


    def visitPolygon(self, ctx):
        pars = []

        for j in range(2, len(ctx.children), 2):
            par = self._convert_values(ctx, j)
            if len(par) > 1:
                pars.append(par)

        ustr = ''
        if self.conunits == "RADIANS":
            ustr = 'd'

        if self.output_sql in ('mysql', 'postgresql'):
            ctx_text = "spoly('{"
            for p in pars:
                ctx_text += '(%s%s,%s%s),' % (str(p[0]), ustr, str(p[1]), ustr)
            ctx_text = ctx_text[:-1] + "}')"
            if self.output_sql == 'postgresql':
                derived_column = _get_ancestor_class_node(
                    ctx,
                    ADQLParser.Derived_columnContext,
                    depth=3
                )
                if derived_column is not None:
                    ctx_text = f"spoly_to_array_deg({ctx_text})"
                    if not (any([isinstance(child, ADQLParser.As_clauseContext) \
                            for child in derived_column.children])):
                        ctx_text = f"{ctx_text} AS polygon"
        else:
            ctx_text = ''

        self.contexts[ctx.children[0]] = ctx_text
        _remove_children(ctx)


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
        func_name_nd = ctx.children[0]
        closing_bracket = ctx.children[-1]
        if self.output_sql == 'mysql':
            self.contexts[func_name_nd] = "sarea_"
            self.contexts[closing_bracket] = ")"
        elif self.output_sql == 'postgresql':
            self.contexts[func_name_nd] = "square_degrees(area_"
            self.contexts[closing_bracket] = "))"
        derived_column = _get_ancestor_class_node(
            ctx,
            ADQLParser.Derived_columnContext,
            depth=9
        )
        if derived_column is not None:
            if not (any([isinstance(child, ADQLParser.As_clauseContext) \
                    for child in derived_column.children])):
                self.contexts[closing_bracket] += " AS adql_area"


    def visitContains_predicate(self, ctx):
        comp_value = ctx.children[0].getText()
        if comp_value == '1' or comp_value == '0':
            if comp_value == '0':
                self.visitContains(ctx.children[2], negate=True)
            else:
                self.visitContains(ctx.children[2])
            if self.output_sql == 'postgresql':
                self.contexts[ctx.children[0]] = '_'
                self.contexts[ctx.children[1]] = '_'
        else:
            raise QueryError(
                'The function CONTAINS allows comparison to 1 or 0 only.'
            )


    def visitContains(self, ctx, negate=False):
        func_name_nd = ctx.children[0]
        lparen_nd = ctx.children[1]
        comma_nd = ctx.children[3]
        rparen_nd = ctx.children[5]

        if self.output_sql == 'mysql':
            self.contexts[func_name_nd] = 'srcontainsl_'
        elif self.output_sql == 'postgresql':
            self.contexts[func_name_nd] = '_'
            self.contexts[lparen_nd] = '_'
            if negate:
                self.contexts[comma_nd] = '!@'
            else:
                self.contexts[comma_nd] = '@'
                pass
            self.contexts[rparen_nd] = '_'


    def visitDistance(self, ctx):
        # case for the two parameter version (two points as parameters)
        if isinstance(ctx.children[2],ADQLParser.Coord_valueContext):
            func_name_nd = ctx.children[0]
            comma_nd = ctx.children[3]
            rparen_nd = ctx.children[5]
            if self.output_sql == 'mysql':
                self.contexts[func_name_nd] = 'DEGREES(sdist_'
                self.contexts[rparen_nd] = '))'
            elif self.output_sql == 'postgresql':
                self.contexts[func_name_nd] = 'DEGREES_'
                self.contexts[comma_nd] = '<->'
                derived_column = _get_ancestor_class_node(
                    ctx,
                    ADQLParser.Derived_columnContext,
                    depth=9
                )
                if derived_column is not None:
                    if not (any([isinstance(child, ADQLParser.As_clauseContext) \
                            for child in derived_column.children])):
                        self.contexts[rparen_nd] = ') AS distance'

        # case for the four parameter version (two coord pairs as parameters)
        else:
            arg = (f"spoint(RADIANS({_convert_values(ctx, 2, self.output_sql)[0]}), " +
                          f"RADIANS({_convert_values(ctx, 4, self.output_sql)[0]}))",
                   f"spoint(RADIANS({_convert_values(ctx, 6, self.output_sql)[0]}), " +
                          f"RADIANS({_convert_values(ctx, 8, self.output_sql)[0]}))")

            if self.output_sql == 'mysql':
                ctx_text = 'DEGREES(sdist(%s, %s))' % arg
            elif self.output_sql == 'postgresql':
                ctx_text = 'DEGREES(%s <-> %s)' % arg
                derived_column = _get_ancestor_class_node(
                    ctx,
                    ADQLParser.Derived_columnContext,
                    depth=9
                )
                if derived_column is not None:
                    if not (any([isinstance(child, ADQLParser.As_clauseContext) \
                            for child in derived_column.children])):
                        ctx_text = f"{ctx_text} AS distance"
            else:
                ctx_text = ''

            self.contexts[ctx.children[0]] = ctx_text
            _remove_children(ctx)


    def visitIntersects_predicate(self, ctx):
        comp_value = ctx.children[0].getText()
        if comp_value == '1' or comp_value == '0':
            if comp_value == '0':
                self.visitIntersects(ctx.children[2], negate=True)
            else:
                self.visitIntersects(ctx.children[2])
            if self.output_sql == 'postgresql':
                self.contexts[ctx.children[0]] = '_'
                self.contexts[ctx.children[1]] = '_'
        else:
            raise QueryError(
                'The function INTERSECTS allows comparison to 1 or 0 only.'
            )


    def visitIntersects(self, ctx, negate=False):
        func_name_nd = ctx.children[0]
        lparen_nd = ctx.children[1]
        comma_nd = ctx.children[3]
        rparen_nd = ctx.children[5]

        if self.output_sql == 'mysql':
            self.contexts[func_name_nd] = 'soverlaps_'
        elif self.output_sql == 'postgresql':
            self.contexts[func_name_nd] = '_'
            self.contexts[lparen_nd] = '_'
            if negate:
                self.contexts[comma_nd] = '!&&'
            else:
                self.contexts[comma_nd] = '&&'
            self.contexts[rparen_nd] = '_'


    def visitMath_function(self, ctx):
        # visiting required since the math functions allowed to be nested
        self.visitChildren(ctx)
        if self.output_sql == 'postgresql':
            func_name_nd = ctx.children[0]
            lparen = ctx.children[1]
            rparen_or_comma = ctx.children[3]
            func_name = func_name_nd.getText().lower()
            if func_name == 'log10':
                self.contexts[func_name_nd] = 'LOG_'
            elif func_name == 'log':
                self.contexts[func_name_nd] = 'LN_'
            elif func_name == 'truncate':
                self.contexts[func_name_nd] = 'TRUNC_'
                # first type cast as numeric to make it compatible with trunc()
                self.contexts[lparen] = "(CAST("
                self.contexts[rparen_or_comma] = "AS numeric)" + \
                                                 rparen_or_comma.getText()


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
            nd = self.contexts[node]
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
        query = query.replace(' ::', '::')
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

        translator_visitor = ADQLGeometryTranslationVisitor(
                output_sql='postgresql')
        translator_visitor.visit(self.tree)
        translator_visitor = \
            ADQLFunctionsTranslationVisitor(translator_visitor.contexts,
                                            output_sql='postgresql')
        translator_visitor.visit(self.tree)

        translated_query = self.translate(translator_visitor)
        return translated_query
