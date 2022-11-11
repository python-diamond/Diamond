# coding=utf-8

"""
A collector for bcache statistics
Based on https://github.com/pommi/collectd-bcache/
"""

import diamond.collector
import os

SYSFS_BCACHE_PATH = '/sys/fs/bcache/'


class BcacheCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(BcacheCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(BcacheCollector, self).get_default_config()
        config.update({
            'path':     'bcache',
        })
        return config

    def file_to_lines(self, fname):
        try:
            with open(fname, "r") as fd:
                return fd.readlines()
        except:
            return []

    def file_to_line(self, fname):
        ret = self.file_to_lines(fname)
        if ret:
            return ret[0].strip()
        return ''

    def bcache_uuids(self):
        uuids = []

        if not os.path.isdir(SYSFS_BCACHE_PATH):
            self.log.error('bcache is not loaded.')
            return uuids

        for cache in os.listdir(SYSFS_BCACHE_PATH):
            if not os.path.isdir('%s%s' % (SYSFS_BCACHE_PATH, cache)):
                continue
            uuids.append(cache)

        return uuids

    def map_uuid_to_bcache(self, uuid):
        devices = []
        for obj in os.listdir(os.path.join(SYSFS_BCACHE_PATH, uuid)):
            if obj.startswith('bdev'):
                devices.append(os.path.basename(os.readlink(
                  os.path.join(SYSFS_BCACHE_PATH, uuid, obj, 'dev'))))
        return devices

    def get_cache_result(self, uuid, stat):
        value = 0
        for obj in os.listdir(os.path.join(SYSFS_BCACHE_PATH, uuid)):
            if obj.startswith('bdev'):
                value = int(self.file_to_line(
                    '%s/%s/%s/stats_five_minute/cache_%s' %
                    (SYSFS_BCACHE_PATH, uuid, obj, stat)))
        return value

    def get_cache_ratio(self, uuid, time):
        for obj in os.listdir(os.path.join(SYSFS_BCACHE_PATH, uuid)):
            if obj.startswith('bdev'):
                hits = float(self.file_to_line(
                    '%s/%s/%s/stats_%s/cache_hits' %
                    (SYSFS_BCACHE_PATH, uuid, obj, time)))
                misses = float(self.file_to_line(
                    '%s/%s/%s/stats_%s/cache_misses' %
                    (SYSFS_BCACHE_PATH, uuid, obj, time)))
                if (hits + misses) == 0:
                    return 100
                return hits / (hits + misses) * 100
        return 0

    def collect(self):
        """
        Overrides the Collector.collect method
        """
        for uuid in self.bcache_uuids():
            for device in self.map_uuid_to_bcache(uuid):
                for t in ['five_minute', 'hour', 'day', 'total']:
                    cache_ratio = self.get_cache_ratio(uuid, t)
                    metric_name = "%s.cache_ratio-%s" % (device, t)
                    self.publish(metric_name, cache_ratio)

                for c in ['bypass_hits', 'bypass_misses', 'hits',
                          'miss_collisions', 'misses', 'readaheads']:
                    cache_result = self.get_cache_result(uuid, c)
                    metric_name = "%s.cache_results-%s" % (device, c)
                    self.publish(metric_name, cache_result)

        return None
