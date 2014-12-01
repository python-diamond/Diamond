#!/usr/local/rnt/bin/python
# coding=utf-8
"""
This class collects data on NUMA utilization

#### Dependencies

* numactl

"""
import diamond.collector
from subprocess import Popen, PIPE
from re import compile as re_compile
import logging

node_re = re_compile('(?P<node>^node \d+ (free|size)): (?P<size>\d+) \MB')


class NumaCollector(diamond.collector.Collector):

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(NumaCollector, self).get_default_config()
        config.update({
            'path':     'numa',
            'bin':      self.find_binary('numactl'),
        })
        return config

    def collect(self):
        p = Popen([self.config['bin'], '--hardware'], stdout=PIPE, stderr=PIPE)

        output, errors = p.communicate()

        lines = output.split('\n')
        for line in lines:
            try:
                match = node_re.search(line)
                if match:
                    logging.debug("Matched: %s %s" %
                                  (match.group('node'), match.group('size')))
                    metric_name = "%s_MB" % match.group('node').replace(' ',
                                                                        '_')
                    metric_value = int(match.group('size'))
                    logging.debug("Publishing %s %s" %
                                  (metric_name, metric_value))
                    self.publish(metric_name, metric_value)
            except Exception as e:
                logging.error('Failed because: %s' % str(e))
                continue
