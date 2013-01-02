# coding=utf-8

"""
Openstack swift collector.

#### Dependencies

 * swift-dispersion-report commandline tool (for dispersion report)
   if using this, make sure swift.conf and dispersion.conf are reable by diamond
   also get an idea of the runtime of a swift-dispersion-report call and make
   sure the collect interval is high enough to avoid contention.
 * swift commandline tool (for container_metrics)

both of these should come installed with swift
"""

import diamond.collector
from subprocess import Popen, PIPE

try:
    import json
    json  # workaround for pyflakes issue #13
except ImportError:
    import simplejson as json


class OpenstackSwiftCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(OpenstackSwiftCollector,
                            self).get_default_config_help()
        config_help.update({
            'enable_dispersion_report': 'gather swift-dispersion-report metrics'
            + ' (default False)',
            'enable_container_metrics': 'gather containers metrics'
            + '(# objects, bytes used, x_timestamp.  default True)',
            'auth_url': 'authentication url (for enable_container_metrics)',
            'account': 'swift auth account (for enable_container_metrics)',
            'user': 'swift auth user (for enable_container_metrics)',
            'password': 'swift auth password (for enable_container_metrics)',
            'containers': 'containers on which to count number of objects, '
            + 'space separated list (for enable_container_metrics)'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(OpenstackSwiftCollector, self).get_default_config()
        config.update({
            'path': 'openstackswift',
            'enable_dispersion_report': False,
            'enable_container_metrics': True,
            # don't use the threaded model with this one.
            # for some reason it crashes.
            'interval': 1200,  # by default, every 20 minutes
        })
        return config

    def collect(self):
        # dispersion report.  this can take easily >60s. beware!
        if (self.config['enable_dispersion_report']):
            p = Popen(['swift-dispersion-report', '-j'],
                stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
            self.publish('dispersion.errors', len(stderr.split('\n')) - 1)
            data = json.loads(stdout)
            for t in ('object', 'container'):
                for (k, v) in data[t].items():
                    self.publish('dispersion.%s.%s' % (t, k), v)

        # container metrics returned by stat <container>
        if(self.config['enable_container_metrics']):
            account = '%s:%s' % (self.config['account'], self.config['user'])
            for container in self.config['containers'].split(','):
                cmd = ['swift', '-A', self.config['auth_url'],
                       '-U', account,
                       '-K', self.config['password'],
                       'stat', container]
                p = Popen(cmd, stdout=PIPE, stderr=PIPE)
                stdout, stderr = p.communicate()
                stats = {}
                # stdout is some lines in 'key   : val' format
                for line in stdout.split('\n'):
                    if line:
                        line = line.split(':', 2)
                        stats[line[0].strip()] = line[1].strip()
                key = 'container_metrics.%s.%s' % (self.config['account'],
                                                   container)
                self.publish('%s.objects' % key, stats['Objects'])
                self.publish('%s.bytes' % key, stats['Bytes'])
                self.publish('%s.x_timestamp' % key, stats['X-Timestamp'])
