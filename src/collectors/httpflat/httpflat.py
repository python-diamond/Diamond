# coding=utf-8

"""
Simple collector which get FLAT files and parse it into flat metrics

#### Dependencies

 * urllib2

"""

import urllib2
import diamond.collector


class HTTPFLATCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(HTTPFLATCollector, self).get_default_config_help()
        config_help.update({
            'url': 'Full URL'
        })
        return config_help

    def get_default_config(self):
        default_config = super(HTTPFLATCollector, self).get_default_config()
        default_config.update({
            'path': 'httpflat',
            'url': 'http://localhost/stat'
        })
        return default_config

    def _flat_to_flat_metrics(self, prefix, data):
        i = 1
        data = dict(line.split("=") for line in data.split("\n"))
        for key in data:
            yield key, data[key]

    def collect(self):
        url = self.config['url']

        req = urllib2.Request(url)
        req.add_header('Content-type', 'application/text')

        try:
            resp = urllib2.urlopen(req)
        except urllib2.URLError as e:
            self.log.error("Can't open url %s. %s", url, e)
        else:

            content = resp.read()

            try:
                data = content
            except ValueError as e:
                self.log.error("Can't parse JSON object from %s. %s", url, e)
            else:
                for metric_name, metric_value in self._flat_to_flat_metrics(
                        "", data):
                    self.publish('voip.rtstatng.' + metric_name, metric_value)
