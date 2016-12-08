"""
Collect memcached slab stats

#### Example Configuration

[[MemcachedSlabCollector]]
enabled = True
host = localhost  # optional
port = 11211  # optional
"""

from collections import defaultdict
import socket

import diamond.collector
from diamond.metric import Metric


def parse_slab_stats(slab_stats):
    """Convert output from memcached's `stats slabs` into a Python dict.

    Newlines are returned by memcached along with carriage returns
    (i.e. '\r\n').

    >>> parse_slab_stats(
            "STAT 1:chunk_size 96\r\nSTAT 1:chunks_per_page 10922\r\nSTAT "
            "active_slabs 1\r\nSTAT total_malloced 1048512\r\nEND\r\n")
    {
        'slabs': {
            1: {
                'chunk_size': 96,
                'chunks_per_page': 10922,
                # ...
            },
        },
        'active_slabs': 1,
        'total_malloced': 1048512,
    }
    """
    stats_dict = {}
    stats_dict['slabs'] = defaultdict(lambda: {})

    for line in slab_stats.splitlines():
        if line == 'END':
            break
        # e.g.: "STAT 1:chunks_per_page 10922"
        cmd, key, value = line.split(' ')
        if cmd != 'STAT':
            continue
        # e.g.: "STAT active_slabs 1"
        if ":" not in key:
            stats_dict[key] = int(value)
            continue
        slab, key = key.split(':')
        stats_dict['slabs'][int(slab)][key] = int(value)

    return stats_dict


def dict_to_paths(dict_):
    """Convert a dict to metric paths.

    >>> dict_to_paths({'foo': {'bar': 1}, 'baz': 2})
    {
        'foo.bar': 1,
        'baz': 2,
    }
    """
    metrics = {}
    for k, v in dict_.iteritems():
        if isinstance(v, dict):
            submetrics = dict_to_paths(v)
            for subk, subv in submetrics.iteritems():
                metrics['.'.join([str(k), str(subk)])] = subv
        else:
            metrics[k] = v
    return metrics


class MemcachedSlabCollector(diamond.collector.Collector):

    def process_config(self):
        super(MemcachedSlabCollector, self).process_config()
        self.host = self.config['host']
        self.port = int(self.config['port'])

    def get_default_config(self):
        config = super(MemcachedSlabCollector, self).get_default_config()
        # Output stats in the format:
        # 'servers.cache-main-01.memcached_slab.slabs.1.chunk_size'
        config.update({
            'interval': 60,
            'path_prefix': 'servers',
            'path': 'memcached_slab',
            'host': 'localhost',
            'port': 11211,
        })
        return config

    def get_slab_stats(self):
        """Retrieve slab stats from memcached."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.send("stats slabs\n")
        try:
            data = ""
            while True:
                data += s.recv(4096)
                if data.endswith('END\r\n'):
                    break
            return data
        finally:
            s.close()

    def collect(self):
        unparsed_slab_stats = self.get_slab_stats()
        slab_stats = parse_slab_stats(unparsed_slab_stats)
        paths = dict_to_paths(slab_stats)
        for path, value in paths.iteritems():
            # Add path and prefix to metric (e.g.
            # 'servers.cache-main-01.memchached_slab')
            full_path = self.get_metric_path(path)
            metric = Metric(full_path, value)
            self.publish_metric(metric)
