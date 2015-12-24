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

import glob
import os
import re
import subprocess

import diamond.collector


def flatten_dict(d):
    def items():
        for key, value in d.items():
            if isinstance(value, dict):
                for subkey, subvalue in flatten_dict(value).items():
                        yield key + "." + subkey, subvalue
            else:
                yield key, value
    return dict(items())


class FioCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(FioCollector, self).get_default_config_help()
        config_help.update({
            'ioengine': 'default: libaio',
            'iodepth': 'default: 4',
            'rw': 'default: write',
            'bs': 'default: 32k',
            'direct': 'default: 0',
            'size': 'default: 1024M',
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
        })
        return config

    def _get_fio_output(self):
        """Return the parsed JSON fio output
        """

        try:
            json_blob = subprocess.check_output(
                ['/usr/bin/fio',
                 '--name=blah',
                 '--ioengine=' + self.config['ioengine'],
                 '--iodepth=' + self.config['iodepth'],
                 '--rw=' + self.config['rw'],
                 '--bs=' + self.config['bs'],
                 '--direct=' + self.config['direct'],
                 '--size=' + self.config['size'],
                 '--numjobs=1',
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

        return json_data

    def _publish_stats(self, stats):
        """Given a stats dictionary from _get_stats_from_socket,
        publish the individual values.
        """

        for job in stats['jobs']:
            job_data = flatten_dict(job)
            for stat in job_data:
                if stat == 'jobname':
                    continue
                stat_name = re.sub('>=', 'gte-', stat)
                self.publish_gauge(stat_name, job_data[stat])

    def collect(self):
        """
        Collect stats
        """
        stats = self._get_fio_output()
        self._publish_stats(stats)
        return
