import json

from test import CollectorTestCase
from test import get_collector_config

from mock import Mock, patch

from scribe import ScribeCollector


class ScribeCollectorTestCase(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('ScribeCollector', {})
        self.collector = ScribeCollector(config, None)

    def test_import(self):
        self.assertTrue(ScribeCollector)

    def test_key_to_metric(self):
        fn = self.collector.key_to_metric
        self.assertEqual(fn("foo! bar!"), "foo__bar_")
        self.assertEqual(fn(" foo:BAR"), "_foo_BAR")
        self.assertEqual(fn("the_same"), "the_same")

    def test_get_scribe_stats(self):
        scribe_ctrl_output = self.getFixture('scribe_ctrl').getvalue()
        expected_scribe_stats = json.loads(self.getFixture(
                                           'scribe_ctrl_stats.json')
                                           .getvalue())

        with patch.object(ScribeCollector, 'get_scribe_ctrl_output',
                          Mock(return_value=scribe_ctrl_output)):
            scribe_stats = self.collector.get_scribe_stats()

        self.assertEqual(dict(scribe_stats), expected_scribe_stats)
