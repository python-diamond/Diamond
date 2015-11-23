# coding=utf-8

"""
The XFSCollector collects XFS metrics using /proc/fs/xfs/stat.

#### Dependencies

 * /proc/fs/xfs/stat

"""

import diamond.collector
import sys


class XFSCollector(diamond.collector.Collector):

    PROC = '/proc/fs/xfs/stat'

    def get_default_config_help(self):
        config_help = super(XFSCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the xfs collector settings
        """
        config = super(XFSCollector, self).get_default_config()
        config.update({
            'path': 'xfs'
        })
        return config

    def collect(self):
        """
        Collect xfs stats.

        For an explanation of the following metrics visit
        http://xfs.org/index.php/Runtime_Stats
        https://github.com/torvalds/linux/blob/master/fs/xfs/xfs_stats.h
        """
        data_structure = {
            'extent_alloc': (
                'alloc_extent',
                'alloc_block',
                'free_extent',
                'free_block'
            ),
            'abt': (
                'lookup',
                'compare',
                'insrec',
                'delrec'
            ),
            'blk_map': (
                'read_ops',
                'write_ops',
                'unmap',
                'add_exlist',
                'del_exlist',
                'look_exlist',
                'cmp_exlist'
            ),
            'bmbt': (
                'lookup',
                'compare',
                'insrec',
                'delrec'
            ),
            'dir': (
                'lookup',
                'create',
                'remove',
                'getdents'
            ),
            'trans': (
                'sync',
                'async',
                'empty'
            ),
            'ig': (
                'ig_attempts',
                'ig_found',
                'ig_frecycle',
                'ig_missed',
                'ig_dup',
                'ig_reclaims',
                'ig_attrchg'
            ),
            'log': (
                'writes',
                'blocks',
                'noiclogs',
                'force',
                'force_sleep'
            ),
            'push_ail': (
                'try_logspace',
                'sleep_logspace',
                'pushes',
                'success',
                'pushbuf',
                'pinned',
                'locked',
                'flushing',
                'restarts',
                'flush'
            ),
            'xstrat': (
                'quick',
                'split'
            ),
            'rw': (
                'write_calls',
                'read_calls'
            ),
            'attr': (
                'get',
                'set',
                'remove',
                'list'
            ),
            'icluster': (
                'iflush_count',
                'icluster_flushcnt',
                'icluster_flushinode'
            ),
            'vnodes': (
                'vn_active',
                'vn_alloc',
                'vn_get',
                'vn_hold',
                'vn_rele',
                'vn_reclaim',
                'vn_remove',
                'vn_free'
            ),
            'buf': (
                'xb_get',
                'xb_create',
                'xb_get_locked',
                'xb_get_locked_waited',
                'xb_busy_locked',
                'xb_miss_locked',
                'xb_page_retries',
                'xb_page_found',
                'xb_get_read'
            ),
            'abtb2': (
                'xs_abtb_2_lookup',
                'xs_abtb_2_compare',
                'xs_abtb_2_insrec',
                'xs_abtb_2_delrec',
                'xs_abtb_2_newroot',
                'xs_abtb_2_killroot',
                'xs_abtb_2_increment',
                'xs_abtb_2_decrement',
                'xs_abtb_2_lshift',
                'xs_abtb_2_rshift',
                'xs_abtb_2_split',
                'xs_abtb_2_join',
                'xs_abtb_2_alloc',
                'xs_abtb_2_free',
                'xs_abtb_2_moves'
            ),
            'abtc2': (
                'xs_abtc_2_lookup',
                'xs_abtc_2_compare',
                'xs_abtc_2_insrec',
                'xs_abtc_2_delrec',
                'xs_abtc_2_newroot',
                'xs_abtc_2_killroot',
                'xs_abtc_2_increment',
                'xs_abtc_2_decrement',
                'xs_abtc_2_lshift',
                'xs_abtc_2_rshift',
                'xs_abtc_2_split',
                'xs_abtc_2_join',
                'xs_abtc_2_alloc',
                'xs_abtc_2_free',
                'xs_abtc_2_moves'
            ),
            'bmbt2': (
                'xs_bmbt_2_lookup',
                'xs_bmbt_2_compare',
                'xs_bmbt_2_insrec',
                'xs_bmbt_2_delrec',
                'xs_bmbt_2_newroot',
                'xs_bmbt_2_killroot',
                'xs_bmbt_2_increment',
                'xs_bmbt_2_decrement',
                'xs_bmbt_2_lshift',
                'xs_bmbt_2_rshift',
                'xs_bmbt_2_split',
                'xs_bmbt_2_join',
                'xs_bmbt_2_alloc',
                'xs_bmbt_2_free',
                'xs_bmbt_2_moves'
            ),
            'ibt2': (
                'lookup',
                'compare',
                'insrec',
                'delrec',
                'newroot',
                'killroot',
                'increment',
                'decrement',
                'lshift',
                'rshift',
                'split',
                'join',
                'alloc',
                'free',
                'moves'
            ),
            'xpc': (
                'xs_xstrat_bytes',
                'xs_write_bytes',
                'xs_read_bytes'
            ),
            'debug': (
                'debug',
            )
        }

        f = open(self.PROC)
        new_stats = f.readlines()
        f.close()

        stats = {}
        for line in new_stats:
            items = line.rstrip().split()
            stats[items[0]] = [int(a) for a in items[1:]]

        for key in stats.keys():
            for item in enumerate(data_structure[key]):
                metric_name = '.'.join([key, item[1]])
                value = stats[key][item[0]]
                self.publish_counter(metric_name, value)
