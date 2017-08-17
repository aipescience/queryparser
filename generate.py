#!/usr/bin/env python

import argparse
import os
import shutil
import subprocess
import re

ANTLR_JAR = 'antlr-4.7-complete.jar'
ANTLR_DIRS = ('.', '/usr/local/lib/', '/usr/local/bin/')

QUERYPARSER_SRC = 'src/queryparser/'
MYSQL_SRC = 'src/queryparser/mysql'
ADQL_SRC = 'src/queryparser/adql'


def main():
    parser = argparse.ArgumentParser(description='Generate the parsers.')
    parser.add_argument('-l', help='language (ADQL or MySQL)')
    parser.add_argument('-p', type=int, help='python version (2 or 3)')

    args = parser.parse_args()

    languages = [args.l] if args.l else ['adql', 'mysql']
    python_versions = [args.p] if args.p else [2, 3]

    if get_java_version() < 7:
        raise RuntimeError('You need a newer version of Java.')

    antlr_path = get_antlr_path()
    if not antlr_path:
        raise RuntimeError('You need Antlr 4.7 installed in %s.' % ':'.join(ANTLR_DIRS))

    for python_version in python_versions:
        for language in languages:
            if language == 'adql':
                build_adql_translator(antlr_path, python_version)

            if language == 'mysql':
                build_mysql_parser(antlr_path, python_version)


def get_java_version():
    try:
        args = ['java', '-version']
        output = subprocess.check_output(args, stderr=subprocess.STDOUT)
        match = re.search('version \"(\d+).(\d+).(.*?)\"', output.decode('utf-8'))
        if match:
            return int(match.group(2))
    except OSError:
        pass

    raise RuntimeError('No java version found.')


def get_antlr_path():
    for directory in ANTLR_DIRS:
        path = os.path.join(directory, ANTLR_JAR)
        if os.path.exists(path):
            return path
    return False


def build_mysql_parser(antlr_path, python_version):
    args = ['java', '-jar', antlr_path, '-Dlanguage=Python%d' % python_version, '-lib', MYSQL_SRC]

    print('building mysql lexer for python%i' % python_version)
    subprocess.check_call(args + [os.path.join(MYSQL_SRC, 'MySQLLexer.g4')])

    print('building mysql parser for python%i' % python_version)
    subprocess.check_call(args + [os.path.join(MYSQL_SRC, 'MySQLParser.g4')])


    directory = os.path.join('lib', 'python2' if python_version < 3 else 'python3', 'queryparser/mysql')
    try:
        os.makedirs(directory)
    except OSError:
        pass

    for filename in ['MySQLLexer.py', 'MySQLParser.py', 'MySQLParserListener.py']:
        source = os.path.join(MYSQL_SRC, filename)
        target = os.path.join(directory, filename)

        print('moving %s -> %s' % (source, target))
        shutil.move(source, target)

    os.remove(os.path.join(MYSQL_SRC, 'MySQLLexer.tokens'))
    os.remove(os.path.join(MYSQL_SRC, 'MySQLParser.tokens'))


def build_adql_translator(antlr_path, python_version):
    args = ['java', '-jar', antlr_path, '-Dlanguage=Python%d' % python_version, '-visitor', '-lib', ADQL_SRC]

    print('building adql lexer for python%i' % python_version)
    subprocess.check_call(args + [os.path.join(ADQL_SRC, 'ADQLLexer.g4')])

    print('building adql parser for python%i' % python_version)
    subprocess.check_call(args + [os.path.join(ADQL_SRC, 'ADQLParser.g4')])

    directory = os.path.join('lib', 'python2' if python_version < 3 else 'python3', 'queryparser/adql')
    try:
        os.makedirs(directory)
    except OSError:
        pass

    for filename in ['ADQLLexer.py', 'ADQLParser.py', 'ADQLParserListener.py', 'ADQLParserVisitor.py']:
        source = os.path.join(ADQL_SRC, filename)
        target = os.path.join(directory, filename)

        print('moving %s -> %s' % (source, target))
        shutil.move(source, target)

    os.remove(os.path.join(ADQL_SRC, 'ADQLLexer.tokens'))
    os.remove(os.path.join(ADQL_SRC, 'ADQLParser.tokens'))


if __name__ == "__main__":
    main()
