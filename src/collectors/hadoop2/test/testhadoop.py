#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch

from diamond.collector import Collector
from hadoop import HadoopMetrics2Collector

from multiprocessing import Process
import os
import tempfile


##########################################################################


class TestHadoopMetrics2Collector(CollectorTestCase):

    def test_import(self):
        self.assertTrue(HadoopMetrics2Collector)

    @patch.object(Collector, 'publish_metric')
    def test_should_work_with_real_data(self, publish_mock):
        # Create collector configured on metric fixtures; then run the collector
        config = get_collector_config('HadoopMetrics2Collector', {
            'metric_files':  [os.path.dirname(__file__) + '/fixtures/*metrics.log'],
        })
        collector = HadoopMetrics2Collector(config, {})
        collector.collect()

        # Check that the expected metrics were published
        expected_metrics = self.getPickledResults('expected.pkl')
        self.assertPublishedMetricMany(publish_mock, expected_metrics)

        # Check the docs are set correctly
        self.setDocExample(collector=collector.__class__.__name__,
                           metrics=expected_metrics,
                           defaultpath='hadoop2')

    def test_file_truncate(self):
        original_text = "123 foo: Hostname=bar, data=1"
        expected_metrics = ('data', 1.0, 'hadoop.foo.data', 'bar', '123')
        new_text = "this should not be truncated"

        # Create a temporary file with metrics to report
        with tempfile.NamedTemporaryFile('w', delete=False) as temporary_file:
            temp_filename = temporary_file.name
            temporary_file.write(original_text)

        # Create hadoop2 collector on the temporary file; then run the collector
        config = get_collector_config('TruncateTestingCollector', {
            'metric_files':  [temp_filename],
            'truncate':  True
        })
        collector = TruncateTestingCollector(config, new_text, expected_metrics)
        collector.collect()

        # Assert that the temporary file is still there and has
        # expected content; then cleanup by removing the file
        self.assertTrue(os.path.isfile(temp_filename))
        self.assertEqual(open(temp_filename, 'r').read(), new_text)
        os.remove(temp_filename)


class TruncateTestingCollector(HadoopMetrics2Collector):

    def __init__(self, config, append_text, expected_args):
        self.append_text = append_text
        self.expected_args = expected_args
        super(TruncateTestingCollector, self).__init__(config, {})

    def _publish(self, *args, **kwargs):
        assert len(self.config['metric_files']) == 1
        assert args == self.expected_args
        temp_filename = self.config['metric_files'][0]
        p = Process(target=self._child_writer, args=(temp_filename,))
        p.start()
        p.join()
        super(TruncateTestingCollector, self)._publish(*args)

    def _child_writer(self, temp_filename):
        with open(temp_filename, 'a') as f:
            f.write(self.append_text)


##########################################################################
if __name__ == "__main__":
    unittest.main()
