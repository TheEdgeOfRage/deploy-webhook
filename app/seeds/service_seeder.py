#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 pavle <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from sqlalchemy.exc import IntegrityError

from app.models.service import Service
from app.db import db


def create_services():
	service1 = Service(name='test_s1', repository='theedgeofrage/test', tag='latest')
	service2 = Service(name='test_s2', repository='theedgeofrage/test2', tag='latest')
	service3 = Service(name='test_s3', repository='theedgeofrage/test3', tag='latest')
	db.session.add(service1)
	db.session.add(service2)
	db.session.add(service3)
	try:
		db.session.commit()
		print('Successfully created services')
	except IntegrityError:
		db.session.rollback()
		print('Services already exists')

