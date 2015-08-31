#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import unittest
import configobj

from diamond.collector import Collector


class BaseCollectorTest(unittest.TestCase):

    def test_SetCustomHostname(self):
        config = configobj.ConfigObj()
        config['server'] = {}
        config['server']['collectors_config_path'] = ''
        config['collectors'] = {}
        config['collectors']['default'] = {
            'hostname': 'custom.localhost',
        }
        c = Collector(config, [])
        self.assertEquals('custom.localhost', c.get_hostname())

    def test_SetHostnameViaShellCmd(self):
        config = configobj.ConfigObj()
        config['server'] = {}
        config['server']['collectors_config_path'] = ''
        config['collectors'] = {}
        config['collectors']['default'] = {
            'hostname': 'echo custom.localhost',
            'hostname_method': 'shell',
        }
        c = Collector(config, [])
        self.assertEquals('custom.localhost', c.get_hostname())
