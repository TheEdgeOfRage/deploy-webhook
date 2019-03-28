#! /bin/sh
#
# entrypoint.sh
# Copyright (C) 2019 Vivify Ideas
#
# Distributed under terms of the BSD-3-Clause license.
#

gunicorn -w 1 --bind 0.0.0.0:80 run:app

