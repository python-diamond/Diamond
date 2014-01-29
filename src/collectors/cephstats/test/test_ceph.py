#!/usr/bin/env python
import os
import sys

curdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curdir)
sys.path.insert(0, '../')

import unittest
import re


def get_ceph_info(info):
    # pattern for ceph information
    pattern = re.compile(r'\bclient io .*')
    ceph_info = pattern.search(info).group()

    # pattern to get number
    number = re.compile(r'\d+')

    read_per_second = number.search(ceph_info)
    write_per_second = number.search(
        ceph_info, read_per_second.end()
        )
    iops = number.search(ceph_info, write_per_second.end())

    return (
        read_per_second.group(),
        write_per_second.group(),
        iops.group()
        )


class TestCeph(unittest.TestCase):
    """
    Test collect ceph data
    """
    def test_sample_data(self):
        """
        Get ceph information from sample data
        """
        f = open('sample.txt')
        self.assertEqual(get_ceph_info(f.read()), ('8643', '4821', '481'))
        f.close()

if __name__ == '__main__':
    unittest.main()
