#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import subprocess

try:
    from setuptools import setup
    setup
except ImportError:
    from distutils.core import setup
    setup


def get_java_version():
    try:
        jp = subprocess.Popen(['java', '-version'], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        jo = jp.communicate()[1].decode('utf-8')
        return re.findall('java version "(.+)"', jo)
    except OSError:
        return []


def find_antlr():
    dirs = ['/usr/local/lib', '/usr/local/bin']
    for d in dirs:
        p = os.path.join(d, 'antlr-4.5.3-complete.jar')
        if os.path.exists(p):
            return p
        else:
            return None


def build_mysql_parser(antlr_path, major):
    ca = ['java', '-jar', antlr_path, '-Dlanguage=Python%d' % major, '-lib',
          'queryparser/mysql']
    print('building mysql lexer')
    subprocess.call(ca + ["./queryparser/mysql/MySQLLexer.g4"])
    print('building mysql parser')
    subprocess.call(ca + ["./queryparser/mysql/MySQLParser.g4"])


def build_adql_translator(antlr_path, major):
    ca = ['java', '-jar', antlr_path, '-Dlanguage=Python%d' % major,
          '-visitor', '-lib', 'queryparser/adql']
    print('building adql lexer')
    subprocess.call(ca + ["./queryparser/adql/ADQLLexer.g4"])
    print('building adql parser')
    subprocess.call(ca + ["./queryparser/adql/ADQLParser.g4"])


jv = get_java_version()

if not len(jv):
    raise RuntimeError("No Java found.")

try:
    if int(jv[0].split('.')[1]) < 7:
        raise RuntimeError("You need a newer version of Java.")
except (AttributeError, IndexError):
    print('No Java found.')
    raise

antlr_path = find_antlr()
if antlr_path is None:
    raise RuntimeError("Please download Antlr4.")

major, _, _, _, _ = sys.version_info

build_mysql_parser(antlr_path, major)
build_adql_translator(antlr_path, major)

setup(
    name="queryparser",
    version="0.0.1",
    author="Gal Matijevic / AIP",
    author_email="gmatijevic@aip.de",
    packages=["queryparser", "queryparser.adql", "queryparser.mysql",
              "queryparser.examples"],
    license="MIT",
    description="Parses MySQL and does some other stuff...",
    include_package_data=True,
    install_requires=["antlr4_python%d_runtime" % major]
)
