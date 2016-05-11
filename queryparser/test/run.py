# -*- coding: utf-8 -*-

import time
import sys
import os

from queryparser import MySQLQueryProcessor

from queryparser.test import test_queries
from queryparser.test import broken_queries


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


def pretty_print(q, columns, keywords, functions, process_time, syntax=None,
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


def test_parsing(qs):
    qp = MySQLQueryProcessor()
    for q in qs:
        qp.set_query(q[0])
        s = time.time()
        qp.process_query()
        s = time.time() - s

        cols, keys, funcs = qp.columns, qp.keywords, qp.functions
        #  not_so_pretty_print(q[0], cols, keys, funcs, s, qp.syntax_errors)
        pretty_print(q, cols, keys, funcs, s, qp.syntax_errors, show_diff=True)


if __name__ == '__main__':
    test_parsing(broken_queries.queries[:])
