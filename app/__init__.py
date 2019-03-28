#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

from flask import Blueprint

from .api import api


def create_blueprint():
	api_blueprint = Blueprint('api', __name__)
	api.init_app(api_blueprint)

	return api_blueprint

