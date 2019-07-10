#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

from app.db import db


class Service(db.Model):
	__tablename__ = 'services'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(256), unique=True, nullable=False)
	repository = db.Column(db.String(256), nullable=False)
	tag = db.Column(db.String(256), nullable=False)

	def __init__(self, name, repository, tag):
		self.name = name
		self.repository = repository
		self.tag = tag

	def __repr__(self):
		return f'<Service {self.name}>'

