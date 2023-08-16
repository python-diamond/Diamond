#!/usr/bin/env python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from mock import Mock
from mock import patch
from test import unittest
from diamond.collector import Collector

from novahypervisorstats import NovaHypervisorStatsCollector

##########################################################################


class TestNovaHypervisorStatsCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('NovaHypervisorStatsCollector', {
            'interval': 10
        })

        self.collector = NovaHypervisorStatsCollector(config, None)

    def test_import(self):
        self.assertTrue(NovaHypervisorStatsCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        instance = novaclient.client.HTTPClient(user='user',
                                                password='password',
                                                projectid='project',
                                                timeout=2,
                                                auth_url="http://www.blah.com")
        self.assertEqual(2, instance.timeout)
        mock_request = mock.Mock()
        mock_request.return_value = requests.Response()
        mock_request.return_value.status_code = 200
        mock_request.return_value.headers = {
            'x-server-management-url': 'blah.com',
            'x-auth-token': 'blah',
        }
        with mock.patch('requests.request', mock_request):
            instance.authenticate()
            requests.request.assert_called_with(
                mock.ANY, mock.ANY, timeout=2, headers=mock.ANY,
                verify=mock.ANY)

##########################################################################
if __name__ == "__main__":
    unittest.main()
