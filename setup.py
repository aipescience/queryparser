import sys

from setuptools import setup

version = '0.1'

python_version = sys.version_info.major

author = u'Gal Matijevic'
author_email = u'gmatijevic@aip.de'

setup(
    name='queryparser-python%d' % python_version,
    version=version,
    description='Parses MySQL and translates ADQL to MySQL.',
    long_description=open('README.rst').read(),
    url='https://github.com/aipescience/queryparser',
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    license=u'Apache License (2.0)',
    packages=[
        'queryparser',
        'queryparser.adql',
        'queryparser.mysql',
        'queryparser.examples'
    ],
    install_requires=[
        'wheel',
        'antlr4_python%d_runtime' % python_version
    ],
    classifiers=[],
    package_dir={
        '': 'lib/python%d' % python_version,
    },
)
