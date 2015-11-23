from test import CollectorTestCase
from test import get_collector_config

from mock import call, Mock, patch
from unittest import TestCase

from diamond.collector import Collector

from portstat import get_port_stats, PortStatCollector


class PortStatCollectorTestCase(CollectorTestCase):

    TEST_CONFIG = {
        'port': {
            'something1': {
                'number': 5222,
            },
            'something2': {
                'number': 8888,
            }
        }
    }

    def setUp(self):
        config = get_collector_config('PortStatCollector',
                                      self.TEST_CONFIG)

        self.collector = PortStatCollector(config, None)

    def test_import(self):
        self.assertTrue(PortStatCollector)

    @patch('portstat.get_port_stats')
    @patch.object(Collector, 'publish')
    def test_collect(self, publish_mock, get_port_stats_mock):

        get_port_stats_mock.return_value = {'foo': 1}

        self.collector.collect()

        get_port_stats_mock.assert_has_calls([call(5222), call(8888)],
                                             any_order=True)
        self.assertPublished(publish_mock, 'something1.foo', 1)
        self.assertPublished(publish_mock, 'something2.foo', 1)


class GetPortStatsTestCase(TestCase):

    @patch('portstat.psutil.net_connections')
    def test_get_port_stats(self, net_connections_mock):

        ports = [Mock() for _ in range(5)]

        ports[0].laddr = (None, 5222)
        ports[0].status = 'ok'
        ports[1].laddr = ports[2].laddr = ports[3].laddr = (None, 8888)
        ports[1].status = 'ok'
        ports[2].status = 'OK'
        ports[3].status = 'bad'
        ports[4].laddr = (None, 9999)

        net_connections_mock.return_value = ports

        cnts = get_port_stats(5222)

        self.assertEqual(net_connections_mock.call_count, 1)
        self.assertEqual(cnts, {'ok': 1})

        cnts = get_port_stats(8888)

        self.assertEqual(net_connections_mock.call_count, 2)
        self.assertEqual(cnts, {'ok': 2, 'bad': 1})
