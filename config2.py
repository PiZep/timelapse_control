#!/bin/usr/env python3

import os

_DEFAULT = {"timeset": False,
            "res": {"width": 320, "height": 240},
            "interval": 60,
            "path": "",
            "days": [False] * 7,
            "start": {"hour": 0, "minute": 0},
            "end": {"hour": 0, "minute": 0},
            "lastpic": ""
            }

TIMESET = _DEFAULT['timeset']
CAM_RES = (_DEFAULT['res']['width'], _DEFAULT['res']['height'])
INTERVAL = _DEFAULT['interval']
PATH = _DEFAULT['path']
DAYS = _DEFAULT['days']
START_HOUR = _DEFAULT['start']['hour']
START_MIN = _DEFAULT['start']['minute']
END_HOUR = _DEFAULT['end']['hour']
END_MIN = _DEFAULT['end']['minute']
LAST_PIC = _DEFAULT['lastpic']

OPTIONS = set(_DEFAULT.keys())


def _check_path(path):
    """Check if the path exists, else return working dir"""
    if not (os.path.isdir(path) and os.access(path, os.W_OK)):
        path = os.getcwd()

    return path


def _isvalid(param, key=None):
    """Check the structure validity of [param]"""
    isvalid = True
    error = ""
    if key and key in OPTIONS:
        keys = {key}
    else:
        keys = OPTIONS

    for k in keys:
        if k not in param:
            isvalid = False
            error = f'The "{k}" key is not optional'
            break
        else:
            if k == 'res':
                if not ('width' in param[k] and
                        'height' in param[k]):
                    isvalid = False
                    error = "Wrong resolution setting"
                    break
            elif k == "days":
                if (not len(param[k]) == 7 and
                        all(isinstance(d, bool) for d in param[k])):
                    isvalid = False
                    error = "Wrong days setting"
                    break
            elif k in ('start', 'end'):
                if not ('hour' in param[k] and
                        'minute' in param[k]):
                    isvalid = False
                    error = "Wrong hour setting"
                    break
    if not isvalid:
        raise TypeError(error)
    return isvalid
