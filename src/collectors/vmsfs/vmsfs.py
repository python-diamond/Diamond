# coding=utf-8

"""
Uses /sys/fs/vmsfs to collect host-global data on VMS memory usage

#### Dependencies

 * /sys/fs/vmsfs <- vmsfs package, vmsfs mounted

"""

import diamond.collector
import os


class VMSFSCollector(diamond.collector.Collector):

    SYSFS = '/sys/fs/vmsfs'

    VMSFS_STATS = {
        'resident': ('cur_resident', 4096),
        'allocated': ('cur_allocated', 4096)
    }

    def vmsfs_stats_read(self, filename):
        stats = {}

        # Open vmsfs sys info.
        stats_fd = None
        try:
            stats_fd = open(filename)

            for line in stats_fd:
                tokens = line.split()
                stats[tokens[0][0:-1]] = long(tokens[1])
        except:
            if stats_fd:
                stats_fd.close()

        return stats

    def vmsfs_stats_dispatch(self, filename, prefix=''):
        stats = self.vmsfs_stats_read(filename)
        for stat in self.VMSFS_STATS:
            name = self.VMSFS_STATS[stat][0]
            scale = self.VMSFS_STATS[stat][1]
            if name in stats:
                self.publish(prefix + name, stats[name] * scale)

    def get_default_config_help(self):
        config_help = super(VMSFSCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(VMSFSCollector, self).get_default_config()
        config.update({
            'path':     'vmsfs'
        })
        return config

    def collect(self):
        if not os.access(self.SYSFS, os.R_OK | os.X_OK):
            return None

        # Dispatch total stats.
        self.vmsfs_stats_dispatch(os.path.join(self.SYSFS, 'stats'))

        # Dispatch per-generation stats.
        # NOTE: We do not currently report the per-generation statistics to
        # diamond. This is because we do not have a good strategy for
        # aggregating generation data and exposing it in a sensible way. There
        # are three strategies:
        #  1) Collect everything at the host level.
        #     The problem here is that the number of metrics will explode for
        #     that individual host (and keep growing).
        #  2) Collect at the top-level (one virtual host per generation).
        #     Then the problem is finding the generation through UI tools, etc.
        #  3) Figure out some way to put the stats in each instance associated
        #     with that generation.
        # We favor (2) currently, but there's not much value in implementing it
        # until it can be exposed to the user.
        if False:
            TO_IGNORE = ('stats', 'version',
                         '00000000-0000-0000-0000-000000000000')
            files = os.listdir(self.SYSFS)
            for f in files:
                if f not in TO_IGNORE:
                    self.vmsfs_stats_dispatch('/sys/fs/vmsfs/' + f,
                                              prefix=('%s.' % f))
