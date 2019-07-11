#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
	create_access_token,
	create_refresh_token,
	jwt_refresh_token_required,
	get_jwt_identity,
)

from app.db import db
from app.models.user import User
from app.schemas.user import UserSchema


class SignupResource(Resource):
	schema = UserSchema()

	def post(self):
		username = request.json['username']
		password = request.json['password']
		user = User(username=username, password=password)
		db.session.add(user)
		db.session.commit()

		return self.schema.dump(user)


class LoginResource(Resource):
	def post(self):
		if not request.is_json:
			return {'msg': 'Missing JSON in request'}, 400

		username = request.json.get('username', None)
		password = request.json.get('password', None)
		if not username:
			return {'msg': 'Missing username'}, 400
		if not password:
			return {'msg': 'Missing password'}, 400

		user = User.query.filter_by(username=username).first()
		if user is None or not user.verify_password(password):
			return {'msg': 'Wrong username or password'}, 401

		ret = {
			'access_token': create_access_token(identity=username),
			'refresh_token': create_refresh_token(identity=username)
		}

		return ret, 200


class RefreshResource(Resource):
	@jwt_refresh_token_required
	def post(self):
		current_username = get_jwt_identity()
		ret = {
			'access_token': create_access_token(identity=current_username)
		}

		return ret, 200

