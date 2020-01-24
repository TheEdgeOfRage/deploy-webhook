#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from sqlalchemy.exc import IntegrityError

from ... import db
from ...models import Service


def create_service(name, repository, tag):
	service = Service(name=name, repository=repository, tag=tag)
	db.session.add(service)
	try:
		db.session.commit()
		print('Successfully created service', name)
	except IntegrityError:
		db.session.rollback()
		print('Service already exists')
