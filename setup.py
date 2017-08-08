import sys

from distutils.core import setup

version = '0.1.0'

python_version, _, _, _, _ = sys.version_info

setup(
    name='queryparser',
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
        'queryparser.adql.two',
        'queryparser.adql.three',
        'queryparser.mysql',
        'queryparser.mysql.two',
        'queryparser.mysql.three',
        'queryparser.examples'
    ],
    install_requires=[
        'wheel',
        'antlr4_python%d_runtime' % python_version
    ],
    download_url='https://github.com/aipescience/queryparser/archive/%s.tar.gz' % version,
    classifiers=[],
)
