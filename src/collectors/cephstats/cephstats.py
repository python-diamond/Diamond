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


# This is external to the CephCollector so it can be tested
# separately.
def process_ceph_status(output):
    pattern = re.compile(r'\bclient io .*')
    res = pattern.search(output)
    if not res:
        return {}
    try:
        ceph_stats = res.group()
        number = re.compile(r'\d+')
        rd = number.search(ceph_stats)
        if rd:
            wr = number.search(ceph_stats, rd.end())
            if wr:
                iops = number.search(ceph_stats, wr.end())
        ret = {}
        if rd:
            ret['rd'] = rd.group()
        if wr:
            ret['wr'] = wr.group()
        if iops:
            ret['iops'] = iops.group()
        return ret
    except:
        return {}


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
