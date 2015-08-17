#!/usr/bin/python
# coding=utf-8
################################################################################
import os
from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import Mock
from mock import patch

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from docker import Client
except ImportError:
    Client = None

from diamond.collector import Collector
from memory_docker import MemoryDockerCollector

dirname = os.path.dirname(__file__)
fixtures_path = os.path.join(dirname, 'fixtures/')
fixtures = []
for root, dirnames, filenames in os.walk(fixtures_path):
    fixtures.append([root, dirnames, filenames])

docker_fixture = [
    {u'Id': u'c3341726a9b4235a35b390c5f6f28e5a6869879a48da1d609db8f6bf4275bdc5',
     u'Names': [u'/testcontainer']},
    {u'Id': u'8c209083474e13f695d5eee01d090ba474a79f1d74ce236f08ffb22419fb6127',
     u'Names': [u'/testcontainer/testcontainer2', u'/testcontainer2']},
    {u'Id': u'9c151939e20682b924d7299875e94a4aabbe946b30b407f89e276507432c625b',
     u'Names': None},
    {u'Id': u'e8b0b1189abcf13aa438f0983328fed7b7a3ff54e445cfbd1a7a359f9855a45a',
     u'Names': None}]

docker_new_paths = [
    'docker-8c209083474e13f695d5eee01d090ba474a79f1d74ce236f08ffb22419fb6127',
    'docker-8c209083474e13f695d5eee01d090ba474a79f1d74ce236f08ffb22419fb6128',
]


def run_only_if_docker_client_is_available(func):
    try:
        from docker import Client
    except ImportError:
        Client = None
    pred = lambda: Client is not None
    return run_only(func, pred)


class TestMemoryDockerCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('MemoryDockerCollector', {
            'interval': 10,
            'byte_unit': 'megabyte',
            'memory_path': fixtures_path,
        })

        self.collector = MemoryDockerCollector(config, None)

    def test_import(self):
        self.assertTrue(MemoryDockerCollector)

    @run_only_if_docker_client_is_available
    @patch('__builtin__.open')
    @patch.object(Client, 'containers', Mock(return_value=[]))
    @patch.object(Collector, 'publish')
    def test_should_open_all_cpuacct_stat(self, publish_mock, open_mock):
        open_mock.side_effect = lambda x: StringIO('')
        self.collector.collect()
        open_mock.assert_any_call(
            fixtures_path + 'lxc/testcontainer/memory.stat')
        open_mock.assert_any_call(
            fixtures_path + 'lxc/testcontainer2/memory.stat')
        for docker_new in docker_new_paths:
            open_mock.assert_any_call(
                fixtures_path + docker_new + '/memory.stat')
        open_mock.assert_any_call(fixtures_path + 'lxc/memory.stat')
        open_mock.assert_any_call(fixtures_path + 'memory.stat')

    @run_only_if_docker_client_is_available
    @patch('__builtin__.open')
    @patch.object(Client, 'containers')
    @patch.object(Collector, 'publish')
    def test_should_get_containers(self, publish_mock, containers_mock,
                                   open_mock):
        containers_mock.return_value = []
        open_mock.side_effect = lambda x: StringIO('')
        self.collector.collect()
        containers_mock.assert_any_call(all=True)

    @run_only_if_docker_client_is_available
    @patch.object(Collector, 'publish')
    @patch.object(Client, 'containers',
                  Mock(return_value=docker_fixture))
    def test_should_work_with_real_data(self, publish_mock):
        self.collector.filter_existing = False
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'lxc.testcontainer.cache': 1,
            'lxc.testcontainer.rss': 1,
            'lxc.testcontainer.swap': 1,
            'lxc.cache': 1,
            'lxc.rss': 1,
            'lxc.swap': 1,
            'system.cache': 1,
            'system.rss': 1,
            'system.swap': 1,
            'docker.testcontainer.cache': 1,
            'docker.testcontainer.rss': 1,
            'docker.testcontainer.swap': 1,
            'docker.testcontainer2.cache': 1,
            'docker.testcontainer2.rss': 1,
            'docker.testcontainer2.swap': 1,
            'docker.c3341726a9b4235a35b390c5f6f28e5a'
            '6869879a48da1d609db8f6bf4275bdc6.cache': 1,
            'docker.c3341726a9b4235a35b390c5f6f28e5a'
            '6869879a48da1d609db8f6bf4275bdc6.rss': 1,
            'docker.c3341726a9b4235a35b390c5f6f28e5a'
            '6869879a48da1d609db8f6bf4275bdc6.swap': 1,
            'docker.8c209083474e13f695d5eee01d090ba4'
            '74a79f1d74ce236f08ffb22419fb6128.cache': 1,
            'docker.8c209083474e13f695d5eee01d090ba4'
            '74a79f1d74ce236f08ffb22419fb6128.rss': 1,
            'docker.8c209083474e13f695d5eee01d090ba4'
            '74a79f1d74ce236f08ffb22419fb6128.swap': 1,
            'docker.cache': 1,
            'docker.rss': 1,
            'docker.swap': 1,
            'docker.service.cache': 1,
            'docker.service.rss': 1,
            'docker.service.swap': 1,
        })
        self.assertUnpublishedMany(publish_mock, {
            'docker.testcontainer.testcontainer2.cache': 1,
            'docker.testcontainer.testcontainer2.rss': 1,
            'docker.testcontainer.testcontainer2.swap': 1,
            'docker-8c209083474e13f695d5eee01d090ba4'
            '74a79f1d74ce236f08ffb22419fb6128.cache': 1,
            'docker-8c209083474e13f695d5eee01d090ba4'
            '74a79f1d74ce236f08ffb22419fb6128.rss': 1,
            'docker-8c209083474e13f695d5eee01d090ba4'
            '74a79f1d74ce236f08ffb22419fb6128.swap': 1,
        })

    @run_only_if_docker_client_is_available
    @patch.object(Collector, 'publish')
    @patch.object(Client, 'containers',
                  Mock(return_value=docker_fixture))
    def test_should_ignore_nonexistent_containers(self, publish_mock):
        self.collector.filter_existing = True
        self.collector.collect()

        self.assertUnpublishedMany(publish_mock, {
            'docker.c3341726a9b4235a35b390c5f6f28e5a'
            '6869879a48da1d609db8f6bf4275bdc6.cache': 1,
            'docker.c3341726a9b4235a35b390c5f6f28e5a'
            '6869879a48da1d609db8f6bf4275bdc6.rss': 1,
            'docker.c3341726a9b4235a35b390c5f6f28e5a'
            '6869879a48da1d609db8f6bf4275bdc6.swap': 1,
            'docker.8c209083474e13f695d5eee01d090ba4'
            '74a79f1d74ce236f08ffb22419fb6128.cache': 1,
            'docker.8c209083474e13f695d5eee01d090ba4'
            '74a79f1d74ce236f08ffb22419fb6128.rss': 1,
            'docker.8c209083474e13f695d5eee01d090ba4'
            '74a79f1d74ce236f08ffb22419fb6128.swap': 1,
            'docker-8c209083474e13f695d5eee01d090ba4'
            '74a79f1d74ce236f08ffb22419fb6128.cache': 1,
            'docker-8c209083474e13f695d5eee01d090ba4'
            '74a79f1d74ce236f08ffb22419fb6128.rss': 1,
            'docker-8c209083474e13f695d5eee01d090ba4'
            '74a79f1d74ce236f08ffb22419fb6128.swap': 1,
        })

    @run_only_if_docker_client_is_available
    @patch.object(Collector, 'publish')
    @patch.object(Client, 'containers',
                  Mock(return_value=docker_fixture))
    def test_should_truncate_container_id_including_nonexistent(self,
                                                                publish_mock):
        self.collector.truncate_ids = 12
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'docker.e8b0b1189abc.cache': 1,
            'docker.e8b0b1189abc.rss': 1,
            'docker.e8b0b1189abc.swap': 1,
            'docker.c3341726a9b4.cache': 1,
            'docker.c3341726a9b4.rss': 1,
            'docker.c3341726a9b4.swap': 1,
        })

    @run_only_if_docker_client_is_available
    @patch.object(Collector, 'publish')
    @patch.object(Client, 'containers',
                  Mock(return_value=docker_fixture))
    def test_should_truncate_container_id_excluding_nonexistent(self,
                                                                publish_mock):
        self.collector.filter_existing = True
        self.collector.truncate_ids = 12
        self.collector.collect()

        self.assertPublishedMany(publish_mock, {
            'docker.e8b0b1189abc.cache': 1,
            'docker.e8b0b1189abc.rss': 1,
            'docker.e8b0b1189abc.swap': 1,
        })
        self.assertUnpublishedMany(publish_mock, {
            'docker.c3341726a9b4.cache': 1,
            'docker.c3341726a9b4.rss': 1,
            'docker.c3341726a9b4.swap': 1,
            'docker.c3341726a9b4235a35b390c5f6f28e5a'
            '6869879a48da1d609db8f6bf4275bdc6.cache': 1,
            'docker.c3341726a9b4235a35b390c5f6f28e5a'
            '6869879a48da1d609db8f6bf4275bdc6.rss': 1,
            'docker.c3341726a9b4235a35b390c5f6f28e5a'
            '6869879a48da1d609db8f6bf4275bdc6.swap': 1,
        })

if __name__ == "__main__":
    unittest.main()
