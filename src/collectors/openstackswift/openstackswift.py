# coding=utf-8

"""
Openstack swift collector.

#### Dependencies

 * swift-dispersion-report commandline tool (for dispersion report)
   if using this, make sure swift.conf and dispersion.conf are reable by diamond
   also get an idea of the runtime of a swift-dispersion-report call and make sure
   the collect interval is high enough to avoid contention.
 * swift commandline tool (for count report)

both of these should come installed with swift
"""

import diamond.collector
from subprocess import Popen, PIPE
import json


class OpenstackSwiftCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(OpenstackSwiftCollector, self).get_default_config_help()
        config_help.update({
            'enable_dispersion_report': 'gather swift-dispersion-report metrics (default False)',
            'enable_counting': 'gather counts of objects in containers (default True)',
            'auth_url': 'authentication url (for enable_counting)',
            'account': 'swift auth account (for enable_counting)',
            'user': 'swift auth user (for enable_counting)',
            'password': 'swift auth password (for enable_counting)',
            'containers': 'containers on which to count number of objects, space separated list (for enable_counting)'
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
            'enable_counting': True,
            # don't use the threaded model with this one.  for some reason it crashes.
            'interval': 1200, # by default, every 20 minutes
        })
        return config

    def collect(self):
        # dispersion report.  this can take easily >60s. beware!
        if (self.config['enable_dispersion_report']):
            p = Popen(['swift-dispersion-report', '-j'], stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
            self.publish('dispersion.errors', len(stderr.split('\n')) - 1)
            data = json.loads(stdout)
            for t in ('object', 'container'):
                for (k,v) in data[t].items():
                    self.publish('dispersion.%s.%s' % (t, k), v)

        # counts of objects in container
        if(self.config['enable_counting']):
            account = '%s:%s' % (self.config['account'], self.config['user'])
            for container in self.config['containers'].split(','):
                cmd = ['swift', '-A', self.config['auth_url'], '-U', account, '-K', self.config['password'], 'list', container]
                p = Popen(cmd, stdout=PIPE, stderr=PIPE)
                stdout, stderr = p.communicate()
                self.publish('counts.%s.%s' % (self.config['account'], container), len(stdout.split('\n')) - 1)
