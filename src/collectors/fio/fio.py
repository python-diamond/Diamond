# coding=utf-8

"""
The FioCollector collects results from fio runs

#### Dependencies

 * fio

"""

try:
    import json
except ImportError:
    import simplejson as json

import re
import subprocess

import diamond.collector


def flatten_dictionary(input, sep='.', prefix=None):
    """Produces iterator of pairs where the first value is
    the joined key names and the second value is the value
    associated with the lowest level key. For example::

      {'a': {'b': 10},
       'c': 20,
       }

    produces::

      [('a.b', 10), ('c', 20)]
    """

    for key, value in sorted(input.items()):
        if isinstance(value, dict):
            for subkey, subvalue in flatten_dictionary(value):
                yield key + "." + subkey, subvalue
        else:
                yield key, value


class FioCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(FioCollector, self).get_default_config_help()
        config_help.update({
            'ioengine': 'default: libaio',
            'iodepth': 'default: 4',
            'rw': 'default: readwrite',
            'bs': 'default: 32k',
            'direct': 'default: 0',
            'size': 'default: 100M',
            'directory': 'default: /tmp'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """

        config = super(FioCollector, self).get_default_config()
        config.update({
            'ioengine': 'libaio',
            'iodepth': '1',
            'rw': 'readwrite',
            'bs': '32k',
            'direct': '0',
            'size': '100M',
            'directory': '/tmp',
        })
        return config

    def _get_stats_from_fio(self):
        """Return the parsed JSON fio output
        """

        try:
            json_blob = subprocess.check_output(
                ['/usr/bin/fio',
                 '--name=fio',
                 '--ioengine=' + self.config['ioengine'],
                 '--iodepth=' + self.config['iodepth'],
                 '--rw=' + self.config['rw'],
                 '--bs=' + self.config['bs'],
                 '--direct=' + self.config['direct'],
                 '--size=' + self.config['size'],
                 '--numjobs=1',
                 '--directory=' + self.config['directory'],
                 '--output-format=json',
                 ])
        except subprocess.CalledProcessError, err:
            self.log.exception('Could not get fio output: %s', err)
            return {}

        try:
            json_data = json.loads(json_blob)
        except Exception, err:
            self.log.exception('Could not parse fio output %s', err)
            return {}

        # only return first job, no support for multiple jobs yet
        return json_data['jobs'][0]

    def _publish_stats(self, stats):
        """ Publish stats """
        for stat_name, stat_value in flatten_dictionary(
            stats,
            prefix='fio',
        ):
            if not stat_value.isdigit():
                continue
            self.publish_gauge(stat_name, stat_value)

    def collect(self):
        """ Collect stats """
        stats = self._get_stats_from_fio()
        self._publish_stats(stats)
        return
