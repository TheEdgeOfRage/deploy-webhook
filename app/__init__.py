#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from flask import Blueprint, Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from os import environ

from .api import tasks
from .api import api
from .commands import register_commands
from .config import configs
from .db import init_db


def register_blueprint(app, package_name):
	api_blueprint = Blueprint('api', package_name)
	api.init_app(api_blueprint)
	app.register_blueprint(api_blueprint, url_prefix='/api')


def create_app(package_name=__name__):
	app = Flask(package_name)
	config = configs.get(environ.get('FLASK_ENV', 'production'))
	app.config.from_object(config)

	CORS(app)
	JWTManager(app)
	init_db(app)
	register_blueprint(app, package_name)
	register_commands(app)
	app.before_first_request(tasks.before_first_request)

	return app

