#!/bin/usr/env python3
# coding: utf-8

"""Main class of the application"""
import os
# import threading
# from camera_opencv import Camera
import json

# camera = Camera()
default = {"timeset": False,
           "res": {"width": 320, "height": 240},
           "interval": 60,
           "path": os.getcwd(),
           "days": [False] * 7,
           "start": {"hour": 0, "min": 0},
           "end": {"hour": 0, "min": 0}
           }
param = {}

try:
    with open('timelapse.json', 'r') as conf:
        param = json.load(conf)

        TIMESET = param['timeset']
        CAM_RES = (param['res']['width'], param['res']['height'])
        INTERVAL = param['interval']
        PATH = param['path']
        DAYS = param['days']
        START_HOUR = param['start']['hour']
        START_MIN = param['start']['minute']
        END_HOUR = param['end']['hour']
        END_MIN = param['end']['minute']
except FileNotFoundError:
    with open('timelapse.json', 'w') as conf:
        param = default
        json.dump(default, conf)


def get_config():
    """Get the actual configuration"""
    return param


def set_config():
    """Write back new parameters"""
    with open('timelapse.json', 'w') as conf:
        json.dump(param, conf)


if __name__ == "__main__":
    set_config()

