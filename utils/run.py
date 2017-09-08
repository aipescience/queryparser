# -*- coding: utf-8 -*-

from __future__ import print_function

import time
import re

from queryparser.mysql import MySQLQueryProcessor
from queryparser.adql import ADQLQueryTranslator
from queryparser.exceptions import QueryError, QuerySyntaxError

import old_test_queries as test_queries
import broken_queries
import adql_queries
import mysql_adql_queries


def not_so_pretty_print(q, columns, keywords, functions, process_time,
                        syntax=None):
    print(q)
    if syntax:
        print('  Query has syntax error(s).')
        print(' ', q, syntax)
    else:
        print("  Columns: ", columns)
        print("  Keywords: ", keywords)
        print("  Functions: ", functions)
    print()


def pretty_print(q, columns, keywords, functions, display_columns,
        process_time, syntax=None, show_diff=True):

    sq = q[0].split('\n')

    proc = '\033[92m\033[1mDone\033[0m'
    failed = False
    offset = [0] * len(sq)
    if len(syntax):
        for se in syntax:
            rep = "\033[91m\033[1m%s\033[0m" % se[2]
            k = se[0] - 1
            orig = sq[k]
            sq[k] = ((orig[:se[1] + offset[k]] + rep + '\033[100m' +
                      orig[se[1] + len(se[2]) + offset[k]:]))

            proc = '\033[91m\033[1mFailed\033[0m'
            failed = True
            offset[se[0] - 1] += 19

    try:
        columns = ['.'.join([str(j) for j in i]) for i in columns
                   if i[0] is not None and i[1] is not None]
        display_columns = ['%s: %s' % (str(i[0]),
                                          '.'.join([str(j) for j in i[1]]))
                              for i in display_columns]
    except TypeError:
        pass

    print('+' + '=' * 78 + '+')

    for k, i in enumerate(sq):
        print('|\033[100m' + i + ' ' * (78 - len(i) + offset[k]) + '\033[49m|')

    if not len(syntax):
        print('|' + ' ' * 78 + '|')
        if len(columns):
            print('|  Columns:' + ' ' * 68 + '|')
            for i in sorted(columns):
                print('|\t' + i + ' ' * (71 - len(i)) + '|')

        if len(display_columns):
            print('|' + ' ' * 78 + '|')
            print('|  Display columns:' + ' ' * 60 + '|')
            for i in sorted(display_columns):
                print('|\t' + i + ' ' * (71 - len(i)) + '|')

        if len(keywords):
            print('|' + ' ' * 78 + '|')
            print('|  Keywords:' + ' ' * 67 + '|')
            for i in sorted(keywords):
                print('|\t' + i.upper() + ' ' * (71 - len(i)) + '|')

        if len(functions):
            print('|' + ' ' * 78 + '|')
            print('|  Functions:' + ' ' * 66 + '|')
            for i in sorted(functions):
                print('|\t' + i.upper() + ' ' * (71 - len(i)) + '|')

        print('|' + ' ' * 78 + '|')

        if show_diff:
            if set(columns).symmetric_difference(q[1]) != set():
                print('|  Missing columns:' + ' ' * 60 + '|')
                for i in set(columns).symmetric_difference(q[1]):
                    print('|\t' + i + ' ' * (71 - len(i)) + '|')
                print('|' + ' ' * 78 + '|')
                proc = '\033[91m\033[1mFailed\033[0m'
            if set(keywords).symmetric_difference(q[2]) != set():
                print('|  Missing keywords:' + ' ' * 59 + '|')
                for i in set(keywords).symmetric_difference(q[2]):
                    print('|\t' + i + ' ' * (71 - len(i)) + '|')
                print('|' + ' ' * 78 + '|')
            if set(functions).symmetric_difference(q[3]) != set():
                print('|  Missing functions:' + ' ' * 58 + '|')
                for i in set(functions).symmetric_difference(q[3]):
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
    print('')


def test_mysql_parsing(qs):
    qp = MySQLQueryProcessor(strict=True)
    for q in qs:
        qp.set_query(q[0])
        s = time.time()
        try:
            qp.process_query(replace_schema_name={'db': 'foo', 'db2': 'bar'})
            #  qp.process_query()
            syntax_errors = []
        except QuerySyntaxError as e:
            syntax_errors = e.syntax_errors
        s = time.time() - s
        #  continue
        qm = list(q)
        qm[0] = '\n' + qp.query + '\n'
        cols, keys, funcs, dispcols= qp.columns, qp.keywords, qp.functions, \
            qp.display_columns
        #  not_so_pretty_print(q[0], cols, keys, funcs, s, qp.syntax_errors)
        pretty_print(qm, cols, keys, funcs, dispcols, s, syntax_errors,
                     show_diff=True)


def test_adql_translation(qs):
    adt = ADQLQueryTranslator()
    for q in qs:
        adt.set_query(q)
        s = time.time()
        try:
            translated_query = adt.to_mysql()
            syntax_errors = []
        except QuerySyntaxError as e:
            syntax_errors = e.syntax_errors
        s = time.time() - s

        if len(syntax_errors):
            print(syntax_errors)
        print('Done in %.4fs' % s)
        print('input:  ', q)
        print('output: ', translated_query)
        print()


def test_translated_mysql_parsing(qs):
    adt = ADQLQueryTranslator()
    qp = MySQLQueryProcessor()
    for q in qs:
        s = time.time()
        adt.set_query(q[0])
        translated_query = adt.to_mysql()
        qp.set_query(translated_query)
        try:
            qp.process_query()
        except QueryError:
            raise
        s = time.time() - s
        #  cols, keys, funcs = qp.columns, qp.keywords, qp.functions
        #  s = 0.0
        #  not_so_pretty_print(translated_query, cols, keys, funcs, s,
                            #  qp.syntax_errors)
        cols, keys, funcs, dispcols= qp.columns, qp.keywords, qp.functions, \
            qp.display_columns
        pretty_print(q, cols, keys, funcs, dispcols, s, qp.syntax_errors,
                     show_diff=True)


if __name__ == '__main__':
    test_mysql_parsing(test_queries.queries[-1:])
    #  test_mysql_parsing(test_queries.queries[35:42])
    #  test_mysql_parsing(test_queries.queries[6:7])
    #  test_mysql_parsing(test_queries.queries[:])
    #  test_mysql_parsing(broken_queries.queries[-1:])
    #  test_adql_translation(adql_queries.queries[-1:])
    #  test_translated_mysql_parsing(mysql_adql_queries.queries)
