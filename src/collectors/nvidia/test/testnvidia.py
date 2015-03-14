from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from nvidia import NvidiaCollector
from nvidia import parse_value

################################################################################


class TestNvidiaCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('NvidiaCollector', {
            'interval': 10,
            'bin': 'true',
        })

        self.collector = NvidiaCollector(config, None)

    def test_import(self):
        self.assertTrue(NvidiaCollector)

    def test_get_value(self):
        self.assertFalse(parse_value('test'))
        self.assertFalse(parse_value(''))
        self.assertFalse(parse_value('xa123'))
        self.assertTrue(parse_value('123 MHz') == 123)
        self.assertTrue(parse_value('16x') == 16)
        self.assertTrue(parse_value('99 %') == 99)

    @patch.object(Collector, 'publish')
    def test_counters(self, publish_mock):
        patch_communicate = patch(
            'subprocess.Popen.communicate',
            Mock(
                return_value=(self.getFixture('nvidia-smi.xml').getvalue(), '')
            )
        )
        patch_communicate.start()
        self.collector.collect()
        patch_communicate.stop()

        self.assertPublishedMany(publish_mock, {
            'nvidia-smi.Tesla_M2070.0000:06:00:0.memory_usage.total': 5375,
            'nvidia-smi.Tesla_M2070.0000:06:00:0.memory_usage.used': 66,
            'nvidia-smi.Tesla_M2070.0000:06:00:0.memory_usage.free': 5309,
            'nvidia-smi.Tesla_M2070.0000:06:00:0.utilization.gpu_util': 99,
            'nvidia-smi.Tesla_M2070.0000:06:00:0.utilization.memory_util': 0,
            'nvidia-smi.Tesla_M2070.0000:11:00:0.utilization.gpu_util': 0,
        })


################################################################################
if __name__ == "__main__":
    unittest.main()
