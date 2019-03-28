#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

from flask_restful import Api
from .webhook import WebhookResource

api = Api()
api.add_resource(WebhookResource, '/')

