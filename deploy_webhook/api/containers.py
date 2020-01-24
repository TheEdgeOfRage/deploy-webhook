#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

from flask import request
from flask_jwt_extended import jwt_required
from servicectl import ContainerController

from . import api


@api.route('/containers/<container_id>/exec', methods=['POST'])
@jwt_required
def exec_command(container_id):
	commands = request.json.get('commands', None)
	if commands is None:
		return {'err': 'Missing parameter'}, 400

	container_controller = ContainerController()
	container = container_controller.get_container(container_id)
	response = []
	for command in commands:
		code, output = container_controller.exec_command(container, command)
		response.append({'command': command, 'code': code, 'output': output})
		if code != 0:
			return {'msg': 'Command failed', 'result': response}, 422

	return {'msg': 'Successfully ran commands', 'result': response}, 200


@api.route('/containers/<container_id>/logs', methods=['GET'])
@jwt_required
def get_container_logs(container_id):
	container_controller = ContainerController()
	container = container_controller.get_container(container_id)
	tail = int(request.args.get('tail') or 1000)
	output = container_controller.get_logs(container, tail=tail)

	return {
		'msg': 'Successfully grabbed logs',
		'container_name': container.name,
		'output': output
	}, 200
