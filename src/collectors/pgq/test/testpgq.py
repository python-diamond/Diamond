#!/usr/bin/python
from test import CollectorTestCase, get_collector_config
from mock import MagicMock, patch

from pgq import PgQCollector


class TestPgQCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('PgQCollector', {})
        self.collector = PgQCollector(config, None)

    def test_import(self):
        self.assertTrue(PgQCollector)

    @patch.object(PgQCollector, 'publish')
    @patch.object(PgQCollector, 'get_consumer_info')
    @patch.object(PgQCollector, 'get_queue_info')
    def test_collect(self, get_queue_info, get_consumer_info, publish):
        get_queue_info.return_value = iter([
            ('q1', {
                'ticker_lag': 1,
                'ev_per_sec': 2,
            }),
            ('q2', {
                'ticker_lag': 3,
                'ev_per_sec': 4,
            }),
        ])

        get_consumer_info.return_value = iter([
            ('q1', 'c1', {
                'lag': 1,
                'pending_events': 2,
                'last_seen': 3,
            }),
            ('q2', 'c1', {
                'lag': 4,
                'pending_events': 5,
                'last_seen': 6,
            }),
        ])

        self.collector._collect_for_instance('db1', connection=MagicMock())

        self.assertPublished(publish, 'db1.q1.ticker_lag', 1)
        self.assertPublished(publish, 'db1.q1.ev_per_sec', 2)
        self.assertPublished(publish, 'db1.q2.ticker_lag', 3)
        self.assertPublished(publish, 'db1.q2.ev_per_sec', 4)

        self.assertPublished(publish, 'db1.q1.consumers.c1.lag', 1)
        self.assertPublished(publish, 'db1.q1.consumers.c1.pending_events', 2)
        self.assertPublished(publish, 'db1.q1.consumers.c1.last_seen', 3)
        self.assertPublished(publish, 'db1.q2.consumers.c1.lag', 4)
        self.assertPublished(publish, 'db1.q2.consumers.c1.pending_events', 5)
        self.assertPublished(publish, 'db1.q2.consumers.c1.last_seen', 6)
