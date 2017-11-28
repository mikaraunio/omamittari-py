#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os

ENVPREFIX = "OMAMITTARI_"
DEFAULT_CONFIG_PATH = "omamittari.ini"


class ConfigError(RuntimeError):
    pass


class Config(object):
    def __init__(self, config_path=None):
        if not config_path:
            config_path = DEFAULT_CONFIG_PATH
        self.config_path = config_path
        self.ini_file = ConfigParser.ConfigParser()
        self.ini_file.read(self.config_path)

    def get(self, name):
        envval = os.getenv(ENVPREFIX + name.upper())
        if envval:
            return envval
        try:
            return self.ini_file.get('authentication', name)
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            raise ConfigError("No value for %s supplied or found in "
                              "environment or config file" % name)
