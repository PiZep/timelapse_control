#!/bin/bash
source env/bin/activate
CAMERA=$1 gunicorn --worker-class gevent --workers 1 --bind 0.0.0.0:5000 server_app:app
