#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

from flask_restful import Api
from .containers import ContainerExecResource
from .deploy import DeployResource
from .services import ServicesResource
from .user import SignupResource, LoginResource, RefreshResource

api = Api()

api.add_resource(LoginResource, '/login')
api.add_resource(RefreshResource, '/refresh')
api.add_resource(SignupResource, '/signup')
api.add_resource(DeployResource, '/deploy')
api.add_resource(ServicesResource, '/services')
api.add_resource(ContainerExecResource, '/containers/<container_id>/exec')

