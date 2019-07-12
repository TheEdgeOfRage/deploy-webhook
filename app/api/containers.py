#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

from flask import request
from flask_restful import Resource

from app.controllers.container_controller import ContainerController


class ContainerExecResource(Resource):
	def post(self, container_id):
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


class ContainerLogsResource(Resource):
	def get(self, container_id):
		container_controller = ContainerController()
		container = container_controller.get_container(container_id)
		output = container_controller.get_logs(container)

		return {'msg': 'Successfully grabbed logs', 'container_name': container.name, 'output': output}, 200

