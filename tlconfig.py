#!/bin/usr/env python3
# coding: utf-8

"""Main class of the application"""
import json
import os
import config

# camera = Camera()

OPTIONS = set(config._DEFAULT.keys())
PARAM = {}


def _isvalid(key=None):
    """Check the structure validity of [param]"""
    isvalid = True
    error = ""
    if key and key in OPTIONS:
        keys = {key}
    else:
        keys = OPTIONS

    for k in keys:
        if k not in PARAM:
            isvalid = False
            error = f'The "{k}" key is not optional'
            break
        else:
            if k == 'res':
                if not ('width' in PARAM[k] and
                        'height' in PARAM[k]):
                    isvalid = False
                    error = "Wrong resolution setting"
                    break
            elif k == "days":
                if (not len(PARAM[k]) == 7 and
                        all(isinstance(d, bool) for d in PARAM[k])):
                    isvalid = False
                    error = "Wrong days setting"
                    break
            elif k in ('start', 'end'):
                if not ('hour' in PARAM[k] and
                        'minute' in PARAM[k]):
                    isvalid = False
                    error = "Wrong hour setting"
                    break
    if not isvalid:
        raise TypeError(error)
    return isvalid


def _check_path(path):
    """Check if the path exists, else return working dir"""
    if not (os.path.isdir(path) and os.access(path, os.W_OK)):
        path = os.getcwd()

    return path


def get_config():
    """Get the actual configuration"""
    global PARAM
    try:
        with open('timelapse.json', 'r') as conf:
            if os.stat('timelapse.json').st_size:
                PARAM = json.load(conf)
                PARAM['path'] = _check_path(config.PATH)
            else:
                PARAM = config._DEFAULT

    except (FileNotFoundError, TypeError):
        with open('timelapse.json', 'w') as conf:
            PARAM = config._DEFAULT

    for k in OPTIONS:
        PARAM[k] = PARAM[k] if _isvalid(k) else config._DEFAULT[k]

    set_config()
    return PARAM


def set_config():
    """Write back new parameters"""
    with open('timelapse.json', 'w') as conf:
        config.TIMESET = PARAM['timeset']
        config.CAM_RES = (PARAM['res']['height'], PARAM['res']['width'])
        config.INTERVAL = PARAM['interval']
        config.PATH = _check_path(PARAM['path'])
        config.DAYS = PARAM['days']
        config.START_HOUR = PARAM['start']['hour']
        config.START_MIN = PARAM['start']['minute']
        config.END_HOUR = PARAM['end']['hour']
        config.END_MIN = PARAM['end']['minute']
        config.LAST_PIC = PARAM['lastpic']
        json.dump(PARAM, conf, indent=4)


if __name__ == "__main__":
    set_config()

