#!/usr/bin/python
################################################################################

import os
import sys
import unittest

from StringIO import StringIO
from contextlib import nested

from mock import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'collectors')))

from diamond import *

def get_collector_config(key, value):
    config = configobj.ConfigObj()
    config['server'] = {}
    config['server']['collectors_config_path'] = ''
    config['collectors'] = {}
    config['collectors']['default'] = {}
    config['collectors'][key] = value
    return config

def get_fixture(fixture_name):
    with open(get_fixture_path(fixture_name), 'r') as file:
        return StringIO(file.read())

def get_fixture_path(fixture_name):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures', fixture_name))

class CollectorTestCase(unittest.TestCase):
    def assertPublished(self, mock, key, value):
        calls = filter(lambda x: x[0][0] == key, mock.call_args_list)

        actual_value = len(calls)
        expected_value = 1
        message = '%s: actual number of calls %d, expected %d' % (key, actual_value, expected_value)

        self.assertEqual(actual_value, expected_value, message)

        actual_value = calls[0][0][1]
        expected_value = value
        precision = None

        if isinstance(value, tuple):
            expected_value, precision = expected_value

        message = '%s: actual %r, expected %r' % (key, actual_value, expected_value)

        if precision:
            self.assertAlmostEqual(actual_value, expected_value, places = precision, msg = message)
        else:
            self.assertEqual(actual_value, expected_value, message)

    def assertPublishedMany(self, mock, dict):
        for key, value in dict.iteritems():
            self.assertPublished(mock, key, value)

        mock.reset_mock()
