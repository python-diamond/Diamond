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

patternchk = re.compile(r'\bclient io .*')
numberchk = re.compile(r'\d+')


# This is external to the CephCollector so it can be tested
# separately.
def process_ceph_status(output):
    res = patternchk.search(output)
    if not res:
        return {}
    ceph_stats = res.group()
    if not ceph_stats:
        return {}
    ret = {}
    rd = wr = iops = None
    rd = numberchk.search(ceph_stats)
    if rd is not None:
        ret['rd'] = rd.group()
        wr = numberchk.search(ceph_stats, rd.end())
        if wr is not None:
            ret['wr'] = wr.group()
            iops = numberchk.search(ceph_stats, wr.end())
            if iops is not None:
                ret['iops'] = iops.group()
    return ret


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

        return process_ceph_status(output)

    def collect(self):
        """
        Collect ceph stats
        """
        stats = self._get_stats()
        self._publish_stats('cephstats', stats)

        return
