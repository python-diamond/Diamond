# coding=utf-8

"""
Collect icmp round trip times
Only valid for ipv4 hosts currently

#### Dependencies

 * ping

#### Configuration

Configuration is done by:

Create a file named: PingCollector.conf in the collectors_config_path

 * enabled = true
 * interval = 60
 * target = example.org
 * extended = true
 * count = 10

The extended and count are optional. If enabled extended will show
min/max/avg/mdev for the results. Count will do more then a single
ping to get those results.

Test your configuration using the following command:

diamond-setup --print -C PingCollector

You should get a response back that indicates 'enabled': True and see entries
for your targets in pairs like:

'target': 'example.org'

If you want multiple ping tests to be done name the configs like
   - PingCollector google.conf
   - PingCollector yahoo.conf

A space in the config name will tell Diamond v4+ to run the collector multiple
times

"""

import diamond.collector
from diamond.collector import str_to_bool

import re
import os
import subprocess


class PingCollector(diamond.collector.ProcessCollector):

    def get_default_config_help(self):
        config_help = super(PingCollector, self).get_default_config_help()
        config_help.update({
            'bin': 'The path to the ping binary',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(PingCollector, self).get_default_config()
        config.update({
            'path': 'ping',
            'bin': '/bin/ping',
            'extended': 'false',
            'count': '20',
        })
        return config

    def collect(self):
        extended = str_to_bool(self.config['extended'])

        #
        # dump things into a dict to keep
        # backward compatability with the
        # old way of using the check
        targets = {}
        try:
            targets[self.config['target']] = self.config['target']
        except:
            targets = dict(filter(lambda item: item[0].startswith('target_'),
                                  self.config.iteritems()))

        if extended:
            count = int(self.config['count'])
        else:
            count = 1

        for metric, host in targets.items():
            ping = self.run_command(['-nq', '-c %i' % count, host])
            ping = ping[0].strip().split("\n")[-1]

            #
            # set the metric name
            metric = host.replace('.', '_')

            try:
                regstr = ('(?P<min>\d+.\d+)\/(?P<avg>\d+.\d+)\/'
                          '(?P<max>\d+.\d+)\/(?P<mdev>\d+.\d+)')

                regex = re.compile(regstr)
                vals = regex.search(ping).groupdict()
            except:
                #
                # something failed so log it and return
                self.log.info("Failed to parse the ping output results")

                vals = {
                    'min': 0,
                    'max': 0,
                    'avg': 0,
                    'mdev': 0
                }

            if extended:
                for m, v in vals.items():
                    metric_name = "%s.%s" % (metric, m)

                    #
                    # send to graphite
                    self.publish(metric_name, v, precision=4)
            else:
                self.publish(metric, vals['min'], precision=4)
