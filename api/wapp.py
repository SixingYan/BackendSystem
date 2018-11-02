#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import environ as env

#import redis
import toml
import traceback
from flask import Flask, jsonify, g, request
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.utils import import_string
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions

from moretime.config import configure
from moretime.api.json_encoder import MyJSONEncoder
from moretime.api.response import ErrorResponse
from moretime.api.signature import verify_signature
from moretime.api.logger import setup_logging
from moretime.base.auth import parse_token
from moretime.entity import Facade as EntityFacade
from moretime.orm import Facade as ModelFacade
from moretime.orm import user as user_model

from moretime.wrong import error

# 日志
logworker = setup_logging()


def initialize_facade(config):

    EntityFacade.config = config

    ModelFacade.initialize(EntityFacade.config["mysql"])


def handle_error(exc):
    code = 500
    if isinstance(exc, HTTPException):
        code = exc.code

    traceback.print_exc()

    data = dict(
        error=str(exc),
        code=code
    )
    return jsonify(ErrorResponse(error.UnknownError, data=data))


blueprints = [
    "api.moretime:blueprint",
]


def create_app():
    app = Flask(__name__, static_folder=None)
    app.json_encoder = MyJSONEncoder

    # config
    config = configure.get_common_config()

    # blueprints
    for blueprint_qualname in blueprints:
        blueprint = import_string(blueprint_qualname)
        app.register_blueprint(blueprint)

    # Initilize facades
    initialize_facade(config)

    # Initialize Sentry
    from raven.contrib.flask import Sentry
    Sentry(app, dsn="http://xxxxxxxxxxxx:xxxxxxxxxxxx@e.moremom.cn/2")

    # Set exception handler
    for code in default_exceptions:
        app.register_error_handler(code, handle_error)

    return app


app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.before_request
def make_db_session():
    g.db = ModelFacade.make_scoped_session()


@app.before_request
def validate_token():
    request.current_user = None
    request.current_user_id = None
    request.current_token = None
    token = request.headers.get('token', None)
    user_id = int(request.headers.get("X-User-Id", 0))
    if user_id != 0:
        m_user = user_model.find_user_by_id(g.db, user_id)
        if m_user is not None:
            request.current_user = m_user
            request.current_user_id = user_id
            request.current_token = token
            logworker.warning(request.current_user_id)
            logworker.warning(request.args)
            logworker.warning(request.json) 
    

@app.after_request
def release_db_session(response):
    if hasattr(g, "db"):
        ModelFacade.release_session(g.db)
    return response

# 需要跨域访问的 API, 用于 H5页面分享
CORS_URLS = ["/v1/moretime/poster/reply", ]


@app.after_request
def add_cors_headers(response):
    if request.path in CORS_URLS:  # poster 分享页
        response.headers['Access-Control-Allow-Origin'] = '*'
        if request.method == 'OPTIONS':
            response.headers[
                'Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers

    return response
