try:
    import json
except ImportError:
    import simplejson as json

import subprocess
import re
import os
import sys
import diamond.collector

"""
Get usage statistics from the ceph cluster.
Total as well as per pool.
"""

class CephPoolStatsCollector(diamond.collector.Collector):

    labels = {'rd_kb':'read_kb', 'wr_kb':'written_kb', 'rd':'read_obj', 'wr':'written_obj', 'bytes_used':'used_bytes', 'objects':'objects'}

    def collect(self):

        try:
            """
            Unfortunately the dumpling "ceph" cli tool does not (yet) support a timeout feature. Starting with Emporer it is possible...
            """
            output = subprocess.check_output(['ceph', 'df', 'detail', '--format=json'])
        except subprocess.CalledProcessError, err:
            self.log.info( 'Could not get stats: %s' % err)
            self.log.exception('Could not get stats')
            return False

        try:
            jsonData = json.loads(output)
        except Exception, err:
            self.log.info('Could not parse stats from ceph df: %s', err)
            self.log.exception('Could not parse stats from ceph df')
            return False

        stats = jsonData["stats"]

        for s in ['total_space', 'total_used', 'total_objects']:
            self.publish(s, stats[s], metric_type='GAUGE')

        pools = jsonData["pools"]

        for p in pools:
            metric = 'pool.' + p["name"]

            """
            The "kb" values are discarded, as their content is just a duplicate
            of the byte-based values. Grafana can handle this for us.
            """

            for s in p["stats"]:
                if s in ['bytes_used', 'objects']:
                    self.publish(metric + '.' + self.labels[s], p["stats"][s], metric_type='GAUGE')

                if s in ['rd_kb', 'wr_kb', 'rd', 'wr']:
                    self.publish(metric + '.' + self.labels[s], p["stats"][s], metric_type='COUNTER')

        return True
