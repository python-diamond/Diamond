# coding=utf-8

"""
Get ceph status from one node
"""

import subprocess
import re
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'ceph'))
from ceph import CephCollector


class CephStatsCollector(CephCollector):
    def _get_stats(self):
        """
        Get ceph stats
        """
        try:
            output = subprocess.check_output(['ceph', '-s'])
        except subprocess.CalledProcessError, err:
            self.log.info(
                'Could not get stats: %s' % err)
            self.log.exception('Could not get stats')
            return {}

        pattern = re.compile(r'\bclient io .*')
        ceph_stats = pattern.search(output).group()
        number = re.compile(r'\d+')
        rd = number.search(ceph_stats)
        wr = number.search(ceph_stats, rd.end())
        iops = number.search(ceph_stats, wr.end())

        return {'rd': rd.group(), 'wr': wr.group(), 'iops': iops.group()}

    def collect(self):
        """
        Collect ceph stats
        """
        stats = self._get_stats()
        self._publish_stats('cephstats', stats)

        return
