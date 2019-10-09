#!/bin/bash
source env/bin/activate
export CAMERA=$1 
# celery worker -A server_app.celery worker -c 4 --loglevel=info inspect active
gunicorn --worker-class gevent --workers 1 --bind 0.0.0.0:5000 server_app:app
