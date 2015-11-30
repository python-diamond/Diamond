#!/usr/bin/python
# coding=utf-8
##########################################################################

import os

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch

import amavis
from diamond.collector import Collector

##########################################################################

MOCK_PATH = os.path.join(os.path.dirname(__file__), 'mock-amavisd-agent')


class TestAmavisCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('AmavisCollector', {
            'amavisd_exe': MOCK_PATH,
        })

        self.collector = amavis.AmavisCollector(config, None)

    @patch.object(Collector, 'publish')
    def test_publish(self, publish_mock):
        self.collector.collect()

        # a couple of the metrics contained in mock-amavisd-agent
        metrics = {
            'sysUpTime.time': 198103058,
            'OutMsgsSizeProtoSMTP.size': 116,
            'OutMsgsSizeProtoSMTP.frequency': 0,
            'OutMsgsSizeProtoSMTP.percentage': 96.4,
            'OutMsgsProtoSMTPRelay.count': 22778,
            'OutMsgsProtoSMTPRelay.frequency': 41,
            'OutMsgsProtoSMTPRelay.percentage': 71.5,
            'TimeElapsedDecoding.time': 652,
            'TimeElapsedDecoding.frequency': 0.024,
            'virus.byname.Eicar-Test-Signature.count': 4436,
            'virus.byname.Eicar-Test-Signature.frequency': 8,
            'virus.byname.Eicar-Test-Signature.percentage': 100.0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    @patch('amavis.subprocess.Popen')
    def test_amavisd_agent_command(self, popen_mock, publish_mock):
        config = get_collector_config('AmavisCollector', {})
        amavis.AmavisCollector(config, None).collect()

        popen_mock.assert_called_with(
            ['/usr/sbin/amavisd-agent', '-c', '1'],
            stdout=-1
        )

    @patch.object(Collector, 'publish')
    @patch('amavis.subprocess.Popen')
    def test_amavisd_agent_command_with_sudo(self, popen_mock, publish_mock):
        config = get_collector_config('AmavisCollector', {
            'use_sudo': True,
            'sudo_user': 'chosen_sudo_user',
        })
        amavis.AmavisCollector(config, None).collect()

        popen_mock.assert_called_with(
            ['/usr/bin/sudo', '-u', 'chosen_sudo_user', '--',
             '/usr/sbin/amavisd-agent', '-c', '1'],
            stdout=-1
        )


##########################################################################
if __name__ == "__main__":
    unittest.main()
