#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from flask import request
from flask_jwt_extended import (
	create_access_token,
	create_refresh_token,
	jwt_refresh_token_required,
	jwt_required,
	get_jwt_identity,
)
from sqlalchemy.exc import IntegrityError, OperationalError

from . import api
from .. import db
from ..models import User
from ..schemas import user_schema


@api.route('/signup', methods=['POST'])
@jwt_required
def create_user():
	"""
	Create a new user in the database.

	:reqheader Authorization: valid JWT access token
	:reqheader Content-Type: application/json
	:reqjson string username: unique username
	:reqjson string password: no requirements

	:resjson string msg: status message
	:resjson string err: error message
	:resjson User user: new user data

	:statuscode 201: user created
	:statuscode 400: missing parameter
	:statuscode 409: username taken
	"""

	username = request.json['username']
	password = request.json['password']
	if None in (username, password):
		return {'err': 'Missing parameter'}, 400

	user = User(username=username, password=password)
	try:
		db.session.add(user)
		db.session.commit()
	except IntegrityError:
		db.session.rollback()
		return {
			'err': 'Username taken',
		}, 409

	return {
		'msg': 'User created',
		'user': user_schema.dump(user),
	}, 201


@api.route('/login', methods=['POST'])
def login():
	"""
	Authenticate with a username and password to receive a JWT access and
	refresh token.

	:reqheader Authorization: valid JWT access token
	:reqheader Content-Type: application/json
	:reqjson string username: unique username
	:reqjson string password: no requirements

	:resjson string acces_token: JWT access token
	:resjson string refresh_token: JWT refresh token
	:resjson string err: error message
	:resjson User user: new user data

	:statuscode 200: authentication successful
	:statuscode 400: missing parameter
	:statuscode 401: bad credentials
	"""

	if not request.is_json:
		return {'err': 'Request is not JSON'}, 400

	username = request.json.get('username', None)
	password = request.json.get('password', None)
	if None in (username, password):
		return {'err': 'Missing parameter'}, 400

	try:
		user = User.query.filter_by(username=username).first()
	except OperationalError as e:
		return {'err': 'Internal error', 'msg': str(e)}, 500

	if user is None or not user.verify_password(password):
		return {'err': 'Wrong username or password'}, 401

	ret = {
		'access_token': create_access_token(identity=username),
		'refresh_token': create_refresh_token(identity=username)
	}

	return ret, 200


@api.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
	"""
	Refresh an old JWT access token using a valid refresh token.

	:reqheader Authorization: valid JWT refresh token

	:resjson string acces_token: JWT access token

	:statuscode 200: authentication successful
	"""

	current_username = get_jwt_identity()

	return {
		'access_token': create_access_token(identity=current_username)
	}, 200
