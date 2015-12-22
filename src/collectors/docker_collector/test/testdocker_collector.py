#!/usr/bin/python
# coding=utf-8
##########################################################################
import os
from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from test import run_only
from mock import Mock
from mock import patch
from mock import mock_open

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from docker import Client
except ImportError:
    Client = None

from diamond.collector import Collector
from docker_collector import DockerCollector

dirname = os.path.dirname(__file__)
fixtures_path = os.path.join(dirname, 'fixtures/')
fixtures = []
for root, dirnames, filenames in os.walk(fixtures_path):
    fixtures.append([root, dirnames, filenames])

docker_fixture = [
    {u'Id': u'c3341726a9b4235a35b390c5f6f28e5a6869879a48da1d609db8f6bf4275bdc5',
     u'Names': [u'/testcontainer']},
    {u'Id': u'0aec7f643ca1cb45f54d41dcabd8fcbcfcbc57170c3e6dd439af1a52761c2bed',
     u'Names': [u'/testcontainer3']},
    {u'Id': u'9c151939e20682b924d7299875e94a4aabbe946b30b407f89e276507432c625b',
     u'Names': None}]


def run_only_if_docker_client_is_available(func):
    try:
        from docker import Client
    except ImportError:
        Client = None
    pred = lambda: Client is not None
    return run_only(func, pred)


class TestDockerCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('DockerCollector', {
            'interval': 10,
            'byte_unit': 'megabyte',
            'memory_path': fixtures_path,
        })

        self.collector = DockerCollector(config, None)

    def test_import(self):
        self.assertTrue(DockerCollector)

    def test_finds_linux_v2_memory_stat_path(self):
        tid = 'c3341726a9b4235a35b390c5f6f28e5a6869879a48da1d609db8f6bf4275bdc5'
        path = self.collector._memory_stat_path(tid)
        self.assertTrue(path is not None)
        self.assertTrue(os.path.exists(path))

    def test_finds_linux_v3_memory_stat_path(self):
        tid = '0aec7f643ca1cb45f54d41dcabd8fcbcfcbc57170c3e6dd439af1a52761c2bed'
        path = self.collector._memory_stat_path(tid)
        self.assertTrue(path is not None)
        self.assertTrue(os.path.exists(path))

    def test_doesnt_find_bogus_memory_stat_path(self):
        tid = 'testcontainer'
        path = self.collector._memory_stat_path(tid)
        self.assertTrue(path is None)

    @patch('os.path.exists', Mock(return_value=True))
    def test_default_memory_path(self):
        read_data = "\n".join([
            'none /selinux selinuxfs rw,relatime 0 0',
            'cgroup /goofy/memory cgroup'
            ' rw,nosuid,nodev,noexec,relatime,devices 0 0',
            'cgroup /mickeymouse/memory cgroup'
            ' rw,nosuid,nodev,noexec,relatime,memory 0 0',
            'tmpfs /dev/shm tmpfs rw,seclabel,nosuid,nodev 0 0',
            '',
        ])

        m = mock_open(read_data=read_data)
        with patch('__builtin__.open', m, create=True):
            self.assertEqual(self.collector._default_memory_path(),
                             '/mickeymouse/memory')

        m.assert_called_once_with('/proc/mounts')

    # @run_only_if_docker_client_is_available
    # @patch.object(Collector, 'publish')
    # @patch.object(Client, 'containers', Mock(return_value=[]))
    # @patch.object(Client, 'images', Mock(return_value=[]))
    # def test_collect_sunny_day(self, publish_mock):
    #     self.assertTrue(self.collector.collect())
    #     self.assertPublishedMany(publish_mock, {
    #         'containers_running_count': 100,
    #         'containers_stopped_count': 100,
    #         'images_count': 100,
    #         'images_dangling_count': 100,
    #         })

    # @run_only_if_docker_client_is_available
    # @patch('__builtin__.open')
    # @patch.object(Client, 'containers', Mock(return_value=[]))
    # @patch.object(Collector, 'publish')
    # def test_should_open_memory_stat(self, publish_mock, open_mock):
    #     # open_mock.side_effect = lambda x: StringIO('')
    #     self.collector.collect()
    #     print open_mock.mock_calls
    #     open_mock.assert_any_call(fixtures_path +
    #         'docker/c3341726a9b4235a35b'
    #         '390c5f6f28e5a6869879a48da1d609db8f6bf4275bdc5/memory.stat')
    #     # open_mock.assert_any_call(fixtures_path +
    #         'lxc/testcontainer/memory.stat')
    #     # open_mock.assert_any_call(fixtures_path + 'lxc/memory.stat')
    #     # open_mock.assert_any_call(fixtures_path + 'memory.stat')

    # @run_only_if_docker_client_is_available
    # @patch('__builtin__.open')
    # @patch.object(Client, 'containers')
    # @patch.object(Collector, 'publish')
    # def test_should_get_containers(self, publish_mock, containers_mock,
    #                                open_mock):
    #     containers_mock.return_value = []
    #     open_mock.side_effect = lambda x: StringIO('')
    #     self.collector.collect()
    #     containers_mock.assert_any_call(all=True)

    # @run_only_if_docker_client_is_available
    # @patch.object(Collector, 'publish')
    # @patch.object(Client, 'containers',
    #               Mock(return_value=docker_fixture))
    # def test_should_work_with_real_data(self, publish_mock):
    #     self.collector.collect()

    #     self.assertPublishedMany(publish_mock, {
    #         'lxc.testcontainer.cache': 1,
    #         'lxc.testcontainer.rss': 1,
    #         'lxc.testcontainer.swap': 1,
    #         'lxc.cache': 1,
    #         'lxc.rss': 1,
    #         'lxc.swap': 1,
    #         'system.cache': 1,
    #         'system.rss': 1,
    #         'system.swap': 1,
    #         'docker.testcontainer.cache': 1,
    #         'docker.testcontainer.rss': 1,
    #         'docker.testcontainer.swap': 1,
    #         'docker.cache': 1,
    #         'docker.rss': 1,
    #         'docker.swap': 1,
    #     })

if __name__ == "__main__":
    unittest.main()
