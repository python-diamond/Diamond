# coding=utf-8

"""
Collect numeric value of a field from loggly search results.

This collector will retrieve the values of a configured field from loggly API and publish each one
on the log's specified timestamp.

The collector will limit the query to a timeframe equal to the collector's duration back from now.

#### Dependencies

    * requests
    * futures

"""

import diamond.collector as collector
import concurrent.futures
import configobj
import datetime
import requests
import bunch
import time
import os

from math import ceil, log10
from diamond.metric import Metric
from diamond.error import DiamondException


def multi_getattr(obj, attr, **kw):
    """Retrieve nested attributes."""
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
            if callable(obj):
                obj = obj()
        except AttributeError:
            if 'default' in kw:
                return kw['default']
            else:
                raise
    return obj


class LogglyCollector(collector.Collector):

    """Loggly Collector."""

    def get_default_config_help(self):
        """Update configuration help."""
        config_help = super(
            LogglyCollector, self).get_default_config_help()
        config_help.update({
            'id': 'Metric identifier',
            'field': 'Name of the field to retrieve, mutually exclusive with count',
            'count': 'Whether to retrieve the count of matching events, mutually exclusive with field',
            'timestamp_field': 'Name of the timestamp field. Defaults to \'timestamp\'',
            'timestamp_format': 'Timestamp format as for strptime or \'int\' for unix time. Defaults to \'int\'',
            'subdomain': 'Loggly subdomain to retrieve results from',
            'query': 'Loggly search query',
            'username': 'Loggly username',
            'password': 'Loggly password'
        })
        return config_help

    def process_config(self):
        """Prepare loggly URIs from configuration values."""
        def set_defaults(config):
            defaults = {
                'timestamp_field': 'timestamp',
                'timestamp_format': 'int',
                'field': 'count',
                'count': False,
                'query': '*'
            }
            [config.update({key: value}) for key, value in defaults.items() if key not in config.keys()]

        super(LogglyCollector, self).process_config()

        if 'path' in self.config['metric']:
            config_extension = self.config['metric'].get('extension', '.conf')
            for cfgfile in os.listdir(self.config['metric']['path']):
                cfgfile = os.path.join(self.config['metric']['path'], cfgfile)
                cfgfile = os.path.abspath(cfgfile)
                if not cfgfile.endswith(config_extension):
                    continue
                newconfig = configobj.ConfigObj(cfgfile)
                self.config.merge(newconfig)
        [self.config['metric'].pop(item, None) for item in ['path', 'extension']]

        self.config_bunch = bunch.bunchify(self.config)
        self.metrics_config = self.config_bunch.metric

        for metric, config in self.metrics_config.items():
            if 'field' in config.keys() and config.field is not 'count' and\
                    'count' in config.keys() and not collector.str_to_bool(config.count):
                raise DiamondException(
                    'Both field and count specified for the metric %s in file %s' % (metric, self.configfile))

            if 'field' not in config.keys() and\
                    ('count' not in config.keys() or not collector.str_to_bool(config.count)):
                raise DiamondException(
                    'At least one of field or count must be speficied for the metric %s in file %s' % (
                        metric, self.configfile))

            set_defaults(config)

            config.update({'search_URI': 'https://{0.subdomain}.loggly.com/apiv2/search?'
                                         'q={0.query}&from=-{1.interval}s&until=now'.format(config, self.config_bunch),
                           'events_URI': 'https://{0.subdomain}.loggly.com/apiv2/events?rsid=%s'.format(config)})

    def collect(self):
        """Collect metrics from loggly."""
        def parse_timestamp(metric_config, timestamp):
            if metric_config.timestamp_format is 'int':
                return datetime.datetime.fromtimestamp(timestamp / 10**(ceil(log10(timestamp)) - 10))
            else:
                return datetime.datetime.strptime(timestamp, self.config_bunch.timestamp_format)

        def retrieve_results(metric_config):
            search_response = requests.get(
                metric_config.search_URI,
                auth=(metric_config.username, metric_config.password))
            events = requests.get(
                metric_config.events_URI % search_response.json()['rsid']['id'],
                auth=(metric_config.username, metric_config.password))

            if metric_config.count:
                return [bunch.bunchify({'timestamp': datetime.datetime.now(), 'value': events.json()['total_events']})]
            else:
                bare_metrics = [(event[metric_config.timestamp_field], multi_getattr(bunch.bunchify(event).event,
                                metric_config.field)) for event in events.json()['events']]
                return map(lambda bm: bunch.bunchify({'timestamp': parse_timestamp(metric_config, bm[0]),
                                                      'value': float(bm[1])}),
                           bare_metrics)

        def parallel_retrieval(results, metric, config):
            results.update({metric: bunch.bunchify({'results': retrieve_results(config)})})
            results.get(metric).update(bunch.bunchify({'field': config.field}))

        results = bunch.Bunch()
        with concurrent.futures.ThreadPoolExecutor(len(self.metrics_config.items())) as executor:
            futures = [executor.submit(parallel_retrieval, results, metric, config)
                       for metric, config in self.metrics_config.items()]
            concurrent.futures.wait(futures)

        for metric, results in results.items():
            for result in results.results:
                self.publish('.'.join([metric, results.field]),
                             result.value,
                             timestamp=time.mktime(result.timestamp.timetuple()))

    def publish(self, name, value, timestamp=None, raw_value=None,
                precision=0, metric_type='GAUGE', instance=None):
        """Publish a metric with the given name."""
        # Check whitelist/blacklist
        if self.config['metrics_whitelist']:
            if not self.config['metrics_whitelist'].match(name):
                return
        elif self.config['metrics_blacklist']:
            if self.config['metrics_blacklist'].match(name):
                return

        # Get metric Path
        path = self.get_metric_path(name, instance=instance)

        # Get metric TTL
        ttl = float(self.config['interval']) * float(
            self.config['ttl_multiplier'])

        # Create Metric
        try:
            metric = Metric(path, value, raw_value=raw_value, timestamp=timestamp,
                            precision=precision, host=self.get_hostname(),
                            metric_type=metric_type, ttl=ttl)
        except DiamondException:
            self.log.error(('Error when creating new Metric: path=%r, '
                            'value=%r'), path, value)
            raise

        # Publish Metric
        self.publish_metric(metric)
