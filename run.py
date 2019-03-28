#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

from app import create_blueprint as app_blueprint
from common import create_app

app = create_app()
app.register_blueprint(app_blueprint(), url_prefix='/deploy')

