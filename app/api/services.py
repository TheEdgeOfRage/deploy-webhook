#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.db import db
from app.controllers.service_controller import ServiceController
from app.controllers.container_controller import ContainerController
from app.models.service import Service
from app.schemas.service import ServiceSchema


class ServicesResource(Resource):
	service_schema = ServiceSchema()

	@jwt_required
	def post(self):
		name = request.json.get('name', None)
		repository = request.json.get('repository', None)
		tag = request.json.get('tag', None)
		if None in [name, repository, tag]:
			return {'err': 'Missing parameter'}, 400

		service = Service(name=name, repository=repository, tag=tag)
		db.session.add(service)
		db.session.commit()

		return {'msg': 'Successfully added service'}, 200

	@jwt_required
	def get(self):
		service_controller = ServiceController()
		services = service_controller.get_services()
		services = [self.service_schema.dump(service) for service in services]
		service_controller.set_services_status(services)
		container_controller = ContainerController(service_controller)
		container_controller.get_active_containers(services)

		return services, 200


