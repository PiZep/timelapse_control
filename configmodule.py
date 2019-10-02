#!/bin/usr/env python3
# coding: utf-8

"""File for a class wrapper arround json"""
import json
import logging
from importlib import import_module, util
from os import stat, path
from inspect import ismodule
from dotdict import DotDict


class ConfigJSON:
    """Simple config manager using json

    The constructor can take one ``config`` parameter.
    ``config`` can refer to a module or a module name.
    If this is the case, it should contain a least a ``_DEFAULT``
    config dict.

    :param config: A dict, a module, a module name, a "stringed" dict or
    a json file name (without the leadding dot or '.json' extension)
    :type config: dict, string

    :Example:

    >>>from configmodule import ConfigJSON
    >>>d = {'param1': 1, 'param2': 2}
    >>>s = str(d)
    >>>c1 = ConfigJSON(d)
    >>>c2 = ConfigJSON('config') # works with config.py or .config.json
    >>>import config
    >>>c3 = ConfigJSON(config)
    >>>c4 = ConfigJSON(s)
    """
    # conf = {}
    # _confjson = ''
    # _module = None
    # _default = {}

    class IterConf(dict):
        """Structure stocking information about iterables in config"""

        def __init__(self, data):
            super().__init__(self)
            self['type'] = type(data)
            self['len'] = len(data)
            self['subtypes'] = type(data)(type(x) for x in data)

    def __init__(self, config=None):
        self.logger = logging.getLogger('server_app.configmodule.ConfigJSON')
        if config:
            # self._module is set only with a DEFAULT attribute
            self._module = self._getmodule(config)
        else:
            config = "config"

        if self._module:
            self._default = self._module.DEFAULT
            self._confjson = self._module.__name__ + '.json'
            self.conf = DotDict(self._getconfig())
        elif isinstance(config, str):
            if path.isfile(config + '.json'):
                self._confjson = config + ".json"
            elif isinstance(eval(config), dict):
                self._default = self.conf = config
        elif isinstance(config, dict):
            self._default = self.conf = eval(str(config))
        else:
            self._default = self.conf = {}

        self._struct = {}
        self._struct = self._getstructure(self._default)
        self.keys = self._default.keys()
        self.save()
        self.logger.debug('__init__')

    def __del__(self):
        self.save()
        self.logger.debug("__del__")

    def _getmodule(self, module):
        """Check config module validity"""
        self.logger.debug('_getmodule')
        if ismodule(module):
            conf_module = module
            # self.logger.debug(f"module importé: {conf_module}")
        elif util.find_spec(module):
            conf_module = import_module(module)
            # self.logger.debug("module importé avec importlib")

        if not hasattr(conf_module, 'DEFAULT'):
            # self.logger.debug("module désimporté: {conf_module} "
            #       f"{hasattr(conf_module, 'DEFAULT')}")
            conf_module = None

        return conf_module

    def _getstructure(self, *args, **kwargs):
        """Return the structure of the config dictionary"""
        self.logger.debug('_getstructure')
        struct = self._struct if self._struct else {}
        for arg in args:
            self.logger.debug(f'in _getstructure: {arg}')
            for (k, v) in arg.items():
                # self.logger.debug(f'{k}: {v}')
                if isinstance(v, dict):
                    struct[k] = self._getstructure(v)
                elif not isinstance(v, str) and hasattr(v, '__iter__'):
                    struct[k] = self.IterConf(v)
                else:
                    struct[k] = type(v)
                # struct = {k: (self._getstructure(v) if isinstance(v, dict)
                #               else self.IterConf(v) if not isinstance(v, str)
                #               and hasattr(v, '__iter__') else type(v))
                #           for (k, v) in arg.items()}
        if kwargs:
            for (k, v) in kwargs.items():
                if isinstance(v, dict):
                    struct[k] = self._getstructure(v)
                elif not isinstance(v, str) and hasattr(v, '__iter__'):
                    struct[k] = self.IterConf(v)
                else:
                    struct[k] = type(v)
        return struct

    def _getconfig(self):
        """Get the actual configuration"""
        self.logger.debug('_getconfig')
        # struct = self._struct if self._struct else {}
        try:
            with open(self._confjson) as conf:
                if stat(self._confjson).st_size:
                    self.conf = json.load(conf)
                else:
                    self.conf = self._default

        except (FileNotFoundError, TypeError):
            with open(self._confjson, 'w') as conf:
                self.conf = self._default

        # self.logger.debug(self.conf)
        for k in self.conf.keys():
            try:
                self.logger.debug(f'in configmodule, try: {k}')
                self._module._isvalid(self.conf, k)
                self.conf[k] = self.conf[k]
            except TypeError:
                self.logger.debug(f'in configmodule, error: {k}')
                self.conf[k] = self._default[k]

        return self.conf

    def save(self):
        """Write back new parameters"""
        # self.logger.debug('save')
        with open(self._confjson, 'w') as conf:
            json.dump(self.conf, conf, indent=4)

