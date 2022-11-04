# -*- coding: utf-8 -*-
import re
import sys

from setuptools import setup

python_version = sys.version_info.major

with open('lib/queryparser/__init__.py') as f:
    metadata = dict(re.findall(r'__(.*)__ = [\']([^\']*)[\']', f.read()))

with open('requirements.txt') as f:
    requirements = f.readlines()

# work around for python 3.4 and antlr4-python3-runtime
if sys.version_info.major == 3 and sys.version_info.minor < 5:
    requirements += ['typing']

setup(
    name='queryparser-python3',
    version=metadata['version'],
    author=metadata['author'],
    author_email=metadata['email'],
    maintainer=metadata['author'],
    maintainer_email=metadata['email'],
    license=metadata['license'],
    url='https://github.com/aipescience/queryparser',
    description=u'Parses PostgreSQL/MySQL and translates ADQL to ' +\
            'PostgreSQL/MySQL.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=requirements,
    classifiers=[],
    packages=[
        'queryparser',
        'queryparser.adql',
        'queryparser.common',
        'queryparser.mysql',
        'queryparser.postgresql',
        'queryparser.exceptions'
    ],
    package_dir={
        '': 'lib'
    },
    include_package_data=True
)
