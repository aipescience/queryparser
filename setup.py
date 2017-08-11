import sys

from setuptools import setup

version = '0.1.0'

python_version = sys.version_info.major

setup(
    name='queryparser-python%d' % python_version,
    version=version,
    description='Parses MySQL and translates ADQL to MySQL.',
    url='https://github.com/aipescience/queryparser',
    author='Gal Matijevic',
    author_email='gmatijevic@aip.de',
    maintainer=u'AIP E-Science',
    maintainer_email=u'escience@aip.de',
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
