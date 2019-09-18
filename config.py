#!/bin/usr/env python3

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

