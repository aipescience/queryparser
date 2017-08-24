import sys

from setuptools import setup

sys.path.append('src')

from queryparser import __title__, __email__, __version__, __author__, __license__

python_version = sys.version_info.major

name = '%s-python%d' % (__title__ ,python_version)

requirements = [
    'pytest',
    'coverage',
    'antlr4_python%d_runtime' % python_version
]

# work around for python 3.4 and antlr4-python3-runtime
if sys.version_info.major == 3 and sys.version_info.minor < 5:
    requirements += ['typing']

setup(
    name=name,
    version=__version__,
    author=__author__,
    author_email=__email__,
    maintainer=__author__,
    maintainer_email=__email__,
    license=__license__,
    url='https://github.com/aipescience/queryparser',
    description=u'Parses MySQL and translates ADQL to MySQL.',
    long_description=open('README.rst').read(),
    install_requires=requirements,
    classifiers=[],
    packages=[
        'queryparser',
        'queryparser.adql',
        'queryparser.mysql'
    ],
    package_dir={
        '': 'lib/python%d' % python_version
    },
    include_package_data=True
)
