#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018  Jun Makii <junmakii@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""Utilities, tools, and scripts for Python.

umuus-rest-utils
================

Installation
------------

    $ pip install git+https://github.com/junmakii/umuus-rest-utils.git

Example
-------

    $ umuus_rest_utils

    >>> import umuus_rest_utils

Usage
-----

    $ python -m umuus_rest_utils run --rest_server '{"module": "MY_MODULE", "host": "0.0.0.0", "port": 8021, "options": {"certfile": "server.crt", "keyfile": "server.key"}}'

Authors
-------

- Jun Makii <junmakii@gmail.com>

License
-------

GPLv3 <https://www.gnu.org/licenses/>

"""
import os
import sys
import json
import types
import functools
import importlib
import logging
logger = logging.getLogger(__name__)
import inspect
import attr
import umuus_utils
import flask
import gunicorn.app.base
__version__ = '0.1'
__url__ = 'https://github.com/junmakii/umuus-rest-utils'
__author__ = 'Jun Makii'
__author_email__ = 'junmakii@gmail.com'
__author_username__ = 'junmakii'
__keywords__ = []
__license__ = 'GPLv3'
__scripts__ = []
__install_requires__ = [
    'attrs>=18.2.0',
    'fire>=0.1.3',
    'gunicorn>=19.9.0',
    'umuus-utils@git+https://github.com/junmakii/umuus-utils.git#egg=umuus_utils-1.0',
]
__dependency_links__ = []
__classifiers__ = []
__entry_points__ = {
    'console_scripts': ['umuus_rest_utils = umuus_rest_utils:main'],
    'gui_scripts': [],
}
__project_urls__ = {}
__setup_requires__ = []
__test_suite__ = ''
__tests_require__ = []
__extras_require__ = {}
__package_data__ = {}
__python_requires__ = ''
__include_package_data__ = True
__zip_safe__ = True
__static_files__ = {}
__extra_options__ = {}
__download_url__ = ''
__all__ = []


def json_encode_value(s):
    try:
        return json.loads(s)
    except Exception:
        return str(s)


def json_encode(d):
    """

>>> json_encode({"a": {"b": "1", "c": type('Object', (), {})}})
{'a': {'b': 1, 'c': "<class '__main__.Object'>"}}

    """
    if isinstance(d, (list, tuple)):
        return type(d)(json_encode_value(_) for _ in d)
    elif isinstance(d, dict):
        store = {}
        for key, value in d.items():
            store[key] = json_encode(value)
        return store
    elif isinstance(d, (bool, float, int, type(None))):
        return d
    elif hasattr(d, '__attrs_attrs__'):
        return json_encode(attr.asdict(d))
    else:
        return json_encode_value(d)


def wrapper(fn=None):
    if not fn:
        return functools.partial(fn)
    spec = inspect.getfullargspec(fn)

    @functools.wraps(fn)
    def _wrapper(*args, **kwargs):
        try:
            params = json_encode(
                dict([(key, value)
                      for key, value in (list(flask.request.args.items()) +
                                         list(flask.request.form.items()))
                      if key in spec.args or spec.varkw]))
            logger.info('Request parameters: %r' % params)
            response = json.dumps(dict(data=json_encode(fn(**params))))
            return flask.Response(
                response,
                content_type='application/json',
                headers={'Access-Control-Allow-Origin': '*'})
        except Exception as err:
            return flask.Response(
                json.dumps(dict(error=str(err))),
                content_type='application/json',
                status=500,
            )

    return _wrapper


@attr.s()
class RestServer(object):
    """

flask.Flask.__init__ = __init__(self, import_name, static_url_path=None, static_folder='static', static_host=None, host_matching=False, subdomain_matching=False, template_folder='templates', instance_path=None, instance_relative_config=False, root_path=None)

    Initialize self.  See help(type(self)) for accurate signature.

    """
    host = attr.ib('localhost')
    port = attr.ib(0)
    options = attr.ib({
        'bind': '',
        'workers': 1,
    })
    debug = attr.ib(True)
    module = attr.ib(None)
    module_object = attr.ib(None)
    static_folder = attr.ib(None)
    static_url_path = attr.ib('')

    def __attrs_post_init__(self):
        self.options['bind'] = (self.options.get('bind')
                                or '%s:%d' % (self.host, self.port))
        self.module_object = (self.module_object
                              or importlib.import_module(self.module))
        self.static_folder = (self.static_folder or os.path.abspath('.'))
        self.app = flask.Flask(
            import_name=self.module_object.__name__,
            static_folder=self.static_folder,
            static_url_path=self.static_url_path,
        )
        self.functions = {
            '/' + key: value
            for key, value in vars(self.module_object).items()
            if isinstance(value, types.FunctionType)
        }
        logger.info(self.functions)
        for key, value in self.functions.items():
            self.app.route(key)(wrapper(value))

    def run(self):
        _self = self
        self.gunicorn_app = type(
            'GunicornApplication',
            (gunicorn.app.base.BaseApplication,),
            dict(
                options=self.options,
                load_config=lambda self: [
                    self.cfg.set(key, value)
                    for key, value in self.options.items()
                ],
                load=lambda self: _self.app.wsgi_app,
            ))
        self.gunicorn_app().run()
        # self.httpd = wsgiref.simple_server.make_server(
        #     app=self.app,
        #     host=self.host,
        #     port=self.port,
        # )
        # if self.certfile and self.keyfile:
        #     self.httpd.socket = ssl.wrap_socket(

#         self.httpd.socket,
#         certfile=self.certfile,
#         keyfile=self.keyfile,
#         # ca_certs='',
#         server_side=True,
#     )
# logger.info(self.httpd.server_address)
# self.httpd.serve_forever(poll_interval=0.5)


@umuus_utils.decorator()
def run(rest_server: RestServer):  # type: None
    rest_server.run()
    return


def main(argv=None):
    umuus_utils.main(name=__name__)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
