#!/bin/usr/env python3
# coding: utf-8

"""File for a class wrapper arround json"""
import json
from importlib import import_module, util
from os import stat, path
from inspect import ismodule
from dotdict import DotDict


class ConfigJSON(DotDict):
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

        # def __repr__(self):
        #     return (f"{{'type': {self.type},"
        #             f"'len': {self.len},"
        #             f"'subtypes': {self.subtypes}}}")

    def __init__(self, config=None):
        if config:
            self._module = self._getmodule(config)
        else:
            config = "config"

        self._confjson = config + ".json"

        if self._module:
            # self._module is set only with a _DEFAULT attribute
            self._default = self._module._DEFAULT
        else:
            if isinstance(config, dict) or isinstance(eval(config), dict):
                self._default = eval(str(config))
            elif path.isfile(config + '.json'):
                self.conf = self._getconfig()

        self.conf = DotDict(self._getconfig())
        # self.save()
        print(self.conf, self._default)
        self._struct = self._getstructure(self._default)
        self.keys = self._default.keys()

    def __del__(self):
        self.save()
        print("Configuration saved")

    def _getmodule(self, module):
        """Check config module validity"""
        conf_module = None
        if ismodule(module):
            import config as conf_module
        elif util.find_spec(module):
            conf_module = import_module(module)

        if not hasattr(conf_module, '_DEFAULT'):
            conf_module = None

        return conf_module

    def _getstructure(self, *args, **kwargs):
        """Return the structure of the config dictionary"""
        struct = self._struct
        for arg in args:
            print(arg)
            for (k, v) in arg.items():
                print(f'{k}: {v}')
                if isinstance(v, dict):
                    struct[k] = self._getstructure(v)
                elif not isinstance(v, str) and hasattr(v, '__iter__'):
                    struct[k] = self.IterConf(v)
                else:
                    struct[k] = type(v)
            # struct = {k: (self._getstructure(v) if isinstance(v, dict)
            #               else self.IterConf(v) if not isinstance(v, str)
            #               and hasattr(v, '__iter__') else type(v))
            #           for (k, v) in args.items()}
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
        try:
            with open(self._confjson) as conf:
                if stat(self._confjson).st_size:
                    self.conf = json.load(conf)
                else:
                    self.conf = self._default

        except (FileNotFoundError, TypeError):
            with open(self._confjson, 'w') as conf:
                self.conf = self._default

        print(self.conf)
        for k in self.conf.keys():
            print(f'in configmodule: {k}')
            self.conf[k] = (self.conf[k] if
                            self._module._isvalid(self.conf, k) else
                            self._default[k])

        return self.conf

    # def save(self):
    #     """Write back new parameters"""
    #     with open(self._confjson, 'w') as conf:
    #         json.dump(self.conf, conf, indent=4)

    # def __getattr__(self, attr):
    #     return self.conf.get(attr)

    # def __setattr__(self, key, value):
    #     self.conf.__setitem__(key, value)
    #     self._getstructure(key=value)

    # def __setitem__(self, key, value):
    #     self.conf.__setitem__(key, value)
    #     self._struct(key=value)

    # def __delattr__(self, item):
    #     self.conf.__delitem__(item)
    #     del self._struct[item]

    # def __delitem__(self, key):
    #     super(DotDict, self).__delitem__(key)
    #     del self.__dict__[key]

