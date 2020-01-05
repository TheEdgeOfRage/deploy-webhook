#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from marshmallow import Schema, fields


class ServiceSchema(Schema):
    name = fields.Str()
    repository = fields.Str()
    tag = fields.Str()
