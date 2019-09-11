#!/bin/usr/env python3
# coding: utf-8

"""Main class of the application"""
import os
import json

# camera = Camera()
DEFAULT = {"timeset": False,
           "res": {"width": 320, "height": 240},
           "interval": 60,
           "path": os.getcwd(),
           "days": [False] * 7,
           "start": {"hour": 0, "minute": 0},
           "end": {"hour": 0, "minute": 0},
           "lastpic": None
           }

PARAM = {}

TIMESET = DEFAULT['timeset']
CAM_RES = (DEFAULT['res']['width'], DEFAULT['res']['height'])
INTERVAL = DEFAULT['interval']
PATH = DEFAULT['path']
DAYS = DEFAULT['days']
START_HOUR = DEFAULT['start']['hour']
START_MIN = DEFAULT['start']['minute']
END_HOUR = DEFAULT['end']['hour']
END_MIN = DEFAULT['end']['minute']
LAST_PIC = DEFAULT['lastpic']


def check_path(path, addeddir=''):
    """Check if the path exists, else return working dir"""
    if not (os.path.isdir(path) and os.access(path, os.F_OK)):
        path = os.getcwd()

    if len(addeddir.split(os.path.sep)) >= 1:
        split_dir = addeddir.split(os.path.sep).insert(0, path)
        path = os.path.sep.join(split_dir)
        os.makedirs(path)

    return path


def get_config():
    """Get the actual configuration"""
    global PARAM
    try:
        with open('timelapse.json', 'r') as conf:
            PARAM = json.load(conf)
            PARAM['PATH'] = check_path(PATH)
            set_config(PARAM)
    except FileNotFoundError:
        with open('timelapse.json', 'w') as conf:
            PARAM = DEFAULT


def set_config(new_param):
    """Write back new parameters"""
    global TIMESET
    global CAM_RES
    global INTERVAL
    global PATH
    global DAYS
    global START_HOUR
    global START_MIN
    global END_HOUR
    global END_MIN
    global LAST_PIC
    with open('timelapse.json', 'w') as conf:
        TIMESET = new_param['timeset']
        CAM_RES = (new_param['res']['width'], new_param['res']['height'])
        INTERVAL = new_param['interval']
        PATH = check_path(new_param['path'])
        DAYS = new_param['days']
        START_HOUR = new_param['start']['hour']
        START_MIN = new_param['start']['minute']
        END_HOUR = new_param['end']['ur']
        END_MIN = new_param['end']['mute']
        LAST_PIC = new_param['lastpic']
        json.dump(new_param, conf)


if __name__ == "__main__":
    set_config(PARAM)

