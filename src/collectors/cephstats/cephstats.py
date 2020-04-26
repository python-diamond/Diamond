# coding=utf-8

"""
Get ceph status from one node
"""

import subprocess
import re
import os
import sys
from ceph import CephCollector
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'ceph'))


patternchk = re.compile(r'\bclient io .*')
numberchk = re.compile(r'\d+')
unitchk = re.compile(r'[a-zA-Z]{1,2}')

# This is external to the CephCollector so it can be tested
# separately.


def to_bytes(value, unit):
    fval = float(value)
    unit = str(unit.lower()).strip()
    if unit == "b":
        return fval
    unit_list = {'kb': 1, 'mb': 2, 'gb': 3, 'tb': 4, 'pb': 5, 'eb': 6}
    for i in range(unit_list[unit]):
        fval = fval * 1000
    return fval


def process_ceph_status(output):
    res = patternchk.search(output)
    if not res:
        return {}
    ceph_stats = res.group()
    if not ceph_stats:
        return {}
    ret = {}
    rd = wr = iops = runit = wunit = None
    rd = numberchk.search(ceph_stats)
    if rd is not None:
        runit = unitchk.search(ceph_stats, rd.end())
        if runit is None:
            self.log.exception('Could not get read units')
            return {}
        ret['rd'] = repr(to_bytes(rd.group(), runit.group()))
        wr = numberchk.search(ceph_stats, rd.end())
        if wr is not None:
            wunit = unitchk.search(ceph_stats, wr.end())
            if runit is None:
                self.log.exception('Could not get read units')
                return {}
            ret['wr'] = repr(to_bytes(wr.group(), wunit.group()))
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
        except subprocess.CalledProcessError as err:
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
