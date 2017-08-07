import sys
import subprocess
import re

from distutils.command.build_py import build_py as distutils_build_py
from distutils.core import setup

version = '0.1.0'

python_version, _, _, _, _ = sys.version_info

# def get_java_version():
#     try:
#         cmd = """java -version 2>&1 | awk '/version/ {print $3}'"""
#         output = subprocess.check_output(cmd,  shell=True)

#         return  output.decode('utf-8').strip('\n').strip('"')
#     except OSError:
#         return []

# def find_antlr():
#     dirs = ['/usr/local/lib', '/usr/local/bin']
#     for d in dirs:
#         p = os.path.join(d, 'antlr-4.7-complete.jar')
#         if os.path.exists(p):
#             return p



class build_py(distutils_build_py):

    def run(self):

        if self._get_java_version() < 7:
            raise RuntimeError('You need a newer version of Java.')

        super(build_py, self).run()

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

# def find_antlr():
#     dirs = ['/usr/local/lib', '/usr/local/bin']
#     for d in dirs:
#         p = os.path.join(d, 'antlr-4.7-complete.jar')
#         if os.path.exists(p):
#             return p


# def build_mysql_parser(antlr_path, major):
#     ca = ['java', '-jar', antlr_path, '-Dlanguage=Python%d' % major, '-lib',
#           'queryparser/mysql']
#     print('building mysql lexer')
#     subprocess.call(ca + ["./queryparser/mysql/MySQLLexer.g4"])
#     print('building mysql parser')
#     subprocess.call(ca + ["./queryparser/mysql/MySQLParser.g4"])


# def build_adql_translator(antlr_path, major):
#     ca = ['java', '-jar', antlr_path, '-Dlanguage=Python%d' % major,
#           '-visitor', '-lib', 'queryparser/adql']
#     print('building adql lexer')
#     subprocess.call(ca + ["./queryparser/adql/ADQLLexer.g4"])
#     print('building adql parser')
#     subprocess.call(ca + ["./queryparser/adql/ADQLParser.g4"])


# jv = get_java_version()

# if not len(jv):
#     raise RuntimeError("No Java found.")

# try:
#     if int(jv.split('.')[1]) < 7:
#         raise RuntimeError("You need a newer version of Java.")
# except (AttributeError, IndexError):
#     print('No Java found.')
#     raise

# antlr_path = find_antlr()
# if antlr_path is None:
#     raise RuntimeError("Please download Antlr4.")

# major, _, _, _, _ = sys.version_info

# build_mysql_parser(antlr_path, major)
# build_adql_translator(antlr_path, major)
