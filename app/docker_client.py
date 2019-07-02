#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

import docker
import json
import time

from datetime import datetime


class ServiceUpdateError(Exception):
	pass


class DockerClient:
	def __init__(self):
		self.client = docker.from_env()
		self.get_images()

	def get_images(self):
		with open('images.json', 'r') as f:
			self.images = json.load(f)

	def backup_images(self):
		try:
			for service in self.images:
				image_name = self.images[service]
				image = self.client.images.get(f'{image_name["repository"]}:{image_name["tag"]}')
				image.tag(image_name['repository'], tag='previous')
		except docker.errors.ImageNotFound as e:
			print(e)
			return False

		return True

	def pull_images(self):
		for service in self.images:
			image = self.images[service]
			self.client.images.pull(repository=image['repository'], tag=image['tag'])

	def wait_for_service_update(self, service, now):
		while True:
			time.sleep(1)
			service.reload()
			updated_at = service.attrs['UpdatedAt'].split('.')[0]
			updated_at = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S')
			state = service.attrs['UpdateStatus']['State']
			if updated_at > now and state != 'updating':
				return

	def update_service(self, service, image):
		now = datetime.utcnow()
		service.update(image=image, force_update=True)
		self.wait_for_service_update(service, now)
		update_state = service.attrs['UpdateStatus']['State']
		if update_state != 'completed':
			raise ServiceUpdateError(f'Failed to update service {service.name}')

		print('Updated service', service.name)

	def update_stack(self):
		revert = self.backup_images()
		self.pull_images()
		services = self.client.services.list()
		services.sort(key=lambda service: service.name)
		updated_services = []

		for service in services:
			if service.name not in self.images:
				continue

			image = self.images[service.name]
			image = f'{image["repository"]}:{image["tag"]}'
			print('Updating service', service.name, 'with image', image)
			try:
				self.update_service(service, image)
				updated_services.append(service)
			except (docker.errors.APIError, ServiceUpdateError) as e:
				print(e)
				if revert:
					return self.revert_services(updated_services, service.name)
				else:
					return {'err': 'Stack revert failed', 'msg': 'No backup images were created'}, 500

		return {'msg': 'Successfully updated all services'}, 200

	def revert_services(self, updated_services, failed_service):
		for service in updated_services:
			image = f'{self.images[service.name]["repository"]}:previous'
			print('Reverting service', service.name)
			try:
				self.update_service(service, image)
			except (docker.errors.APIError, ServiceUpdateError) as e:
				print(e)
				return {'err': 'Stack revert failed', 'msg': str(e)}, 500

		return {'err': 'Stack update failed', 'msg': f'Service {failed_service} failed to update. Stack reverted'}, 500

