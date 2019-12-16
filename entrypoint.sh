#! /bin/sh
#
# entrypoint.sh
# Copyright (C) 2019 Pavle Portic <pavle.portic@tilda.center>
#
# Distributed under terms of the BSD-3-Clause license.
#

flask db upgrade
gunicorn -w 1 --bind 0.0.0.0:80 ${FLASK_APP}

