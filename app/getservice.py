#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 pavle <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.

import docker
import pprint


def print_attrs(service):
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(service.attrs)


if __name__ == '__main__':
	client = docker.from_env()
	services = client.services.list()
	for service in services:
		print_attrs(service)
