#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import unittest
from mock import patch
from diamond.metric import Metric
import urllib2
import configobj
import StringIO
import gzip
import contextlib
import json

from diamond.handler.tsdb import TSDBHandler


@patch('diamond.handler.tsdb.urllib2.urlopen')
@patch('diamond.handler.tsdb.urllib2.Request')
class TestTSDBdHandler(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:4242/api/put'

    def decompress(self, input):
        infile = StringIO.StringIO()
        infile.write(input)
        with contextlib.closing(gzip.GzipFile(fileobj=infile, mode="r")) as f:
            f.rewind()
            out = f.read()
            return out

    def test_HTTPError(self, mock_request, mock_urlopen):
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')
        handler = TSDBHandler(config)
        header = {'Content-Type': 'application/json'}
        exception = urllib2.HTTPError(url=self.url, code=404, msg="Error",
                                      hdrs=header, fp=None)
        handler.side_effect = exception
        handler.process(metric)

    def test_single_metric(self, mock_request, mock_urlopen):
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')
        handler = TSDBHandler(config)
        handler.process(metric)
        body = [{"timestamp": 1234567,
                 "metric": "cpu.cpu_count",
                 "value": 123,
                 "tags": {"hostname": "myhostname"}}]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_compression(self, mock_request, mock_urlopen):
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['compression'] = 1
        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')
        handler = TSDBHandler(config)
        handler.process(metric)
        body = [{"timestamp": 1234567,
                 "metric": "cpu.cpu_count",
                 "value": 123,
                 "tags": {"hostname": "myhostname"}}]
        passed_headers = mock_request.call_args[0][2]
        passed_body = mock_request.call_args[0][1]
        assert passed_headers['Content-Encoding'] == 'gzip'
        assert passed_headers['Content-Type'] == 'application/json'
        assert json.loads(self.decompress(passed_body)) == body

    def test_user_password(self, mock_request, mock_urlopen):
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['user'] = 'John Doe'
        config['password'] = '123456789'
        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')
        handler = TSDBHandler(config)
        handler.process(metric)
        body = [{"timestamp": 1234567,
                 "metric": "cpu.cpu_count",
                 "value": 123,
                 "tags": {"hostname": "myhostname"}}]
        header = {'Content-Type': 'application/json',
                  'Authorization': 'Basic Sm9obiBEb2U6MTIzNDU2Nzg5'}
        self.check_request_param(mock_request, body, header)

    def test_batch(self, mock_request, mock_urlopen):
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['batch'] = 2
        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')
        metric2 = Metric('servers.myhostname.cpu.cpu_time',
                         123, raw_value=456, timestamp=5678910,
                         host='myhostname', metric_type='GAUGE')
        handler = TSDBHandler(config)
        handler.process(metric)
        handler.process(metric2)
        body = [
            {
                "timestamp": 1234567,
                "metric": "cpu.cpu_count",
                "value": 123,
                "tags": {"hostname": "myhostname"}},
            {
                "timestamp": 5678910,
                "metric": "cpu.cpu_time",
                "value": 123,
                "tags": {"hostname": "myhostname"}
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_tags(self, mock_request, mock_urlopen):
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = 'tag1=tagv1 tag2=tagv2'
        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')
        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "cpu.cpu_count",
                "value": 123,
                "tags": {
                    "hostname": "myhostname",
                    "tag1": "tagv1",
                    "tag2": "tagv2"
                }
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_prefix(self, mock_request, mock_urlopen):
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['prefix'] = 'diamond'
        metric = Metric('servers.myhostname.cpu.cpu_count',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')
        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "diamond.cpu.cpu_count",
                "value": 123,
                "tags": {"hostname": "myhostname"}
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_cpu_metrics_taghandling_default(self, mock_request, mock_urlopen):
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = ['myFirstTag=myValue']

        metric = Metric('servers.myhostname.cpu.cpu0.user',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "cpu.user",
                "value": 123,
                "tags": {
                    "cpuId": "cpu0",
                    "myFirstTag": "myValue",
                    "hostname": "myhostname"
                }
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_cpu_metrics_taghandling_0(self, mock_request, mock_urlopen):
        """
        deactivate
        """
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = ['myFirstTag=myValue']
        config['cleanMetrics'] = False

        metric = Metric('servers.myhostname.cpu.cpu0.user',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "cpu.cpu0.user",
                "value": 123,
                "tags": {
                    "myFirstTag": "myValue",
                    "hostname": "myhostname"
                }
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_cpu_metrics_taghandling_default(self, mock_request, mock_urlopen):
        """
        aggregate default
        """
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = ['myFirstTag=myValue']

        metric = Metric('servers.myhostname.cpu.total.user',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        handler = TSDBHandler(config)
        handler.process(metric)
        assert not mock_urlopen.called, "should not process"

    def test_cpu_metrics_taghandling_1(self, mock_request, mock_urlopen):
        """
        aggregate deactivate
        """
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = ['myFirstTag=myValue']
        config['cleanMetrics'] = False

        metric = Metric('servers.myhostname.cpu.total.user',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "cpu.total.user",
                "value": 123,
                "tags": {
                    "myFirstTag": "myValue",
                    "hostname": "myhostname"
                }
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_cpu_metrics_taghandling_2(self, mock_request, mock_urlopen):
        """
        aggregate deactivate
        """
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = ['myFirstTag=myValue']
        config['cleanMetrics'] = True
        config['skipAggregates'] = False

        metric = Metric('servers.myhostname.cpu.total.user',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "cpu.user",
                "value": 123,
                "tags": {
                    "cpuId": "total",
                    "myFirstTag": "myValue",
                    "hostname": "myhostname"
                }
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_haproxy_metrics_default(self, mock_request, mock_urlopen):
        """
        taghandling default
        """
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = ['myFirstTag=myValue']

        metric = Metric('servers.myhostname.haproxy.SOME-BACKEND.SOME-SERVER.'
                        'bin',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "haproxy.bin",
                "value": 123,
                "tags": {
                    "backend": "SOME-BACKEND",
                    "myFirstTag": "myValue",
                    "hostname": "myhostname",
                    "server": "SOME-SERVER"
                }
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_haproxy_metrics(self, mock_request, mock_urlopen):
        """
        taghandling deactivate
        """
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = ['myFirstTag=myValue']
        config['cleanMetrics'] = False

        metric = Metric('servers.myhostname.haproxy.SOME-BACKEND.SOME-SERVER.'
                        'bin',
                        123, raw_value=123, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "haproxy.SOME-BACKEND.SOME-SERVER.bin",
                "value": 123,
                "tags": {
                    "myFirstTag": "myValue",
                    "hostname": "myhostname"
                }
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_diskspace_metrics_default(self, mock_request, mock_urlopen):
        """
        taghandling default
        """
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = ['myFirstTag=myValue']

        metric = Metric('servers.myhostname.diskspace.MOUNT_POINT.byte_percent'
                        'free',
                        80, raw_value=80, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "diskspace.byte_percentfree",
                "value": 80,
                "tags": {
                    "mountpoint": "MOUNT_POINT",
                    "myFirstTag": "myValue",
                    "hostname": "myhostname"
                }
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_diskspace_metrics(self, mock_request, mock_urlopen):
        """
        taghandling deactivate
        """
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = ['myFirstTag=myValue']
        config['cleanMetrics'] = False

        metric = Metric('servers.myhostname.diskspace.MOUNT_POINT.byte_'
                        'percentfree',
                        80, raw_value=80, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "diskspace.MOUNT_POINT.byte_percentfree",
                "value": 80,
                "tags": {
                    "myFirstTag": "myValue",
                    "hostname": "myhostname"
                }
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_iostat_metrics_default(self, mock_request, mock_urlopen):
        """
        taghandling default
        """
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = ['myFirstTag=myValue']

        metric = Metric('servers.myhostname.iostat.DEV.io_in_progress',
                        80, raw_value=80, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "iostat.io_in_progress",
                "value": 80,
                "tags": {
                    "device": "DEV",
                    "myFirstTag": "myValue",
                    "hostname": "myhostname"
                }
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_iostat_metrics(self, mock_request, mock_urlopen):
        """
        taghandling deactivate
        """
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = ['myFirstTag=myValue']
        config['cleanMetrics'] = False

        metric = Metric('servers.myhostname.iostat.DEV.io_in_progress',
                        80, raw_value=80, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "iostat.DEV.io_in_progress",
                "value": 80,
                "tags":
                    {
                        "myFirstTag": "myValue",
                        "hostname": "myhostname"
                    }
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_network_metrics_default(self,mock_request, mock_urlopen):
        """
        taghandling default
        """
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = ['myFirstTag=myValue']

        metric = Metric('servers.myhostname.network.IF.rx_packets',
                        80, raw_value=80, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "network.rx_packets",
                "value": 80,
                "tags": {
                    "interface": "IF",
                    "myFirstTag": "myValue",
                    "hostname": "myhostname"
                }
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def test_network_metrics(self, mock_request, mock_urlopen):
        """
        taghandling deactivate
        """
        config = configobj.ConfigObj()
        config['host'] = '127.0.0.1'
        config['port'] = '4242'
        config['tags'] = ['myFirstTag=myValue']
        config['cleanMetrics'] = False

        metric = Metric('servers.myhostname.network.IF.rx_packets',
                        80, raw_value=80, timestamp=1234567,
                        host='myhostname', metric_type='GAUGE')

        handler = TSDBHandler(config)
        handler.process(metric)
        body = [
            {
                "timestamp": 1234567,
                "metric": "network.IF.rx_packets",
                "value": 80,
                "tags": {
                    "myFirstTag": "myValue",
                    "hostname": "myhostname"
                }
            }
        ]
        header = {'Content-Type': 'application/json'}
        self.check_request_param(mock_request, body, header)

    def check_request_param(self, mock, body, header):
        actual_body = json.loads(mock.call_args[0][1])
        self.assertEqual(actual_body, body)
        actual_url = mock.call_args[0][0]
        self.assertEqual(actual_url, self.url)
        actual_header = mock.call_args[0][2]
        self.assertEqual(actual_header, header)

