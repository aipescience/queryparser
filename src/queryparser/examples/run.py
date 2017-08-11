# -*- coding: utf-8 -*-

from __future__ import print_function

import time

from queryparser import MySQLQueryProcessor
from queryparser import ADQLQueryTranslator

from queryparser.examples import test_queries
from queryparser.examples import broken_queries
from queryparser.examples import adql_queries


def not_so_pretty_print(q, columns, keywords, functions, process_time,
                        syntax=None):
    print(q)
    if syntax:
        print('  Query has syntax error(s).')
    else:
        print("  Columns: ", columns)
        print("  Keywords: ", keywords)
        print("  Functions: ", functions)
    print()


def pretty_print(q, columns, keywords, functions, column_aliases, process_time,
                 syntax=None, show_diff=True):

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

        if len(column_aliases.items()):
            print('|' + ' ' * 78 + '|')
            print('|  Column aliases:' + ' ' * 61 + '|')
            for i in sorted(column_aliases.items()):
                pstr = '%s: %s' % i
                print('|\t' + pstr + ' ' * (71 - len(pstr)) + '|')


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
            if columns.symmetric_difference(q[1]) != set():
                print('|  Missing columns:' + ' ' * 60 + '|')
                for i in columns.symmetric_difference(q[1]):
                    print('|\t' + i + ' ' * (71 - len(i)) + '|')
                print('|' + ' ' * 78 + '|')
                proc = '\033[91m\033[1mFailed\033[0m'
            if keywords.symmetric_difference(q[2]) != set():
                print('|  Missing keywords:' + ' ' * 59 + '|')
                for i in keywords.symmetric_difference(q[2]):
                    print('|\t' + i + ' ' * (71 - len(i)) + '|')
                print('|' + ' ' * 78 + '|')
                proc = '\033[91m\033[1mFailed\033[0m'
            if functions.symmetric_difference(q[3]) != set():
                print('|  Missing functions:' + ' ' * 58 + '|')
                for i in functions.symmetric_difference(q[3]):
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
    qp = MySQLQueryProcessor()
    for q in qs:
        qp.set_query(q[0])
        s = time.time()
        qp.process_query()
        s = time.time() - s

        cols, keys, funcs, col_als = qp.columns, qp.keywords, qp.functions, \
            qp.column_aliases
        #  not_so_pretty_print(q[0], cols, keys, funcs, s, qp.syntax_errors)
        pretty_print(q, cols, keys, funcs, col_als, s, qp.syntax_errors,
                     show_diff=True)


def test_adql_translation(qs):
    adt = ADQLQueryTranslator()
    for q in qs:
        adt.set_query(q)
        s = time.time()
        translated_query = adt.to_mysql()
        s = time.time() - s

        se = adt.syntax_error_listener.syntax_errors
        if len(se):
            print(se)
        print('Done in %.4fs' % s)
        print('input:  ', q)
        print('output: ', translated_query)
        print()


def test_translated_mysql_parsing(qs):
    adt = ADQLQueryTranslator()
    qp = MySQLQueryProcessor()
    for q in qs[10:20]:
        adt.set_query(q)
        translated_query = adt.to_mysql()
        qp.set_query(translated_query)
        qp.process_query()
        cols, keys, funcs = qp.columns, qp.keywords, qp.functions
        s = 0.0
        not_so_pretty_print(translated_query, cols, keys, funcs, s,
                            qp.syntax_errors)


if __name__ == '__main__':
    test_mysql_parsing(test_queries.queries[:])
    #  test_mysql_parsing(broken_queries.queries[-1:])
    #  test_adql_translation(adql_queries.queries[:])
    #  test_translated_mysql_parsing(adql_queries.queries)
