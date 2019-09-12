#!/bin/usr/env python3

DEFAULT = {"timeset": False,
           "res": {"width": 320, "height": 240},
           "interval": 60,
           "path": None,
           "days": [False] * 7,
           "start": {"hour": 0, "minute": 0},
           "end": {"hour": 0, "minute": 0},
           "lastpic": None
           }

TIMESET = DEFAULT['timeset']
CAM_RES = DEFAULT['cam_res']
INTERVAL = DEFAULT['interval']
PATH = DEFAULT['path']
DAYS = DEFAULT['days']
START_HOUR = DEFAULT['start']['hour']
START_MIN = DEFAULT['start']['min']
END_HOUR = DEFAULT['end']['hour']
END_MIN = DEFAULT['end']['min']
LAST_PIC = DEFAULT['lastpic']
