#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

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
	SIGNATURE_SECRET = environ.get('SIGNATURE_SECRET', 'default-secret')
	SECRET_KEY = environ.get('SECRET_KEY', 'default-secret')
	SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI ', 'sqlite:////tmp/auth.db')


class TestConfig(BaseConfig):
	DEBUG = True
	TESTING = True
	SIGNATURE_SECRET = environ.get('SIGNATURE_SECRET', 'default-secret')
	SECRET_KEY = environ.get('SECRET_KEY', 'default-secret')
	SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI ', 'sqlite:////tmp/auth.db')


class ProdConfig(BaseConfig):
	DEBUG = False
	TESTING = False
	SIGNATURE_SECRET = environ.get('SIGNATURE_SECRET', None)
	SECRET_KEY = environ.get('SECRET_KEY', None)
	SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI ', None)


class DockerConfig(BaseConfig):
	DEBUG = False
	TESTING = False
	SIGNATURE_SECRET = environ.get('SIGNATURE_SECRET', None)
	SECRET_KEY = environ.get('SECRET_KEY', None)
	SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI ', 'sqlite:////data/auth.db')


configs = {
	'development': DevConfig,
	'testing': TestConfig,
	'production': ProdConfig,
	'docker': DockerConfig,
}

