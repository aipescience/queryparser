#!/usr/bin/env python

import os
import shutil
import subprocess
import sys
import re

version = '0.1.0'

python_version, _, _, _, _ = sys.version_info

ANTLR_JAR = 'antlr-4.7-complete.jar'
ANTLR_DIRS = ('/usr/local/lib/', '/usr/local/bin/')


def main():
    if get_java_version() < 7:
        raise RuntimeError('You need a newer version of Java.')

    antlr_path = get_antlr_path()
    if not antlr_path:
        raise RuntimeError('You need Antlr 4.7 installed in %s.' % ':'.join(ANTLR_DIRS))

    copy_source_files()
    build_mysql_parser(antlr_path)
    build_adql_translator(antlr_path)


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


def copy_source_files():
    shutil.rmtree('queryparser')
    shutil.copytree('src/queryparser', 'queryparser')


def build_mysql_parser(antlr_path):
    args = ['java', '-jar', antlr_path, '-Dlanguage=Python%d' % python_version,
        '-lib', 'queryparser/mysql']

    print('building mysql lexer')
    subprocess.call(args + ['queryparser/mysql/MySQLLexer.g4'])

    print('building mysql parser')
    subprocess.call(args + ['queryparser/mysql/MySQLParser.g4'])


def build_adql_translator(antlr_path):
    args = ['java', '-jar', antlr_path, '-Dlanguage=Python%d' % python_version,
        '-visitor', '-lib', 'queryparser/adql']

    print('building adql lexer')
    subprocess.call(args + ['queryparser/adql/ADQLLexer.g4'])

    print('building adql parser')
    subprocess.call(args + ['queryparser/adql/ADQLParser.g4'])


if __name__ == "__main__":
    main()
