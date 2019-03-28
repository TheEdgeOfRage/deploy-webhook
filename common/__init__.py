#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

from flask import Flask
from os import environ

from .config import configs


def create_app(package_name=__name__):
	app = Flask(package_name)
	config = configs.get(environ.get('FLASK_ENV', 'production'))
	app.config.from_object(config)

	return app

