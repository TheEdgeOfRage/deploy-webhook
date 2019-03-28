#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

import docker


class DockerClient:
	def __init__(self, stack):
		self.client = docker.from_env()
		self.stack = stack
		self.get_images()

	def get_images(self):
		self.services = self.client.services.list()
		self.images = {}
		for service in self.services:
			if service.name.startswith(self.stack):
				image = service.attrs['Spec']['TaskTemplate']['ContainerSpec']['Image']
				image = image.split('@')[0]
				repository, tag = image.split(':')
				self.images[service.name] = {
					'repository': repository,
					'tag': tag,
				}

	def backup_images(self):
		for service in self.images:
			new_image = self.images[service]
			old_image = self.client.images.get(f'{new_image["repository"]}:{new_image["tag"]}')
			old_image.tag(new_image['repository'], tag='previous')

	def pull_images(self):
		for service in self.images:
			image = self.images[service]
			self.client.images.pull(repository=image['repository'], tag=image['tag'])

	def update_stack(self):
		self.backup_images()
		self.pull_images()
		updated_services = {}

		for service in self.services:
			if service.name not in self.images:
				continue

			image = self.images[service.name]
			repository = image['repository']
			tag = image['tag']
			image = f'{repository}:{tag}'
			updated_services.append(service)
			try:
				service.update(force_update=True)
				print(f'Updated service {service.name}')
			except docker.errors.APIError:
				return self.revert_services(updated_services, service.name)

		return {'msg': 'Successfully updated all services'}, 200

	def revert_services(self, updated_services, failed_service):
		for service in updated_services:
			image = f'{self.images[service.name]["repository"]}:previous'
			print(service, image)
			try:
				service.update(image, force_update=True)
			except docker.errors.APIError as e:
				return {'err': 'Revert failed', 'msg': str(e)}, 500

		return {'err': f'Update failed', 'msg': 'Service {failed_service} failed to update. Stack reverted'}, 500

