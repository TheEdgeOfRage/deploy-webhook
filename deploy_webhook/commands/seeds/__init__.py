#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.


import click
from flask.cli import with_appcontext

from .user_seeder import create_user
from .service_seeder import create_service


@click.group()
def seed():
	"""Perform database migrations."""
	pass


@click.option('-u', '--username', default='admin', help=('Username of the account'))
@click.option('-p', '--password', default='admin', help=('Password of the account'))
@click.option('--prompt', default=False, is_flag=True, help=('Prompt for password instead of passing it as an option'))
@seed.command()
@with_appcontext
def user(username, password, prompt):
	create_user(username, password, prompt)


@click.option('-n', '--name', help=('Name of the service'))
@click.option('-r', '--repository', help=('Repository in docker registry'))
@click.option('-t', '--tag', help=('Image tag'))
@seed.command()
@with_appcontext
def service(name, repository, tag):
	create_service(name, repository, tag)
