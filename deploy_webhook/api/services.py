#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from flask import jsonify, request
from flask_jwt_extended import jwt_required
from servicectl import ServiceController, ContainerController
from servicectl.exceptions import InternalDockerError
from sqlalchemy.exc import IntegrityError, OperationalError

from . import api
from .. import db
from ..models import Service
from ..schemas import service_schema


@api.route('/services', methods=['GET'])
@jwt_required
def get_services():
	service_controller = ServiceController()
	try:
		services = Service.query.all()
	except OperationalError as e:
		return {'err': 'Internal error', 'msg': str(e)}, 500

	services = [service_schema.dump(service) for service in services]
	service_controller.set_services_status(services)
	container_controller = ContainerController(service_controller)
	try:
		services = container_controller.get_active_containers(services)
	except InternalDockerError as e:
		return {
			'err': 'InternalDockerError',
			'msg': str(e),
		}, 500

	return jsonify(services)


@api.route('/services', methods=['POST'])
@jwt_required
def add_service():
	name = request.json.get('name', None)
	repository = request.json.get('repository', None)
	tag = request.json.get('tag', None)
	if None in [name, repository, tag]:
		return {'err': 'Missing parameter'}, 400

	service = Service(name=name, repository=repository, tag=tag)
	try:
		db.session.add(service)
		db.session.commit()
	except IntegrityError:
		db.session.rollback()
		return {
			'err': 'Service exists',
			'msg': f'A service with the name {name} already exists',
		}, 409

	return {
		'msg': 'Successfully added service',
		'service': service_schema.dump(service)
	}, 200


@api.route('/services/<service_name>', methods=['DELETE'])
@jwt_required
def delete(self, service_name):
	try:
		service = Service.query.filter_by(name=service_name).first()
	except OperationalError as e:
		return {'err': 'Internal error', 'msg': str(e)}, 500

	if service is None:
		return {'msg': f'Successfully deleted service named {service_name}'}, 200

	db.session.delete(service)
	db.session.commit()

	return {
		'err': 'Services deletion failed',
		'msg': f'The service {service_name} has not been found'
	}, 404
