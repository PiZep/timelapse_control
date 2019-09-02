#!/usr/bin/env python3
# coding: utf-8

import json


def get_config():
    """Get the actual configuration"""
    with open('timelapse.json', 'r') as conf:
        param = json.load(conf)
    return param


def set_config(new_param):
    """Write back new parameters"""
    param = {}
    with open('timelapse.json', 'w') as conf:
        param = json.load(conf)
        param = {key: (item if new_param[key] else param[key])
                 for (key, item) in new_param.items()}
        json.seek(0)
        json.dump(param, conf)

