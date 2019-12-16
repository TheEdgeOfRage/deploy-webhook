#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from flask_restful import Api
from .containers import ContainerExecResource, ContainerLogsResource
from .deploy import DeployResource
from .services import ServicesResource, ServiceResource
from .user import SignupResource, LoginResource, RefreshResource
from .tasks import TaskResource

api = Api()

api.add_resource(LoginResource, '/login')
api.add_resource(RefreshResource, '/refresh')
api.add_resource(SignupResource, '/signup')
api.add_resource(DeployResource, '/deploy')
api.add_resource(ServicesResource, '/services')
api.add_resource(ServiceResource, '/services/<service_name>')
api.add_resource(ContainerExecResource, '/containers/<container_id>/exec')
api.add_resource(ContainerLogsResource, '/containers/<container_id>/logs')
api.add_resource(TaskResource, '/tasks/<task_id>')

