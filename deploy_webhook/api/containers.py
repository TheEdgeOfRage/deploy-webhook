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
	"""
	Execute one or more commands in the container with the specified id.
	If one command fails, execution halts and a 422 response is returned.

	:reqheader Authorization: valid JWT access token
	:reqheader Content-Type: application/json
	:reqjson list commands: commands to run

	:resjson string msg: status message
	:resjson string err: error message
	:resjson list result: command execution results

	:statuscode 200: found services
	:statuscode 400: missing parameter
	:statuscode 422: command failed
	"""

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
	"""
	Get the standard output logs from the container with the specified id.

	:reqheader Authorization: valid JWT access token

	:resjson string msg: status message
	:resjson string container_name: container name
	:resjson string output: container log

	:statuscode 200: found services
	"""

	container_controller = ContainerController()
	container = container_controller.get_container(container_id)
	tail = int(request.args.get('tail') or 1000)
	output = container_controller.get_logs(container, tail=tail)

	return {
		'msg': 'Successfully grabbed logs',
		'container_name': container.name,
		'output': output
	}, 200
