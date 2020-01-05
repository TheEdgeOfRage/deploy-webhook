#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from app.controllers.service_controller import ServiceController
from app.controllers.container_controller import ContainerController
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

		service_controller = ServiceController()
		service = service_controller.add_service(name, repository, tag)
		if service is None:
			return {'err': 'Service exists', 'msg': f'A service with the name {name} already exists'}, 409

		return {'msg': 'Successfully added service', 'service': self.service_schema.dump(service)}, 200

	@jwt_required
	def get(self):
		service_controller = ServiceController()
		services = service_controller.get_services()
		services = [self.service_schema.dump(service) for service in services]
		service_controller.set_services_status(services)
		container_controller = ContainerController(service_controller)
		container_controller.get_active_containers(services)

		return services, 200


class ServiceResource(Resource):
	@jwt_required
	def delete(self, service_name):
		service_controller = ServiceController()
		if service_controller.delete_service(service_name):
			return {'msg': f'Successfully deleted service named {service_name}'}, 200
		else:
			return {'err': 'Services deletion failed', 'msg': f'The service named {service_name} has not been found'}, 404
