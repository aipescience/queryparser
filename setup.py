import sys

from setuptools import setup

version = '0.1.2'

python_version = sys.version_info.major

author = u'Gal Matijevic'
author_email = u'gmatijevic@aip.de'

packages = [
    'queryparser',
    'queryparser.adql',
    'queryparser.mysql'
]

package_dir = {
    '': 'lib/python%d' % python_version
}

requirements = [
    'pytest',
    'coverage',
    'antlr4_python%d_runtime' % python_version
]
print (requirements)
# work around for python 3.4 and antlr4-python3-runtime
if sys.version_info.major == 3 and sys.version_info.minor < 5:
    requirements += ['typing']

classifiers = []

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
    packages=packages,
    install_requires=requirements,
    classifiers=classifiers,
    package_dir=package_dir,
)
