# coding=utf-8

"""
Shells out to get the value of sysctl net.netfilter.nf_conntrack_count and
net.netfilter.nf_conntrack_count_max

#### Dependencies

 * nf_conntrack module

"""

import diamond.collector


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
            "dir":         "Directory with files of interest",
            "files":       "List of files to collect statistics from",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ConnTrackCollector, self).get_default_config()
        config.update({
            "path":             "conntrack",
            "dir":              "/proc/sys/net/ipv4/netfilter",
            "files":            "ip_conntrack_count,ip_conntrack_max",
        })
        return config

    def collect(self):
        """
        Collect metrics
        """
        collected = {}
        for sfile in self.config["files"].split(","):
            fpath = "%s/%s" % (self.config["dir"], sfile)
            try:
                with open(fpath, "r") as fhandle:
                    collected[sfile] = float(fhandle.readline().rstrip("\n"))
            except Exception as exception:
                self.log.error("Failed to collect from '%s': %s",
                               fpath,
                               exception)

        for key in collected.keys():
            self.publish(key, collected[key])
