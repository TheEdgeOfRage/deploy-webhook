#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from logging.config import dictConfig
from os import environ


class BaseConfig:
	DEBUG = False
	TESTING = False
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_RECORD_QUERIES = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SIGNATURE_SECRET = None
	SECRET_KEY = None
	JWT_DECODE_LEEWAY = 10


class DevConfig(BaseConfig):
	DEBUG = True
	TESTING = True
	LOGGING_LEVEL = 'DEBUG'
	SIGNATURE_SECRET = environ.get('SIGNATURE_SECRET', 'default-secret')
	SECRET_KEY = environ.get('SECRET_KEY', 'default-secret')
	SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI ', 'sqlite:////tmp/auth.db')


class TestConfig(BaseConfig):
	DEBUG = True
	TESTING = True
	LOGGING_LEVEL = 'WARNING'
	SIGNATURE_SECRET = environ.get('SIGNATURE_SECRET', 'default-secret')
	SECRET_KEY = environ.get('SECRET_KEY', 'default-secret')
	SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI ', 'sqlite://')


class ProdConfig(BaseConfig):
	DEBUG = False
	TESTING = False
	LOGGING_LEVEL = 'WARNING'
	SIGNATURE_SECRET = environ.get('SIGNATURE_SECRET', None)
	SECRET_KEY = environ.get('SECRET_KEY', None)
	SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI ', None)


class DockerConfig(BaseConfig):
	DEBUG = False
	TESTING = False
	LOGGING_LEVEL = 'WARNING'
	SIGNATURE_SECRET = environ.get('SIGNATURE_SECRET', None)
	SECRET_KEY = environ.get('SECRET_KEY', None)
	SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI ', 'sqlite:////data/auth.db')


def configure_logging(app):
	dictConfig({
		'version': 1,
		'disable_existing_loggers': False,
		'formatters': {
			'default_formatter': {
				'format': '[%(asctime)s] %(levelname)-8s %(module)s: %(message)s',
				'datefmt': '%Y-%m-%dT%H:%M:%S%z',
			},
		},
		'handlers': {
			'default_handler': {
				'formatter': 'default_formatter',
				'class': 'logging.StreamHandler',
				#  'stream': 'ext://flask.logging.wsgi_errors_stream',
			},
		},
		'loggers': {
			'deploy_webhook': {
				'level': app.config.get('LOGGING_LEVEL'),
				'handlers': ['default_handler'],
				'propagate': False,
			},
			'servicectl': {
				'level': app.config.get('LOGGING_LEVEL'),
				'handlers': ['default_handler'],
				'propagate': False,
			},
		},
	})


configs = {
	'development': DevConfig,
	'testing': TestConfig,
	'production': ProdConfig,
	'docker': DockerConfig,
}
