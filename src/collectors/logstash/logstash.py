# coding=utf-8

"""
Collect the logstash stats for the local node

#### Dependencies

 * urlib2
 * json

"""

import urllib2

try:
    import json
    json  # workaround for pyflakes issue #13
except ImportError:
    import simplejson as json

import diamond.collector


class LogstashCollector(diamond.collector.Collector):

    metrics = {}

    def get_default_config_help(self):
        config_help = super(LogstashCollector,
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
        config = super(LogstashCollector, self).get_default_config()
        config.update({
            'host': '127.0.0.1',
            'port': 9600,
        })
        return config

    def _get(self, path, expect_json=True):
        url = 'http://%s:%i/%s' % (
            self.config['host'], int(self.config['port']), path)
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, err:
            self.log.error("%s: %s", url, err)
            return False

        if not expect_json:
            return response.read()

        try:
            return json.load(response)
        except (TypeError, ValueError):
            self.log.error("Unable to parse response from elasticsearch as a"
                           + " json object")
            return False

    def _parse_stats(self, data, prefix=None):
        for key, value in data.iteritems():
            if type(value) == dict:
                name = '.'.join([prefix, key]) if prefix else key
                self._parse_stats(value, name)
            elif type(value) in [int, float, long]:
                name = '.'.join([prefix, key.replace('.', '_')]) if prefix else key.replace('.', '_')
                self.metrics[name] = value
            else:
                self.log.debug('Type %s not handled for %s', type(value), key)

    def collect(self):
        if json is None:
            self.log.error('Unable to import json')
            return {}

        result = self._get('_node/stats')
        if not result:
            self.log.error('Could not load node stats')
            return

        subtrees_to_collect = ['jvm', 'process', 'pipeline']
        result = {k:v for k,v in result.iteritems() if any(k == x for x in subtrees_to_collect)}

        # convert pipeline.plugins array into hash
        plugins_hash = {}
        for plugin_type,plugins_array in result['pipeline']['plugins'].iteritems():
            plugins_hash[plugin_type] = {}
            for plugin in plugins_array:
                if 'events' in plugin:
                    plugins_hash[plugin_type].update({ plugin['id']: plugin['events'] })

        # keep only events and plugins subtrees in resulting pipeline hash
        result['pipeline'] = {
            'events': result['pipeline']['events'],
            'plugins': plugins_hash,
        }

        self._parse_stats(result)

        for key in self.metrics:
            self.log.debug('%s: %s', key, self.metrics[key])
            if key in self.metrics:
                self.publish(key, self.metrics[key])
