#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Miguel Grinberg <miguelgrinberg50@gmail.com>
#
# Distributed under terms of the MIT license.

import threading
import time
import uuid
from datetime import datetime
from flask import current_app, request
from flask_restful import Resource
from functools import wraps

tasks = {}


def before_first_request():
	def clean_old_tasks():
		global tasks
		while True:
			# Only keep tasks that are running or that finished less than 5 minutes ago.
			five_min_ago = datetime.timestamp(datetime.utcnow()) - 5 * 60
			tasks = {
				task_id: task
				for task_id, task in tasks.items()
				if 'timestamp' not in task or task['timestamp'] > five_min_ago
			}
			time.sleep(60)

	thread = threading.Thread(target=clean_old_tasks)
	thread.start()


def async_api(f):
	@wraps(f)
	def wrapped(*args, **kwargs):
		def task(flask_app, environ):
			# Create a request context similar to that of the original request
			with flask_app.request_context(environ):
				try:
					tasks[task_id]['response'] = f(*args, **kwargs)
				except Exception as e:
					tasks[task_id]['response'] = {
						'err': 'Task failed',
						'msg': str(e)
					}, 500
					if current_app.debug:
						raise e
				finally:
					tasks[task_id]['timestamp'] = datetime.timestamp(datetime.utcnow())

		task_id = uuid.uuid4().hex
		tasks[task_id] = {
			'task': threading.Thread(
				target=task,
				args=(current_app._get_current_object(), request.environ)
			)
		}
		tasks[task_id]['task'].start()

		# Return a 202 response, with a link that the client can use to obtain task status
		return {'msg': 'Task started', 'task_id': task_id}, 202

	return wrapped


class TaskResource(Resource):
	def get(self, task_id):
		"""
		Return status about an asynchronous task. If this request returns a 202
		status code, it means that task hasn't finished yet. Else, the response
		from the task is returned.
		"""
		task = tasks.get(task_id)
		if task is None:
			return {'err': 'Task not found'}, 404
		if 'response' not in task:
			return {'msg': 'Task is still running'}, 202

		return task['response']
