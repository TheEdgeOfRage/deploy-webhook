#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 pavle <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.


from app.schemas.container import ContainerSchema
from .docker_controller import DockerController


class ContainerController(DockerController):
	container_schema = ContainerSchema()

	def __init__(self, controller=None):
		if controller is None:
			super(ContainerController, self).__init__()
		else:
			self.client = controller.client

	def get_active_containers(self, services):
		containers = self.client.containers.list(all=True)
		for service in services:
			service['containers'] = [self.container_schema.dump(container) for container in containers if container.name.startswith(service['name'])]

	def get_container(self, container_id):
		return self.client.containers.get(container_id)

	def exec_command(self, container, command):
		code, output = container.exec_run(command)
		output = output.decode('UTF-8')

		return code, output
