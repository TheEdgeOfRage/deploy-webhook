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
	username = request.json['username']
	password = request.json['password']
	user = User(username=username, password=password)

	try:
		db.session.add(user)
		db.session.commit()
	except IntegrityError:
		db.session.rollback()
		return {
			'err': 'Username taken',
			'msg': f'A user with the usernamename {username} already exists'
		}, 409

	return user_schema.dump(user)


@api.route('/login', methods=['POST'])
def login():
	if not request.is_json:
		return {'msg': 'Missing JSON in request'}, 400

	username = request.json.get('username', None)
	password = request.json.get('password', None)
	if not username:
		return {'msg': 'Missing username'}, 400
	if not password:
		return {'msg': 'Missing password'}, 400

	try:
		user = User.query.filter_by(username=username).first()
	except OperationalError as e:
		return {'err': 'Internal error', 'msg': str(e)}, 500

	if user is None or not user.verify_password(password):
		return {'msg': 'Wrong username or password'}, 401

	ret = {
		'access_token': create_access_token(identity=username),
		'refresh_token': create_refresh_token(identity=username)
	}

	return ret, 200


@api.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
	current_username = get_jwt_identity()

	return {
		'access_token': create_access_token(identity=current_username)
	}, 200
