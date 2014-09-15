# coding=utf-8

"""
Collecting connections tracking statistics from nf_conntrack/ip_conntrack
kernel module.

#### Dependencies

 * nf_conntrack/ip_conntrack kernel module

"""

import diamond.collector
import os


class ConnTrackCollector(diamond.collector.Collector):
    """
    Collector of number of conntrack connections
    """

    def get_default_config_help(self):
        """
        Return help text for collector configuration
        """
        config_help = super(ConnTrackCollector, self).get_default_config_help()
        config_help.update({
            "dir":      "Directories with files of interest, comma seperated",
            "files":    "List of files to collect statistics from",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ConnTrackCollector, self).get_default_config()
        config.update({
            "path":  "conntrack",
            "dir":   "/proc/sys/net/ipv4/netfilter,/proc/sys/net/netfilter",
            "files": "ip_conntrack_count,ip_conntrack_max,"
                     "nf_conntrack_count,nf_conntrack_max",
        })
        return config

    def collect(self):
        """
        Collect metrics
        """
        collected = {}
        files = []

        if isinstance(self.config['dir'], basestring):
            dirs = [d.strip() for d in self.config['dir'].split(',')]
        elif isinstance(self.config['dir'], list):
            dirs = self.config['dir']

        if isinstance(self.config['files'], basestring):
            files = [f.strip() for f in self.config['files'].split(',')]
        elif isinstance(self.config['files'], list):
            files = self.config['files']

        for sdir in dirs:
            for sfile in files:
                if sfile.endswith('conntrack_count'):
                    metric_name = 'ip_conntrack_count'
                elif sfile.endswith('conntrack_max'):
                    metric_name = 'ip_conntrack_max'
                else:
                    self.log.error('Unknown file for collection: %s', sfile)
                    continue
                fpath = os.path.join(sdir, sfile)
                if not os.path.exists(fpath):
                    continue
                try:
                    with open(fpath, "r") as fhandle:
                        metric = float(fhandle.readline().rstrip("\n"))
                        collected[metric_name] = metric
                except Exception as exception:
                    self.log.error("Failed to collect from '%s': %s",
                                   fpath,
                                   exception)
        if not collected:
            self.log.error('No metric was collected, looks like '
                           'nf_conntrack/ip_conntrack kernel module was '
                           'not loaded')
        else:
            for key in collected.keys():
                self.publish(key, collected[key])
