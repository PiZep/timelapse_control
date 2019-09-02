#!/bin/usr/env python3
# coding: utf-8

"""Main class of the application"""
# import os
# import threading
# from camera_opencv import Camera
import json

# camera = Camera()

TIMESET = False
CAM_RES = (0, 0)
INTERVAL = 0
DAYS = [False] * 7
START_HOUR = 0
START_MIN = 0
END_HOUR = 0
END_MIN = 0
PATH = ''


def get_config():
    """Get the actual configuration"""
    with open('timelapse.json', 'r') as conf:
        param = json.load(conf)

    TIMESET = param['timeset']
    CAM_RES = (param['res']['width'], param['res']['height'])
    INTERVAL = param['interval']
    if TIMESET:
        DAYS = param['days']
        START_HOUR = param['start']['hour']
        START_MIN = param['start']['minute']
        END_HOUR = param['end']['hour']
        END_MIN = param['end']['minute']
        PATH = param['path']

    return param


def set_config(new_param=None):
    """Write back new parameters"""
    param = {}
    if new_param:
        with open('timelapse.json', 'w') as conf:
            param = json.load(conf)
            param = {key: (item if new_param[key] else param[key])
                     for (key, item) in new_param.items()}
            json.seek(0)
            json.dump(param, conf)


if __name__ = "__main__":
    set_config()

