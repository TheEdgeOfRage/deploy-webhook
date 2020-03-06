#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD 3-Clause license.

from . import api


@api.route('/healthcheck', methods=['GET'])
def healthcheck():
	"""
	Healthcheck route

	:resjson string msg: status message

	:statuscode 200: Started deploy
	"""

	return {'msg': 'OK'}, 200
