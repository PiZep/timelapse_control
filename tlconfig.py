#!/bin/usr/env python3
# coding: utf-8

"""Main class of the application"""
import json
import os
import config

# camera = Camera()
PARAM = {}


def _isvalid(param, key=None):
    """Check the structure validity of [param]"""
    isvalid = True
    error = ""
    options = {"timeset", "res", "path", "days", "start", "end", "lastpic"}
    if key and key in options:
        keys = {key}
    else:
        keys = options

    for k in keys:
        if k not in param:
            isvalid = False
            error = f"key {k} is not an option"
            break
        else:
            if k == 'res':
                if not ('width' in param[k] and 'height' in param[k]):
                    isvalid = False
                    error = "Wrong resolution setting"
                    break
            elif k == "days":
                if not len(param[k]) == 7 and all(isinstance(d, bool)
                                                  for d in param[k]):
                    isvalid = False
                    error = "Wrong days setting"
                    break
            elif k in ('start', 'end'):
                if not ('hour' in param[k] and 'minute' in param[k]):
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
    try:
        with open('timelapse.json', 'r') as conf:
            if os.stat('timelapse.json').st_size:
                config.PARAM = json.load(conf)
                config.PARAM['path'] = _check_path(config.PATH)
            else:
                config.PARAM = config.DEFAULT

    except (FileNotFoundError, TypeError):
        with open('timelapse.json', 'w') as conf:
            config.PARAM = config.DEFAULT
            set_config(config.PARAM)

    if _isvalid(config.PARAM):
        set_config(config.PARAM)
    else:
        set_config(config.DEFAULT)

    return config.PARAM


def set_config(newparam):
    """Write back new parameters"""
    with open('timelapse.json', 'w') as conf:
        config.TIMESET = newparam['timeset']
        config.CAM_RES = (newparam['res']['height'], newparam['res']['width'])
        config.INTERVAL = newparam['interval']
        config.PATH = _check_path(newparam['path'])
        config.DAYS = newparam['days']
        config.START_HOUR = newparam['start']['hour']
        config.START_MIN = newparam['start']['minute']
        config.END_HOUR = newparam['end']['hour']
        config.END_MIN = newparam['end']['minute']
        config.LAST_PIC = newparam['lastpic']
        json.dump(newparam, conf, indent=4)


# if __name__ == "__main__":
#     set_config(PARAM)

