#!/usr/bin/env python3
# coding: utf-8

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/pi/projets/flask-video-streaming")

from app import app as application

