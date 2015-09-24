# coding=utf-8

"""
Collect numeric value of a field from loggly search results.

This collector will retrieve the values of a configured field from loggly API
and publish each one on the log's specified timestamp.

The collector will limit the query to a timeframe equal to the collector's
duration back from now.

#### Dependencies

    * requests
    * futures

Example config file LogglyCollector.conf

```
enabled = true
interval = 60
subdomain = example
username = loggly_user
password = loggly_pass

[ metric ]
[[ test.metric ]]
field = some.field
query = tag:some_tag AND some_text_field='VALUE'
```

"""

import diamond.collector as collector
import concurrent.futures
import configobj
import datetime
import requests
import time
import os

from math import ceil, log10
from diamond.metric import Metric
from diamond.error import DiamondException


def multi_getvalue(obj, attr, **kw):
    """Retrieve nested attributes."""
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = obj[i]
            if callable(obj):
                obj = obj()
        except KeyError:
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
            'id': "Metric identifier",
            'field': "Name of the field to retrieve, required",
            'count': "Whether to retrieve the count of matching events",
            'timestamp_field': "Name of the timestamp field."
                               "Defaults to 'timestamp'",
            'timestamp_format': "Timestamp format as for strptime or 'int'"
                                "for unix time. Defaults to 'int'",
            'subdomain': "Loggly subdomain to retrieve results from",
            'query': "Loggly search query",
            'username': "Loggly username",
            'password': "Loggly password"
        })
        return config_help

    def get_default_config(self):
        """Return the default collector settings."""
        config = super(LogglyCollector, self).get_default_config()
        config.update({
            'timestamp_field': 'timestamp',
            'timestamp_format': 'int',
            'count': False,
            'query': '*'
        })
        return config

    def process_config(self):
        """Prepare metrics' configuration."""
        def pull_metric_defaults(config):
            [config.update({key: self.config[key]}) for key in
                ['timestamp_field', 'timestamp_format', 'count', 'query']
                if key not in config.keys()]

        super(LogglyCollector, self).process_config()

        if not all((item in self.config.keys()
                    for item in ['subdomain', 'username', 'password'])):
            raise DiamondException(
                'All of subdomain, username and password must be specified '
                'in file %s' % self.configfile)

        for metric, config in self.config['metric'].items():
            if 'field' not in config.keys():
                raise DiamondException(
                    'field must be specified for the metric %s in file %s' %
                    (metric, self.configfile))

            pull_metric_defaults(config)
            config.update({
                'search_URI': 'https://{subdomain}.loggly.com'
                              '/apiv2/search?q={query}&from='
                              '-{interval}s&until=now'.format(
                                  subdomain=self.config['subdomain'],
                                  interval=self.config['interval'],
                                  query=config['query']),
                'events_URI': 'https://{subdomain}.loggly.com'
                              '/apiv2/events?rsid=%s'.format(
                                  subdomain=self.config['subdomain'])})

    def collect(self):
        """Collect metrics from loggly."""
        def parse_timestamp(metric_config, timestamp):
            if metric_config['timestamp_format'] is 'int':
                return datetime.datetime.fromtimestamp(
                    timestamp / 10**(ceil(log10(timestamp)) - 10))
            else:
                return datetime.datetime.strptime(
                    timestamp, metric_config['timestamp_format'])

        def retrieve_results(metric_config):
            def now_as_timefield():
                if metric_config['timestamp_format'] is 'int':
                    return time.mktime(datetime.datetime.now().timetuple())
                else:
                    return datetime.datetime.now().strftime(
                        metric_config['timestamp_format'])

            # see Loggly API documentation Response Codes at:
            # https://www.loggly.com/docs/api-overview/
            known_errors = {
                400: 'Bad Request',
                401: 'Unauthorized',
                403: 'Forbidden',
                404: 'Not Found',
                409: 'Duplicate',
                410: 'Gone',
                500: 'Internal Server Error',
                501: 'Not Implemented',
                503: 'Throttled',
                504: 'Gateway Timeout'
            }

            bare_metrics = []
            search_response = requests.get(
                metric_config['search_URI'],
                auth=(self.config['username'], self.config['password']))
            if search_response.status_code is 200:
                events = requests.get(
                    metric_config['events_URI'] % search_response
                    .json()['rsid']['id'],
                    auth=(self.config['username'], self.config['password']))

                if events.status_code is 200:
                    bare_metrics = [(metric_config['field'],
                                     event[metric_config['timestamp_field']],
                                     multi_getvalue(event['event'],
                                                    metric_config['field']))
                                    for event in events.json()['events']]
                    if metric_config['count']:
                        bare_metrics.append(('count', now_as_timefield(),
                                            events.json()['total_events']))
                else:
                    if events.status_code in known_errors.keys():
                        self.log.error('Loggly returned error %s: %s'
                                       % (events.status_code,
                                          known_errors[events.status_code]))
                    else:
                        self.log.error('HTTP request returned unrecognized '
                                       'error code %s' % events.status_code)
            else:
                if search_response.status_code in known_errors.keys():
                    self.log.error('Loggly returned error %s: %s'
                                   % (search_response.status_code,
                                      known_errors[search_response
                                                   .status_code]))
                else:
                    self.log.error('HTTP request returned unrecognized '
                                   'error code %s' % search_response
                                   .status_code)

            return map(lambda bm: {
                'field': bm[0],
                'timestamp': parse_timestamp(metric_config, bm[1]),
                'value': float(bm[2])}, bare_metrics)

        def parallel_retrieval(results, metric, config):
            results[metric] = {'results': retrieve_results(config)}

        results = {}
        with concurrent.futures.ThreadPoolExecutor(
                len(self.config['metric'].items())) as executor:
            futures = [executor.submit(
                parallel_retrieval, results, metric, config)
                for metric, config in self.config['metric'].items()]
            concurrent.futures.wait(futures)

        for metric, results in results.items():
            for result in results['results']:
                self.publish('.'.join([metric, result['field']]),
                             result['value'],
                             timestamp=time.mktime(
                             result['timestamp'].timetuple()))

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
            metric = Metric(path, value, raw_value=raw_value,
                            timestamp=timestamp, precision=precision,
                            host=self.get_hostname(), metric_type=metric_type,
                            ttl=ttl)
        except DiamondException:
            self.log.error(('Error when creating new Metric: path=%r, '
                            'value=%r'), path, value)
            raise

        # Publish Metric
        self.publish_metric(metric)
