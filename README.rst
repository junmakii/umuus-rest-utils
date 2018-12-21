
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

    $ python -m umuus_rest_utils run --rest_server '{"module": "MY_MODULE", "host": "0.0.0.0", "port": 8021, "options": {"certfile": "server.crt", "keyfile": "server.key"}, "auth_database_options": {"url": "http://couchdb:5984"}}'

Without basic auth:

    $ python -m umuus_rest_utils run --rest_server '{"module": "MY_MODULE", "host": "0.0.0.0", "port": 8021, "options": {"certfile": "server.crt", "keyfile": "server.key"}}'

Authors
-------

- Jun Makii <junmakii@gmail.com>

License
-------

GPLv3 <https://www.gnu.org/licenses/>