#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.

from docker_client import DockerClient


def main():
	client = DockerClient('test')
	return client.update_stack()


if __name__ == '__main__':
	print(main())

