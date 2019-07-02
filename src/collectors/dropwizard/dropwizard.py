# coding=utf-8

"""
Collect [dropwizard](http://dropwizard.codahale.com/) stats for the local node

"""

import re
import requests

import diamond.collector


"""
Dropwizard returns metrics in the format
    {
      "category": {
        "name": {
          "type": value
          ...
        },
        ...
This dict defines the types in each category we emit.
"""
METRIC_TYPES_TO_EMIT = {
    # only value in this category is the value
    "gauges": [
        "value"
    ],
    # only value in this category is the count
    "counters": [
        "count"
    ],
    # ignores minute rates ("m1_rate", "m5_rate", "m15_rate") and "units"
    "meters": [
        "count", "mean_rate"
    ],
    # ignores all rates ("m1_rate", "m5_rate", "m15_rate", "mean_rate"), units
    # ("duration_units", "rate_units"), "p999", and "stddev"
    "timers": [
        "count", "max", "mean", "min", "p50", "p75", "p95", "p98", "p99"
    ]
}

"""
Blacklist of metrics to ignore. Generally we want all metrics; however some
are just not useful or are not even an integer value. Each entry is a regex
that will be compared against the metric names.
"""
METRIC_NAME_BLACKLIST = {
    "gauges": [
        "io.dropwizard.jetty.MutableServletContextHandler.*", # use metered metrics instead
        "jvm.attribute.name",    # a string
        "jvm.attribute.vendor",  # a string
        "jvm.memory.pools.*",    # 40+ metric values I doubt we need
        "jvm.threads.deadlocks", # returns a dict
    ],
    "counters": [
        "TimeBoundHealthCheck-pool-%d.*"  # useless
    ],
    "meters": [
        "TimeBoundHealthCheck-pool-%d.*"  # useless
    ],
    "timers": [
        "io.dropwizard.jetty.MutableServletContextHandler.trace-requests"  # useless
    ],
}

"""Default URL to request metrics from"""
DEFAULT_METRICS_URL = 'http://127.0.0.1:8081/metrics'


class DropwizardCollector(diamond.collector.Collector):

    def __init__(self, config=None, handlers=[], name=None, configfile=None):
        super(DropwizardCollector, self).__init__(config, handlers,
                                                  name, configfile)
        # construct blacklist regex
        self.blacklist = {name: re.compile('|'.join(black))
                            for name, black in METRIC_NAME_BLACKLIST.items()}


    def get_default_config_help(self):
        config_help = super(DropwizardCollector,
                            self).get_default_config_help()
        config_help.update({
            'url': '',
            'path': ''
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(DropwizardCollector, self).get_default_config()
        config.update({
            'url': DEFAULT_METRICS_URL,
            'path': 'dropwizard'
        })
        return config

    def collect(self):
        try:
            response = requests.get(self.config['url'])
        except requests.exceptions.RequestException as err:
            self.log.error("Dropwizard collector: error requesting from"
                           " %s: %s", url, err)
            return

        if response.status_code != 200:
            self.log.error("Dropwizard collector: received invalid status code"
                           " %d", response.status_code)
            return

        try:
            result_json = response.json()
        except ValueError:
            self.log.error("Dropwizard collector: unable to parse response from"
                           " dropwizard as a json object")
            return

        # construct metrics to emit
        metrics_to_emit = {}

        # loop over each metric category (e.g. gauge, timer, etc.)
        for metric_category, events in result_json.items():
            # ignore categories like "version" and "histogram"
            if metric_category not in METRIC_TYPES_TO_EMIT:
                continue
            # loop over each metric name (e.g. jvm.threads.count, etc.)
            for metrics_name, data in events.items():
                # ignore if the name is in the blacklist for this category
                if self.blacklist[metric_category].match(metrics_name):
                    continue
                # loop over each valid metric type in this category and add
                # the metric to the dict
                for metric_type in METRIC_TYPES_TO_EMIT[metric_category]:
                    metric_key = '{}.{}.{}'.format(metric_category,
                                                   metrics_name,
                                                   metric_type)
                    metrics_to_emit[metric_key] = data[metric_type]

        # emit metrics
        for key, val in metrics_to_emit.items():
            self.publish(key, val)
