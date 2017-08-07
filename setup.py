import os
import shutil
import subprocess
import sys
import re

from distutils.command.build_py import build_py as distutils_build_py
from distutils.core import setup

version = '0.1.0'

python_version, _, _, _, _ = sys.version_info


class build_py(distutils_build_py):

    antlr_jar = 'antlr-4.7-complete.jar'
    antlr_dirs = ('/usr/local/lib/', '/usr/local/bin/')

    def run(self):
        if self._get_java_version() < 7:
            raise RuntimeError('You need a newer version of Java.')

        antlr_path = self._get_antlr_path()
        if not antlr_path:
            raise RuntimeError('You need Antlr 4.7 installed in %s.' % ':'.join(self.antlr_dirs))

        self._build_mysql_parser(antlr_path)
        self._build_adql_translator(antlr_path)

        # regular build, aka. copy the files into the build directory
        distutils_build_py.run(self)

    def _get_java_version(self):
        try:
            args = ['java', '-version']
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            match = re.search('version \"(\d+).(\d+).(.*?)\"', output.decode('utf-8'))
            if match:
                return int(match.group(2))
        except OSError:
            pass

        raise RuntimeError('No java version found.')

    def _get_antlr_path(self):
        for directory in self.antlr_dirs:
            path = os.path.join(directory, self.antlr_jar)
            if os.path.exists(path):
                return path
        return False

    def _build_mysql_parser(self, antlr_path):
        args = ['java', '-jar', antlr_path, '-Dlanguage=Python%d' % python_version,
            '-lib', 'queryparser/mysql']

        print('building mysql lexer')
        subprocess.call(args + ['queryparser/mysql/MySQLLexer.g4'])

        print('building mysql parser')
        subprocess.call(args + ['queryparser/mysql/MySQLParser.g4'])

    def _build_adql_translator(self, antlr_path):
        args = ['java', '-jar', antlr_path, '-Dlanguage=Python%d' % python_version,
            '-visitor', '-lib', 'queryparser/adql']

        print('building adql lexer')
        subprocess.call(args + ['queryparser/adql/ADQLLexer.g4'])

        print('building adql parser')
        subprocess.call(args + ['queryparser/adql/ADQLParser.g4'])

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
        'queryparser.mysql',
        'queryparser.examples'
    ],
    install_requires=[
        'wheel',
        'antlr4_python%d_runtime' % python_version
    ],
    download_url='https://github.com/aipescience/queryparser/archive/%s.tar.gz' % version,
    classifiers=[],
    cmdclass={
        'build_py': build_py
    }
)
