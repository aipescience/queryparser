# -*- coding: utf-8 -*-

from __future__ import absolute_import

import time

import test.test_queries
import test.broken_queries
from mysql.queryparser import QueryProcessor


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
    for q in test.test_queries.queries[-1:]:
        s = time.time()
        qp = QueryProcessor(q[0])
        cols, keys = qp.columns, qp.keywords

        s = time.time() - s
        
        pretty_print(q, cols, keys, s, qp.syntax_errors, show_diff=True)
