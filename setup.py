
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def run_tests(self):
        import sys
        import shlex
        import pytest
        errno = pytest.main(['--doctest-modules'])
        if errno != 0:
            raise Exception('An error occured during installution.')
        install.run(self)


setup(
    packages=setuptools.find_packages('.'),
    version='0.1',
    url='https://github.com/junmakii/umuus-rest-utils',
    author='Jun Makii',
    author_email='junmakii@gmail.com',
    keywords=[],
    license='GPLv3',
    scripts=[],
    install_requires=['attrs>=18.2.0',
 'fire>=0.1.3',
 'gunicorn>=19.9.0',
 'requests>=2.20.1',
 'umuus-utils@git+https://github.com/junmakii/umuus-utils.git#egg=umuus_utils-1.0'],
    dependency_links=[],
    classifiers=[],
    entry_points={'console_scripts': ['umuus_rest_utils = umuus_rest_utils:main'],
 'gui_scripts': []},
    project_urls={},
    setup_requires=[],
    test_suite='',
    tests_require=[],
    extras_require={},
    package_data={},
    python_requires='',
    include_package_data=True,
    zip_safe=True,
    name='umuus-rest-utils',
    description='Utilities, tools, and scripts for Python.',
    long_description=('Utilities, tools, and scripts for Python.\n'
 '\n'
 'umuus-rest-utils\n'
 '================\n'
 '\n'
 'Installation\n'
 '------------\n'
 '\n'
 '    $ pip install git+https://github.com/junmakii/umuus-rest-utils.git\n'
 '\n'
 'Example\n'
 '-------\n'
 '\n'
 '    $ umuus_rest_utils\n'
 '\n'
 '    >>> import umuus_rest_utils\n'
 '\n'
 'Usage\n'
 '-----\n'
 '\n'
 '    $ python -m umuus_rest_utils run --rest_server \'{"module": "MY_MODULE", '
 '"host": "0.0.0.0", "port": 8021, "options": {"certfile": "server.crt", '
 '"keyfile": "server.key"}, "auth_database_options": {"url": '
 '"http://couchdb:5984"}}\'\n'
 '\n'
 'Without basic auth:\n'
 '\n'
 '    $ python -m umuus_rest_utils run --rest_server \'{"module": "MY_MODULE", '
 '"host": "0.0.0.0", "port": 8021, "options": {"certfile": "server.crt", '
 '"keyfile": "server.key"}}\'\n'
 '\n'
 'Authors\n'
 '-------\n'
 '\n'
 '- Jun Makii <junmakii@gmail.com>\n'
 '\n'
 'License\n'
 '-------\n'
 '\n'
 'GPLv3 <https://www.gnu.org/licenses/>'),
    cmdclass={"pytest": PyTest},
)
