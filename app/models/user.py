#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from app.db import db
from passlib.hash import argon2


class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.Unicode(256), unique=True, index=True, nullable=False)
	password = db.Column(db.String(128), nullable=False)

	def __init__(self, username, password):
		self.username = username
		self.password = argon2.hash(password)

	def verify_password(self, password):
		return argon2.verify(password, self.password)

	def __repr__(self):
		return f'<User {self.username}>'
