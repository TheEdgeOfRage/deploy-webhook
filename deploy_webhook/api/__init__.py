#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from flask import Blueprint

api = Blueprint('api', __name__)

from . import (  # noqa
	auth,
	containers,
	deploy,
	healthcheck,
	services,
	tasks,
)
