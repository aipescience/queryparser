# -*- coding: utf-8 -*-

import sys

from setuptools import setup

python_version = sys.version_info.major

version = '0.2.3'

author = 'Gal Matijevic'
email = 'gmatijevic@aip.de'

requirements = [
    'pytest',
    'coverage',
    'antlr4_python%d_runtime' % python_version
]

# work around for python 3.4 and antlr4-python3-runtime
if sys.version_info.major == 3 and sys.version_info.minor < 5:
    requirements += ['typing']

setup(
    name='queryparser-python%d' % python_version,
    version=version,
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    license='Apache-2.0',
    url='https://github.com/aipescience/queryparser',
    description=u'Parses MySQL and translates ADQL to MySQL.',
    long_description=open('README.rst').read(),
    install_requires=requirements,
    classifiers=[],
    packages=[
        'queryparser',
        'queryparser.adql',
        'queryparser.mysql',
        'queryparser.exceptions'
    ],
    package_dir={
        '': 'lib/python%d' % python_version
    },
    include_package_data=True
)
