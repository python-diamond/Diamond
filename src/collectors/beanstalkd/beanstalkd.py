# coding=utf-8

"""
Collects the following from beanstalkd:
    - Server statistics via the 'stats' command
    - Per tube statistics via the 'stats-tube' command

#### Dependencies

 * beanstalkc

"""

import re
import diamond.collector

try:
    import beanstalkc
    beanstalkc  # workaround for pyflakes issue #13
except ImportError:
    beanstalkc = None


class BeanstalkdCollector(diamond.collector.Collector):
    COUNTERS_REGEX = re.compile(
        r'^(cmd-.*|job-timeouts|total-jobs|total-connections)$')

    def get_default_config_help(self):
        config_help = super(BeanstalkdCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': 'Hostname',
            'port': 'Port',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(BeanstalkdCollector, self).get_default_config()
        config.update({
            'path':     'beanstalkd',
            'host':     'localhost',
            'port':     11300,
        })
        return config

    def _get_stats(self):
        stats = {}
        try:
            connection = beanstalkc.Connection(self.config['host'],
                                               int(self.config['port']))
        except beanstalkc.BeanstalkcException, e:
            self.log.error("Couldn't connect to beanstalkd: %s", e)
            return {}

        stats['instance'] = connection.stats()
        stats['tubes'] = []

        for tube in connection.tubes():
            tube_stats = connection.stats_tube(tube)
            stats['tubes'].append(tube_stats)

        return stats

    def collect(self):
        if beanstalkc is None:
            self.log.error('Unable to import beanstalkc')
            return {}

        info = self._get_stats()

        for stat, value in info['instance'].items():
            if stat != 'version':
                self.publish(stat, value,
                             metric_type=self.get_metric_type(stat))

        for tube_stats in info['tubes']:
            tube = tube_stats['name']
            for stat, value in tube_stats.items():
                if stat != 'name':
                    self.publish('tubes.%s.%s' % (tube, stat), value,
                                 metric_type=self.get_metric_type(stat))

    def get_metric_type(self, stat):
        if self.COUNTERS_REGEX.match(stat):
            return 'COUNTER'
        return 'GAUGE'
