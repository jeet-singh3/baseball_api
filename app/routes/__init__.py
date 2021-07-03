import importlib
import os
import logging
import datetime

from flask import Flask
from flask import jsonify
from flask import json
from flask import Response
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import JWTManager
from flask_cors import CORS

JWT = None


def create_app(config=None, app_name=__name__):
    app = Flask(app_name, static_folder='docs')
    app.secret_key = 'random_series_of_characters'
    app.config['SESSION_TYPE'] = 'rest_api'
    app.config['SESSION_COOKIE_NAME'] = 'flask_api'
    app.config['SESSION_COOKIE_PATH'] = ''

    app.permanent_session_lifetime = datetime.timedelta(days=1)
    app.config.from_object(config)
    app.register_error_handler(Exception, handle_error)

    if config is not None:
        JWT = JWTManager(app)
        JWT.expired_token_loader(my_expired_token_callback)

    register_blueprints(app)
    CORS(app)

    return app


def register_blueprints(app):
    for dir_name in os.listdir('app'):
        module_name = '.' + dir_name
        module_path = os.path.join('app', dir_name, 'routes.py')
        if os.path.exists(module_path):
            module = importlib.import_module(module_name, __name__)
            api = getattr(module, 'API', None)
            api.url_prefix = '/api/v1' + api.url_prefix
            app.register_blueprint(api)


def handle_expired_token(error):
    status = 401
    message = error.response.get('Error', {'Message': 'internal server error'}).get('Message')
    logging.error(message)
    res = {
        'status': status,
        'message': 'Token has expired',
        'developer_text': message
    }
    return json_response(res, status_code=status)


def handle_error(error):
    if type(error).__name__ == 'ExpiredTokenException':
        return handle_expired_token(error)

    status = 500
    message = 'internal server error'

    if isinstance(error, HTTPException):
        status = error.code
        message = error.description

    logging.error(error)
    res = {
        'status': status,
        'message': message
    }
    return json_response(res, status_code=status)


def json_response(res, status_code=200):
    return Response(
        mimetype='application/json',
        response=json.dumps(res),
        status=status_code
    )


def json_error_response(error, status_code=500):
    return jsonify({
        'status': status_code,
        'message': error
    }), status_code


def my_expired_token_callback(token):
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'message': f"The token {token} has expired"
    }), 401
