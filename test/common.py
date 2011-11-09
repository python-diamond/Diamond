#!/usr/bin/python
################################################################################

import os
import sys
import unittest

from mock import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from diamond import *

def get_collector_config():
    config = configobj.ConfigObj()
    config['server'] = {}
    config['server']['collectors_config_path'] = ''
    config['collectors'] = {}
    config['collectors']['default'] = {}
    return config

def get_fixture_path(fixture_name):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures', fixture_name))
