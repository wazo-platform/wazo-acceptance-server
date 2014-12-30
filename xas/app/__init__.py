# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Avencall
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging
import os
import sys
import urllib

from flask import Flask
from flask import request
from flask_restless import APIManager
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from gevent.wsgi import WSGIServer
import pkg_resources
from xivo import wsgi


logger = logging.getLogger(__name__)


class FlaskConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://asterisk:proformatique@localhost/asterisk'


def main(config):
    app = Flask('xas')
    app.config.from_object(FlaskConfig)
    db = SQLAlchemy(app)

    manager = APIManager(app, flask_sqlalchemy_db=db)

    @app.before_request
    def log_requests():
        params = {
            'method': request.method,
            'url': urllib.unquote(request.url).decode('utf8')
        }
        if request.data:
            params.update({'data': request.data})
            logger.info("%(method)s %(url)s with data %(data)s ", params)
        else:
            logger.info("%(method)s %(url)s", params)

    logger.debug(app.url_map)

    environ = {
        'wsgi.multithread': True,
    }
    http_server = WSGIServer(listener=(config['rest_api']['listen'], config['rest_api']['port']),
                             application=app,
                             environ=environ)

    logger.debug('WSGIServer starting... uid: %s, listen: %s:%s',
                 os.getuid(),
                 config['rest_api']['listen'],
                 config['rest_api']['port'])

    http_server.serve_forever()


if __name__ == "__main__":
    main()
