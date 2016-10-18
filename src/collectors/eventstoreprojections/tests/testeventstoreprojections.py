#!/usr/bin/python
# coding=utf-8
##########################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import call, patch

from diamond.collector import Collector

from eventstoreprojections import EventstoreProjectionsCollector

##########################################################################


class TestEventstoreProjectionsCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('EventstoreProjectionsCollector', {})
        self.collector = EventstoreProjectionsCollector(config, None)

    def test_import(self):
        self.assertTrue(EventstoreProjectionsCollector)

    @patch('urllib2.urlopen')
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock, urlopen_mock):
        returns = [self.getFixture('projections')]
        urlopen_mock.side_effect = lambda *args: returns.pop(0)

        self.collector.collect()

        metrics = {
            'projections.all-reports.eventsProcessedAfterRestart': 88,
            'projections.all-reports.bufferedEvents': 0,
            'projections.all-reports.coreProcessingTime': 46,
            'projections.all-reports.epoch': -1,
            'projections.all-reports.version': 1,
            'projections.all-reports.progress': 100.0,
            'projections.all-reports.status': 1,
            'projections.all-reports.writePendingEventsBeforeCheckpoint': 0,
            'projections.all-reports.partitionsCached': 1,
            'projections.all-reports.writesInProgress': 0,
            'projections.all-reports.readsInProgress': 0,
            'projections.all-reports.writePendingEventsAfterCheckpoint': 0,

            'projections._by_event_type.eventsProcessedAfterRestart': 0,
            'projections._by_event_type.bufferedEvents': 0,
            'projections._by_event_type.coreProcessingTime': 0,
            'projections._by_event_type.epoch': -1,
            'projections._by_event_type.version': 0,
            'projections._by_event_type.progress': -1.0,
            'projections._by_event_type.status': 0,
            'projections._by_event_type.writePendingEventsBeforeCheckpoint': 0,
            'projections._by_event_type.partitionsCached': 1,
            'projections._by_event_type.writesInProgress': 0,
            'projections._by_event_type.readsInProgress': 0,
            'projections._by_event_type.writePendingEventsAfterCheckpoint': 0,

            'projections._by_category.eventsProcessedAfterRestart': 886,
            'projections._by_category.bufferedEvents': 0,
            'projections._by_category.coreProcessingTime': 10,
            'projections._by_category.epoch': -1,
            'projections._by_category.version': 1,
            'projections._by_category.progress': 100.0,
            'projections._by_category.status': 1,
            'projections._by_category.writePendingEventsBeforeCheckpoint': 0,
            'projections._by_category.partitionsCached': 1,
            'projections._by_category.writesInProgress': 0,
            'projections._by_category.readsInProgress': 0,
            'projections._by_category.writePendingEventsAfterCheckpoint': 0,

            'projections._stream_by_cat.eventsProcessedAfterRestart': 0,
            'projections._stream_by_cat.bufferedEvents': 0,
            'projections._stream_by_cat.coreProcessingTime': 0,
            'projections._stream_by_cat.epoch': -1,
            'projections._stream_by_cat.version': 0,
            'projections._stream_by_cat.progress': -1.0,
            'projections._stream_by_cat.status': 0,
            'projections._stream_by_cat.writePendingEventsBeforeCheckpoint': 0,
            'projections._stream_by_cat.partitionsCached': 1,
            'projections._stream_by_cat.writesInProgress': 0,
            'projections._stream_by_cat.readsInProgress': 0,
            'projections._stream_by_cat.writePendingEventsAfterCheckpoint': 0,

            'projections._streams.eventsProcessedAfterRestart': 0,
            'projections._streams.bufferedEvents': 0,
            'projections._streams.coreProcessingTime': 0,
            'projections._streams.epoch': -1,
            'projections._streams.version': 0,
            'projections._streams.progress': -1.0,
            'projections._streams.status': 0,
            'projections._streams.writePendingEventsBeforeCheckpoint': 0,
            'projections._streams.partitionsCached': 1,
            'projections._streams.writesInProgress': 0,
            'projections._streams.readsInProgress': 0,
            'projections._streams.writePendingEventsAfterCheckpoint': 0,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics)

        self.assertPublishedMany(publish_mock, metrics)


##########################################################################
if __name__ == "__main__":
    unittest.main()
