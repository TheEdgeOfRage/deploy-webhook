#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
	db.init_app(app)
	Migrate(app, db)
