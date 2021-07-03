import logging
import sys

from flask import Blueprint
from flask import request
from flask_cors import cross_origin

from app.services import (
    HelloWorldService,
    LoginService
)

from app.routes import json_response

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)

API = Blueprint('jeeter', __name__, url_prefix='')


@API.route('/healthcheck', methods=['GET'])
@cross_origin()
def health_check():
    LOG.info("Hit health check")
    return json_response('Ok')


@API.route('/hello_world', methods=['GET'])
@cross_origin()
def hello_world():
    response = HelloWorldService.handle_request(request)
    return json_response(response)


@API.route('/login', methods=['POST'])
@cross_origin()
def login():
    response = LoginService.handle_request(request)
    return json_response(response)