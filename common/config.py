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
	SIGNATURE_SECRET = None


class DevConfig(BaseConfig):
	DEBUG = True
	TESTING = True
	SIGNATURE_SECRET = environ.get('SIGNATURE_SECRET', 'default-secret')


class TestConfig(BaseConfig):
	DEBUG = True
	TESTING = True
	SIGNATURE_SECRET = environ.get('SIGNATURE_SECRET', 'default-secret')


class ProdConfig(BaseConfig):
	DEBUG = False
	TESTING = False
	SIGNATURE_SECRET = environ.get('SIGNATURE_SECRET', None)


configs = {
	'development': DevConfig,
	'testing': TestConfig,
	'production': ProdConfig,
}

