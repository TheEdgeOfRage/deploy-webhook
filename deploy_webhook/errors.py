#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD 3-Clause license.

from flask.json import jsonify

from . import db


def _page_not_found(e):
	return {'err': 'URL not found'}, 404


def _method_not_allowed(e):
	response = jsonify({'err': 'Method not allowed'})
	response.status_code = 405
	response.headers.set('Allow', ', '.join(e.valid_methods))

	return response


def _internal_server_error(e):
	db.session.rollback()

	return {'err': 'Internal server error'}, 500


def register_error_handlers(app):
	app.register_error_handler(404, _page_not_found)
	app.register_error_handler(405, _method_not_allowed)
	app.register_error_handler(500, _internal_server_error)
