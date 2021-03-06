#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.


from sqlalchemy.exc import IntegrityError
from getpass import getpass

from ... import db
from ...models import User


def create_user(username, password, prompt):
	if prompt:
		password = getpass(prompt="password: ")

	user = User(username=username, password=password)
	db.session.add(user)
	try:
		db.session.commit()
		print('Successfully created user', username)
	except IntegrityError:
		db.session.rollback()
		print('User already exists')
