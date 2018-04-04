# coding=utf-8

"""
Collect [dropwizard](http://dropwizard.codahale.com/) stats for the local node

"""

import urllib2

try:
    import json
except ImportError:
    import simplejson as json

import diamond.collector


class DropwizardCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(DropwizardCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': "",
            'port': "",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(DropwizardCollector, self).get_default_config()
        config.update({
            'host':     '127.0.0.1',
            'port':     8081,
            'path':     'dropwizard',
        })
        return config

    def send_metric(self, key, value):
        try:
            self.publish(key, value, value, 5)
        except Exception as e:
            self.log.error(e.message)

    def report_timer(self, key, value):
        self.send_metric(key + ".count", value['count'])
        self.send_metric(key + ".max", value['max'])
        self.send_metric(key + ".min", value['min'])
        self.send_metric(key + ".mean", value['mean'])
        self.send_metric(key + ".stddev", value['stddev'])
        self.send_metric(key + ".p50", value['p50'])
        self.send_metric(key + ".p75", value['p75'])
        self.send_metric(key + ".p95", value['p95'])
        self.send_metric(key + ".p98", value['p98'])
        self.send_metric(key + ".p99", value['p99'])
        self.send_metric(key + ".p999", value['p999'])
        self.send_metric(key + ".m1_rate", value['m1_rate'])
        self.send_metric(key + ".m5_rate", value['m5_rate'])
        self.send_metric(key + ".m15_rate", value['m15_rate'])
        self.send_metric(key + ".mean_rate", value['mean_rate'])

    def report_counter(self, key, value):
        self.send_metric(key + ".count", value['count'])

    def report_gauge(self, key, value):
        self.send_metric(key, value['value'])

    def report_histogram(self, key, value):
        self.send_metric(key + ".count", value['count'])
        self.send_metric(key + ".max", value['max'])
        self.send_metric(key + ".min", value['min'])
        self.send_metric(key + ".mean", value['mean'])
        self.send_metric(key + ".stddev", value['stddev'])
        self.send_metric(key + ".p50", value['p50'])
        self.send_metric(key + ".p75", value['p75'])
        self.send_metric(key + ".p95", value['p95'])
        self.send_metric(key + ".p98", value['p98'])
        self.send_metric(key + ".p99", value['p99'])
        self.send_metric(key + ".p999", value['p999'])

    def report_meter(self, key, value):
        self.send_metric(key + ".count", value['count'])
        self.send_metric(key + ".m1_rate", value['m1_rate'])
        self.send_metric(key + ".m5_rate", value['m5_rate'])
        self.send_metric(key + ".m15_rate", value['m15_rate'])
        self.send_metric(key + ".mean_rate", value['mean_rate'])

    def collect(self):
        if json is None:
            self.log.error('Unable to import json')
            return {}
        url = 'http://%s:%i/metrics' % (
            self.config['host'], int(self.config['port']))
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError as err:
            self.log.error("%s: %s", url, err)
            return

        try:
            result = json.load(response)
        except (TypeError, ValueError):
            self.log.error("Unable to parse response from elasticsearch as" +
                           " a json object")
            return

        timers = result['timers']
        histograms = result['histograms']
        counters = result['counters']
        gauges = result['gauges']
        meters = result['meters']

        for key in timers:
            self.report_timer(key, timers[key])

        for key in histograms:
            self.report_histogram(key, histograms[key])

        for key in counters:
            self.report_counter(key, counters[key])

        for key in gauges:
            self.report_gauge(key, gauges[key])

        for key in meters:
            self.report_meter(key, meters[key])
