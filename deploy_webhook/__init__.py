#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from os import environ

from .commands import register_commands
from .config import configs, configure_logging


db = SQLAlchemy()


def create_app(package_name=__name__):
	app = Flask(package_name)
	config_class = configs.get(environ.get('FLASK_ENV', 'production'))
	app.config.from_object(config_class)
	configure_logging(app)
	CORS(app)
	JWTManager(app)
	db.init_app(app)
	Migrate(app, db)
	register_commands(app)

	from .api import api as api_bp
	app.register_blueprint(api_bp, url_prefix='/api')

	from .api import tasks
	app.before_first_request(tasks.before_first_request)

	from .errors import register_error_handlers
	register_error_handlers(app)

	return app
