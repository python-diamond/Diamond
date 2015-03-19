#!/usr/bin/python
# coding=utf-8
################################################################################
import socket

from mock import Mock, patch

from snmp import SNMPCollector
from test import CollectorTestCase, get_collector_config


class TestSNMPCollector(CollectorTestCase):

    def setUp(self, allowed_names=None):
        if not allowed_names:
            allowed_names = []

        config = get_collector_config('SNMPCollector', {
            'allowed_names': allowed_names,
            'interval': 1
        })

        self.collector = SNMPCollector(config, None)

    def test_import(self):
        self.assertTrue(SNMPCollector)

    def test_default_config(self):
        config = self.collector.get_default_config()
        self.assertEqual(config['path'], 'snmp')
        self.assertEqual(config['timeout'], 5)
        self.assertEqual(config['retries'], 3)
        self.assertEqual(config['devices'], {})

    def test_to_oid_tuple(self):
        self.assertEqual((1, 2, 3), self.collector._to_oid_tuple('1.2.3'))

    def test_to_oid_tuple_handles_tuple(self):
        tup = (1, 2, 3)
        self.assertEqual(tup, self.collector._to_oid_tuple(tup))

    def test_from_oid_tuple(self):
        self.assertEqual('1.2.3', self.collector._from_oid_tuple((1, 2, 3)))

    def test_from_oid_tuple_handles_string(self):
        string = '1.2.3'
        self.assertEqual(string, self.collector._from_oid_tuple(string))

    def test_publish_empty_value(self):
        with patch.object(self.collector, 'publish_gauge'):
            self.collector._publish('device', 'x', 'y', 'name', None)
            self.assertFalse(self.collector.publish_gauge.called)

    @patch('snmp.IntegerType', Mock)
    def test_publish_path_replacement(self):
        name = Mock(prettyPrint=lambda: '1.2.3.1.2.3')
        value = Mock(prettyPrint=lambda: '42')

        with patch.object(self.collector, 'publish_gauge'):
            self.collector._publish('device', '1.2', 'foo', name, value)
            self.collector.publish_gauge.assert_called_with(
                'devices.device.foo.3.1.2.3', '42'
            )

    @patch('snmp.IntegerType', int)
    def test_publish_non_integer_type(self):
        value = Mock(prettyPrint=lambda: 'value')
        with patch.object(self.collector, 'publish_gauge'):
            self.collector._publish('device', 'x', 'y', 'name', value)
            self.assertFalse(self.collector.publish_gauge.called)

    @patch('snmp.IntegerType', int)
    def test_publish_non_integer_type_conversion(self):
        name = Mock(prettyPrint=lambda: 'name')
        value = Mock(prettyPrint=lambda: '42')
        with patch.object(self.collector, 'publish_gauge'):
            self.collector._publish('device', 'x', 'y', name, value)
            self.collector.publish_gauge.assert_called_with(
                'devices.device.name', 42.0
            )

    @patch('snmp.IntegerType', Mock)
    def test_publish(self):
        name = Mock(prettyPrint=lambda: '1.2.3')
        value = Mock(prettyPrint=lambda: '42')

        with patch.object(self.collector, 'publish_gauge'):
            self.collector._publish('device', '1.2', 'foo', name, value)
            self.collector.publish_gauge.assert_called_with(
                'devices.device.foo.3', '42'
            )

    def test_snmp_get_no_metrics(self):
        retvals = [
            [],  # IndexError
            (None, None, None, []),  # IndexError
            (None, None, None, ['foo']),  # ValueError
        ]

        for retval in retvals:
            self.collector.cmdgen = Mock()
            self.collector.cmdgen.getCmd.return_value = []

            auth = Mock()
            transport = Mock(transportAddr=('localhost', 161))
            metrics = self.collector.snmp_get('1.2', auth, transport)

            self.assertEqual([], metrics)

    def test_snmp_get(self):
        name = Mock()
        value = Mock()

        self.collector.cmdgen = Mock()
        self.collector.cmdgen.getCmd.return_value = (
            None, None, None, [(name, value)]
        )

        auth = Mock()
        transport = Mock()

        metrics = self.collector.snmp_get('1.2', auth, transport)
        self.assertEqual(metrics, [(name, value)])

    def test_snmp_walk_no_metrics(self):
        for retval in ([], (None, None, None, [])):
            self.collector.cmdgen = Mock()
            self.collector.cmdgen.nextCmd.return_value = retval

            auth = Mock()
            transport = Mock(transportAddr=('localhost', 161))
            metrics = self.collector.snmp_walk('1.2', auth, transport)

            self.assertEqual([], list(metrics))

    def test_snmp_walk(self):
        metrics = (None, None, None, [
            [(Mock(prettyPrint=lambda: '1.2.1'),
             Mock(prettyPrint=lambda: '41'))],
            [(Mock(prettyPrint=lambda: '1.2.2'),
             Mock(prettyPrint=lambda: '42'))],
            [(Mock(prettyPrint=lambda: '1.2.3'),
             Mock(prettyPrint=lambda: '43'))],
        ])

        expected = [x[0] for x in metrics[3]]

        self.collector.cmdgen = Mock()
        self.collector.cmdgen.nextCmd.return_value = metrics

        auth = Mock()
        transport = Mock(transportAddr=('localhost', 161))

        ret_metrics = list(self.collector.snmp_walk('1.2', auth, transport))
        self.assertEqual(expected, ret_metrics)

    @patch('snmp.IntegerType', Mock)
    @patch('snmp.cmdgen', Mock())
    def test_collect_calls_snmp_get(self):
        device = 'mydevice'
        oids = {
            '1.2.3': 'foo.bar',
        }

        self.collector.config.update({
            'devices': {
                'mydevice': {
                    'oids': oids,
                },
            },
        })

        metrics = [
            (Mock(prettyPrint=lambda: '1.2.3'),
             Mock(prettyPrint=lambda: '42')),
            (Mock(prettyPrint=lambda: '1.2.3.4'),
             Mock(prettyPrint=lambda: '43')),
        ]

        with patch.multiple(self.collector,
                            snmp_get=Mock(),
                            snmp_walk=Mock(),
                            publish_metric=Mock()):
            self.collector.snmp_get.return_value = metrics

            self.collector.collect_snmp(device, 'localhost', 161, 'public')

            # Are we calling the correct method
            self.assertFalse(self.collector.snmp_walk.called)
            self.assertTrue(self.collector.snmp_get.called)

            calls = self.collector.publish_metric.call_args_list

            # Do we publish metrics?
            self.assertEqual(len(calls), 2)
            prefix = 'servers.{0}.snmp'.format(socket.gethostname())

            # Were metrics properly namespaced
            self.assertEqual(calls[0][0][0].path,
                             '{0}.devices.mydevice.foo.bar'.format(prefix))
            self.assertEqual(calls[1][0][0].path,
                             '{0}.devices.mydevice.foo.bar.4'.format(prefix))

    @patch('snmp.IntegerType', Mock)
    @patch('snmp.cmdgen', Mock())
    def test_collect_calls_snmp_walk(self):
        device = 'mydevice'
        oids = {
            '1.2.3.*': 'foo.bar',
        }

        self.collector.config.update({
            'devices': {
                'mydevice': {
                    'oids': oids,
                },
            },
        })

        metrics = [
            (Mock(prettyPrint=lambda: '1.2.3'),
             Mock(prettyPrint=lambda: '42')),
            (Mock(prettyPrint=lambda: '1.2.3.4'),
             Mock(prettyPrint=lambda: '43')),
        ]

        with patch.multiple(self.collector,
                            snmp_get=Mock(),
                            snmp_walk=Mock(),
                            publish_metric=Mock()):
            self.collector.snmp_walk.return_value = metrics

            self.collector.collect_snmp(device, 'localhost', 161, 'public')

            # Are we calling the correct method
            self.assertTrue(self.collector.snmp_walk.called)
            self.assertFalse(self.collector.snmp_get.called)

            calls = self.collector.publish_metric.call_args_list

            # Do we publish metrics?
            self.assertEqual(len(calls), 2)
            prefix = 'servers.{0}.snmp'.format(socket.gethostname())

            # Were metrics properly namespaced
            self.assertEqual(calls[0][0][0].path,
                             '{0}.devices.mydevice.foo.bar'.format(prefix))
            self.assertEqual(calls[1][0][0].path,
                             '{0}.devices.mydevice.foo.bar.4'.format(prefix))

    @patch('snmp.cmdgen', None)
    def test_collect_nothing_with_pysnmp_error(self):
        with patch.object(self.collector, 'log'):
            self.collector.collect()
            self.collector.log.error.assert_called_with(
                'pysnmp.entity.rfc3413.oneliner.cmdgen failed to load'
            )

    @patch('snmp.cmdgen')
    def test_collect_no_devices(self, cmdgen):
        with patch.multiple(self.collector, log=Mock(), config={}):
            self.collector.collect()
            self.collector.log.error.assert_called_with(
                'No devices configured for this collector'
            )

    @patch('snmp.cmdgen')
    def test_collect(self, cmdgen):
        oids = {
            '1.2.3': 'foo.bar',
        }

        config = {
            'devices': {
                'mydevice': {
                    'host': 'localhost',
                    'port': 161,
                    'community': 'public',
                    'oids': oids,
                }
            }
        }

        # Setup mocks
        auth = Mock()
        auth.return_value = auth

        transport = Mock()
        transport.return_value = transport

        collect_snmp = Mock()

        with patch.multiple(self.collector,
                            config=config,
                            collect_snmp=collect_snmp):
            self.collector.collect()
            collect_snmp.assert_called_with(
                'mydevice', 'localhost', 161, 'public'
            )

    @patch('snmp.cmdgen')
    def test_collect_uses_defaults(self, cmdgen):
        oids = {
            '1.2.3': 'foo.bar',
        }

        # We should allow assuming default values for community and port
        config = {
            'devices': {
                'mydevice': {
                    'host': 'localhost',
                    'oids': oids,
                }
            }
        }

        # Setup mocks
        auth = Mock()
        auth.return_value = auth

        transport = Mock()
        transport.return_value = transport

        collect_snmp = Mock()

        with patch.multiple(self.collector,
                            config=config,
                            collect_snmp=collect_snmp):
            self.collector.collect()
            collect_snmp.assert_called_with(
                'mydevice', 'localhost', 161, 'public'
            )
