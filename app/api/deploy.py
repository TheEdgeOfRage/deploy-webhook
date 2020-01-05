#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

import hmac
from flask import current_app, request
from flask_restful import Resource

from app.controllers.service_controller import ServiceController
from .tasks import async_api


class DeployResource(Resource):
	def verify_signature(self):
		secret = current_app.config.get('SIGNATURE_SECRET', None)
		if secret is None:
			raise Exception('Secret not defined in config')

		signature = request.headers.get('X-Signature')
		if signature is None:
			return {'msg': 'Invalid signature'}, 403

		sha_name, signature = signature.split('=')
		if sha_name != 'sha1':
			return {'msg': 'Only sha1 is supported as the signature algorithm'}, 501

		mac = hmac.new(secret.encode(), msg=request.data, digestmod='sha1')
		if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
			return {'msg': 'Invalid signature'}, 403

	@async_api
	def post(self):
		service_controller = ServiceController()
		services_to_update = request.json
		return service_controller.update_stack(services_to_update)
