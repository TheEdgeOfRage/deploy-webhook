#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

from marshmallow import Schema, fields


class ContainerSchema(Schema):
    id = fields.Str()
    short_id = fields.Str()
    name = fields.Str()
    status = fields.Str()

