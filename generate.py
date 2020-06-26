#!/usr/bin/env python

import argparse
import os
import shutil
import subprocess
import re

ANTLR_JAR = 'antlr-4.8-complete.jar'
ANTLR_DIRS = ('.', '/usr/local/lib/', '/usr/local/bin/')

QUERYPARSER_SRC = 'src/queryparser/'
MYSQL_SRC = 'src/queryparser/mysql'
POSTGRESQL_SRC = 'src/queryparser/postgresql'
ADQL_SRC = 'src/queryparser/adql'


def main():
    parser = argparse.ArgumentParser(description='Generate the parsers.')
    parser.add_argument('-l', help='language (ADQL / MySQL / PostgreSQL)')

    args = parser.parse_args()

    languages = [args.l] if args.l else ['adql', 'mysql', 'postgresql']

    if get_java_version() < 7:
        raise RuntimeError('You need a newer version of Java.')

    antlr_path = get_antlr_path()
    if not antlr_path:
        raise RuntimeError('You need %s installed in %s.'
                           % (ANTLR_JAR, ':'.join(ANTLR_DIRS)))

    for language in languages:
        if language == 'adql':
            build_adql_translator(antlr_path)

        if language == 'mysql':
            build_mysql_parser(antlr_path)

        if language == 'postgresql':
            build_postgresql_parser(antlr_path)


def get_java_version():
    try:
        args = ['java', '-version']
        output = subprocess.check_output(args, stderr=subprocess.STDOUT)
        match = re.search('version \"(\d+).(\d+).(.*?)\"',
                          output.decode('utf-8'))
        if match:
            ver = int(match.group(2))
            if ver == 0:
                ver = int(match.group(1))
            return ver
    except OSError:
        pass

    raise RuntimeError('No java version found.')


def get_antlr_path():
    for directory in ANTLR_DIRS:
        path = os.path.join(directory, ANTLR_JAR)
        if os.path.exists(path):
            return path
    return False


def build_mysql_parser(antlr_path):
    args = ['java', '-jar', antlr_path, '-Dlanguage=Python3',
            '-lib', MYSQL_SRC]

    print('building mysql lexer')
    subprocess.check_call(args + [os.path.join(MYSQL_SRC, 'MySQLLexer.g4')])

    print('building mysql parser')
    subprocess.check_call(args + [os.path.join(MYSQL_SRC, 'MySQLParser.g4')])

    directory = os.path.join('lib', 'queryparser/mysql')

    try:
        os.makedirs(directory)
    except OSError:
        pass

    for filename in ['MySQLLexer.py', 'MySQLParser.py',
                     'MySQLParserListener.py']:
        source = os.path.join(MYSQL_SRC, filename)
        target = os.path.join(directory, filename)

        print('moving %s -> %s' % (source, target))
        shutil.move(source, target)

    os.remove(os.path.join(MYSQL_SRC, 'MySQLLexer.tokens'))
    os.remove(os.path.join(MYSQL_SRC, 'MySQLParser.tokens'))


def build_postgresql_parser(antlr_path):
    args = ['java', '-jar', antlr_path, '-Dlanguage=Python3',
            '-lib', POSTGRESQL_SRC]

    print('building postgresql lexer')
    subprocess.check_call(args + [os.path.join(POSTGRESQL_SRC,
        'PostgreSQLLexer.g4')])

    print('building postgresql parser')
    subprocess.check_call(args + [os.path.join(POSTGRESQL_SRC,
        'PostgreSQLParser.g4')])

    directory = os.path.join('lib', 'queryparser/postgresql')

    try:
        os.makedirs(directory)
    except OSError:
        pass

    for filename in ['PostgreSQLLexer.py', 'PostgreSQLParser.py',
                     'PostgreSQLParserListener.py']:
        source = os.path.join(POSTGRESQL_SRC, filename)
        target = os.path.join(directory, filename)

        print('moving %s -> %s' % (source, target))
        shutil.move(source, target)

    os.remove(os.path.join(POSTGRESQL_SRC, 'PostgreSQLLexer.tokens'))
    os.remove(os.path.join(POSTGRESQL_SRC, 'PostgreSQLParser.tokens'))


def build_adql_translator(antlr_path):
    args = ['java', '-jar', antlr_path, '-Dlanguage=Python3',
            '-visitor', '-lib', ADQL_SRC]

    print('building adql lexer')
    subprocess.check_call(args + [os.path.join(ADQL_SRC, 'ADQLLexer.g4')])

    print('building adql parser')
    subprocess.check_call(args + [os.path.join(ADQL_SRC, 'ADQLParser.g4')])

    directory = os.path.join('lib', 'queryparser/adql')

    try:
        os.makedirs(directory)
    except OSError:
        pass

    for filename in ['ADQLLexer.py', 'ADQLParser.py', 'ADQLParserListener.py',
                     'ADQLParserVisitor.py']:
        source = os.path.join(ADQL_SRC, filename)
        target = os.path.join(directory, filename)

        print('moving %s -> %s' % (source, target))
        shutil.move(source, target)

    os.remove(os.path.join(ADQL_SRC, 'ADQLLexer.tokens'))
    os.remove(os.path.join(ADQL_SRC, 'ADQLParser.tokens'))


if __name__ == "__main__":
    main()
