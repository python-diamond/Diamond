# coding=utf-8

"""
Simple collector which get JSON and parse it into flat metrics

#### Dependencies

 * urllib2

"""

import urllib2
import json
import diamond.collector


class JSONCommonCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(JSONCommonCollector, self).get_default_config_help()
        config_help.update({
            'url': 'Full URL'
        })
        return config_help

    def get_default_config(self):
        default_config = super(JSONCommonCollector, self).get_default_config()
        default_config['url'] = 'http://localhost/stat'
        return default_config

    def _json_to_flat_metrics(self, prefix, data):
        for key, value in data.items():
            if isinstance(value, dict):
                for k, v in self._json_to_flat_metrics("%s.%s" % (prefix, key), value):
                    yield k, v
            else:
                try:
                    int(value)
                except ValueError:
                    value = None
                finally:
                    yield ("%s.%s" % (prefix, key), value)

    def collect(self):
        url = self.config['url']

        req = urllib2.Request(url)
        req.add_header('Content-type', 'application/json')

        try:
            resp = urllib2.urlopen(req)
        except urllib2.URLError as e:
            self.log.error("Can't open url ", e)
        else:

            content = resp.read()

            try:
                data = json.loads(content)
            except ValueError as e:
                self.log.error("Can't parse JSON object from %s" % url, e)
            else:
                for metric_name, metric_value in self._json_to_flat_metrics("", data):
                    self.publish(metric_name, metric_value)
