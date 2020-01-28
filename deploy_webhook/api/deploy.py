#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

import hmac

from flask import current_app, request
from servicectl import ServiceController
from servicectl.exceptions import StackRevertFailed
from sqlalchemy.exc import OperationalError

from . import api
from ..models import Service
from .tasks import async_api


def verify_signature():
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


@api.route('/deploy', methods=['POST'])
@async_api
def deploy():
	"""
	Asynchronously update designated services with a new version of image.
	A background task thread with a `task_id` gets started that does the updating.

	:reqheader Content-Type: application/json
	:reqjson list services: the services to update

	:resjson string msg: status message
	:resjson string task_id: the unique id of the background task

	:statuscode 202: Started deploy
	"""

	service_controller = ServiceController()
	services_to_update = request.json
	try:
		tracked_services = Service.query.all()
	except OperationalError as e:
		return {'err': 'Internal error', 'msg': str(e)}, 500

	try:
		success, failed_service = service_controller.update_stack(tracked_services, services_to_update)
	except StackRevertFailed as e:
		return {'err': 'Stack revert failed', 'msg': str(e)}, 500

	if success:
		return {'msg': 'Successfully updated all services'}, 200
	else:
		return {
			'err': 'Stack update failed',
			'msg': f'Service {failed_service} failed to update. Stack reverted'
		}, 500
