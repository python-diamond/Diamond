#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import MagicMock, Mock, mock_open
from mock import patch

from diamond.collector import Collector

from mesos_cgroup import MesosCGroupCollector

##########################################################################


class TestMesosCGroupCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('MesosCGroupCollector', {})

        self.collector = MesosCGroupCollector(config, None)

    def test_import(self):
        self.assertTrue(MesosCGroupCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):

        task_id = 'b0d5971e-915c-414b-aa25-0da46e64ff4e'

        def urlopen_se(url):
            if url == 'http://localhost:5051/state.json':
                return self.getFixture('state.json')
            else:
                print url
                raise NotImplementedError()

        def listdir_se(directory):
            cgroup_directories = [
                '/sys/fs/cgroup/cpuacct/mesos',
                '/sys/fs/cgroup/cpu/mesos',
                '/sys/fs/cgroup/memory/mesos'
            ]

            if directory in cgroup_directories:
                return ["b0d5971e-915c-414b-aa25-0da46e64ff4e"]
            else:
                print directory
                raise NotImplementedError()

        def isdir_se(directory):
            task_directories = [
                '/sys/fs/cgroup/cpuacct/mesos/%s' % task_id,
                '/sys/fs/cgroup/cpu/mesos/%s' % task_id,
                '/sys/fs/cgroup/memory/mesos/%s' % task_id
            ]

            if directory in task_directories:
                return True
            else:
                print directory
                raise NotImplementedError()

        def open_se(path, mode='r', create=True):
            if path.endswith('cpuacct/mesos/%s/cpuacct.usage' % task_id):
                fixture = self.getFixture('cpuacct.usage')
                m = mock_open(read_data=fixture.getvalue())
                m.__enter__.return_value = fixture
                return m
            elif path.endswith('cpuacct/mesos/%s/cpuacct.stat' % task_id):
                fixture = self.getFixture('cpuacct.stat')
                m = mock_open(read_data=fixture.getvalue())
                m.__enter__.return_value = fixture
                return m
            elif path.endswith('cpu/mesos/%s/cpu.stat' % task_id):
                fixture = self.getFixture('cpu.stat')
                m = mock_open(read_data=fixture.getvalue())
                m.__enter__.return_value = fixture
                return m
            elif path.endswith('memory/mesos/%s/memory.stat' % task_id):
                fixture = self.getFixture('memory.stat')
                m = mock_open(read_data=fixture.getvalue())
                m.__enter__.return_value = fixture
                return m
            else:
                patch_open.stop()
                o = open(path, mode, create)
                patch_open.start()
                return o

        patch_urlopen = patch('urllib2.urlopen', Mock(side_effect=urlopen_se))
        patch_listdir = patch('os.listdir', Mock(side_effect=listdir_se))
        patch_isdir = patch('os.path.isdir', Mock(side_effect=isdir_se))
        patch_open = patch('__builtin__.open', MagicMock(spec=file,
                                                         side_effect=open_se))

        patch_urlopen.start()
        patch_listdir.start()
        patch_isdir.start()
        patch_open.start()
        self.collector.collect()
        patch_open.stop()
        patch_isdir.stop()
        patch_listdir.stop()
        patch_urlopen.stop()

        metrics = self.get_metrics()
        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

        self.assertPublishedMany(publish_mock, metrics)

    def get_metrics(self):
        return {
            'ENVIRONMENT.ROLE.TASK.0.cpuacct.usage': '170379797227518',
            'ENVIRONMENT.ROLE.TASK.0.cpuacct.user': '9333852',
            'ENVIRONMENT.ROLE.TASK.0.cpuacct.system': '2774846',
            'ENVIRONMENT.ROLE.TASK.0.cpu.nr_periods': '26848849',
            'ENVIRONMENT.ROLE.TASK.0.cpu.nr_throttled': '85144',
            'ENVIRONMENT.ROLE.TASK.0.cpu.throttled_time': '34709931864651',
            'ENVIRONMENT.ROLE.TASK.0.memory.cache': '233398272',
            'ENVIRONMENT.ROLE.TASK.0.memory.rss': '1789911040',
            'ENVIRONMENT.ROLE.TASK.0.memory.rss_huge': '1642070016',
            'ENVIRONMENT.ROLE.TASK.0.memory.mapped_file': '1118208',
            'ENVIRONMENT.ROLE.TASK.0.memory.writeback': '0',
            'ENVIRONMENT.ROLE.TASK.0.memory.pgpgin': '375953210',
            'ENVIRONMENT.ROLE.TASK.0.memory.pgpgout': '385688436',
            'ENVIRONMENT.ROLE.TASK.0.memory.pgfault': '353980394',
            'ENVIRONMENT.ROLE.TASK.0.memory.pgmajfault': '157',
            'ENVIRONMENT.ROLE.TASK.0.memory.inactive_anon': '0',
            'ENVIRONMENT.ROLE.TASK.0.memory.active_anon': '1789911040',
            'ENVIRONMENT.ROLE.TASK.0.memory.inactive_file': '52654080',
            'ENVIRONMENT.ROLE.TASK.0.memory.active_file': '180727808',
            'ENVIRONMENT.ROLE.TASK.0.memory.unevictable': '0',
            'ENVIRONMENT.ROLE.TASK.0.memory.hierarchical_memory_limit': '3355443200',  # noqa
            'ENVIRONMENT.ROLE.TASK.0.memory.total_cache': '233398272',
            'ENVIRONMENT.ROLE.TASK.0.memory.total_rss': '1789911040',
            'ENVIRONMENT.ROLE.TASK.0.memory.total_rss_huge': '1642070016',
            'ENVIRONMENT.ROLE.TASK.0.memory.total_mapped_file': '1118208',
            'ENVIRONMENT.ROLE.TASK.0.memory.total_writeback': '0',
            'ENVIRONMENT.ROLE.TASK.0.memory.total_pgpgin': '375953210',
            'ENVIRONMENT.ROLE.TASK.0.memory.total_pgpgout': '385688436',
            'ENVIRONMENT.ROLE.TASK.0.memory.total_pgfault': '353980394',
            'ENVIRONMENT.ROLE.TASK.0.memory.total_pgmajfault': '157',
            'ENVIRONMENT.ROLE.TASK.0.memory.total_inactive_anon': '0',
            'ENVIRONMENT.ROLE.TASK.0.memory.total_active_anon': '1789911040',
            'ENVIRONMENT.ROLE.TASK.0.memory.total_inactive_file': '52654080',
            'ENVIRONMENT.ROLE.TASK.0.memory.total_active_file': '180727808',
            'ENVIRONMENT.ROLE.TASK.0.memory.total_unevictable': '0'
        }

##########################################################################
if __name__ == "__main__":
    unittest.main()
