<!--This file was generated from the python source
Please edit the source to make changes
-->
XFSCollector
=====

The XFSCollector collects XFS metrics using /proc/fs/xfs/stat.

#### Dependencies

 * /proc/fs/xfs/stat


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.xfs.abt.compare 0
servers.hostname.xfs.abt.delrec 0
servers.hostname.xfs.abt.insrec 0
servers.hostname.xfs.abt.lookup 0
servers.hostname.xfs.abtb2.xs_abtb_2_alloc 0
servers.hostname.xfs.abtb2.xs_abtb_2_compare 1876
servers.hostname.xfs.abtb2.xs_abtb_2_decrement 0
servers.hostname.xfs.abtb2.xs_abtb_2_delrec 47
servers.hostname.xfs.abtb2.xs_abtb_2_free 0
servers.hostname.xfs.abtb2.xs_abtb_2_increment 0
servers.hostname.xfs.abtb2.xs_abtb_2_insrec 47
servers.hostname.xfs.abtb2.xs_abtb_2_join 0
servers.hostname.xfs.abtb2.xs_abtb_2_killroot 0
servers.hostname.xfs.abtb2.xs_abtb_2_lookup 203
servers.hostname.xfs.abtb2.xs_abtb_2_lshift 0
servers.hostname.xfs.abtb2.xs_abtb_2_moves 7040
servers.hostname.xfs.abtb2.xs_abtb_2_newroot 0
servers.hostname.xfs.abtb2.xs_abtb_2_rshift 0
servers.hostname.xfs.abtb2.xs_abtb_2_split 0
servers.hostname.xfs.abtc2.xs_abtc_2_alloc 0
servers.hostname.xfs.abtc2.xs_abtc_2_compare 4014
servers.hostname.xfs.abtc2.xs_abtc_2_decrement 0
servers.hostname.xfs.abtc2.xs_abtc_2_delrec 203
servers.hostname.xfs.abtc2.xs_abtc_2_free 0
servers.hostname.xfs.abtc2.xs_abtc_2_increment 0
servers.hostname.xfs.abtc2.xs_abtc_2_insrec 203
servers.hostname.xfs.abtc2.xs_abtc_2_join 0
servers.hostname.xfs.abtc2.xs_abtc_2_killroot 0
servers.hostname.xfs.abtc2.xs_abtc_2_lookup 422
servers.hostname.xfs.abtc2.xs_abtc_2_lshift 0
servers.hostname.xfs.abtc2.xs_abtc_2_moves 34516
servers.hostname.xfs.abtc2.xs_abtc_2_newroot 0
servers.hostname.xfs.abtc2.xs_abtc_2_rshift 0
servers.hostname.xfs.abtc2.xs_abtc_2_split 0
servers.hostname.xfs.attr.get 54995
servers.hostname.xfs.attr.list 0
servers.hostname.xfs.attr.remove 0
servers.hostname.xfs.attr.set 0
servers.hostname.xfs.blk_map.add_exlist 58
servers.hostname.xfs.blk_map.cmp_exlist 0
servers.hostname.xfs.blk_map.del_exlist 116
servers.hostname.xfs.blk_map.look_exlist 124879
servers.hostname.xfs.blk_map.read_ops 124647
servers.hostname.xfs.blk_map.unmap 116
servers.hostname.xfs.blk_map.write_ops 116
servers.hostname.xfs.bmbt.compare 0
servers.hostname.xfs.bmbt.delrec 0
servers.hostname.xfs.bmbt.insrec 0
servers.hostname.xfs.bmbt.lookup 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_alloc 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_compare 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_decrement 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_delrec 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_free 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_increment 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_insrec 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_join 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_killroot 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_lookup 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_lshift 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_moves 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_newroot 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_rshift 0
servers.hostname.xfs.bmbt2.xs_bmbt_2_split 0
servers.hostname.xfs.buf.xb_busy_locked 0
servers.hostname.xfs.buf.xb_create 6671
servers.hostname.xfs.buf.xb_get 39013
servers.hostname.xfs.buf.xb_get_locked 32391
servers.hostname.xfs.buf.xb_get_locked_waited 0
servers.hostname.xfs.buf.xb_get_read 6671
servers.hostname.xfs.buf.xb_miss_locked 6671
servers.hostname.xfs.buf.xb_page_found 13217
servers.hostname.xfs.buf.xb_page_retries 0
servers.hostname.xfs.debug.debug 0
servers.hostname.xfs.dir.create 58
servers.hostname.xfs.dir.getdents 334948
servers.hostname.xfs.dir.lookup 49652
servers.hostname.xfs.dir.remove 58
servers.hostname.xfs.extent_alloc.alloc_block 928
servers.hostname.xfs.extent_alloc.alloc_extent 58
servers.hostname.xfs.extent_alloc.free_block 928
servers.hostname.xfs.extent_alloc.free_extent 116
servers.hostname.xfs.ibt2.alloc 0
servers.hostname.xfs.ibt2.compare 1214
servers.hostname.xfs.ibt2.decrement 0
servers.hostname.xfs.ibt2.delrec 0
servers.hostname.xfs.ibt2.free 0
servers.hostname.xfs.ibt2.increment 0
servers.hostname.xfs.ibt2.insrec 0
servers.hostname.xfs.ibt2.join 0
servers.hostname.xfs.ibt2.killroot 0
servers.hostname.xfs.ibt2.lookup 138
servers.hostname.xfs.ibt2.lshift 0
servers.hostname.xfs.ibt2.moves 0
servers.hostname.xfs.ibt2.newroot 0
servers.hostname.xfs.ibt2.rshift 0
servers.hostname.xfs.ibt2.split 0
servers.hostname.xfs.icluster.icluster_flushcnt 16
servers.hostname.xfs.icluster.icluster_flushinode 16
servers.hostname.xfs.icluster.iflush_count 49
servers.hostname.xfs.ig.ig_attempts 0
servers.hostname.xfs.ig.ig_attrchg 0
servers.hostname.xfs.ig.ig_dup 0
servers.hostname.xfs.ig.ig_found 13142
servers.hostname.xfs.ig.ig_frecycle 0
servers.hostname.xfs.ig.ig_missed 34759
servers.hostname.xfs.ig.ig_reclaims 110424
servers.hostname.xfs.log.blocks 8320
servers.hostname.xfs.log.force 681
servers.hostname.xfs.log.force_sleep 65
servers.hostname.xfs.log.noiclogs 0
servers.hostname.xfs.log.writes 65
servers.hostname.xfs.push_ail.flush 0
servers.hostname.xfs.push_ail.flushing 0
servers.hostname.xfs.push_ail.locked 0
servers.hostname.xfs.push_ail.pinned 0
servers.hostname.xfs.push_ail.pushbuf 144
servers.hostname.xfs.push_ail.pushes 2521
servers.hostname.xfs.push_ail.restarts 0
servers.hostname.xfs.push_ail.sleep_logspace 0
servers.hostname.xfs.push_ail.success 41
servers.hostname.xfs.push_ail.try_logspace 13403
servers.hostname.xfs.rw.read_calls 1909917
servers.hostname.xfs.rw.write_calls 584
servers.hostname.xfs.trans.async 586
servers.hostname.xfs.trans.empty 0
servers.hostname.xfs.trans.sync 7
servers.hostname.xfs.vnodes.vn_active 0
servers.hostname.xfs.vnodes.vn_alloc 0
servers.hostname.xfs.vnodes.vn_free 0
servers.hostname.xfs.vnodes.vn_get 0
servers.hostname.xfs.vnodes.vn_hold 0
servers.hostname.xfs.vnodes.vn_reclaim 110462
servers.hostname.xfs.vnodes.vn_rele 110462
servers.hostname.xfs.vnodes.vn_remove 110462
servers.hostname.xfs.xpc.xs_read_bytes 2953097143
servers.hostname.xfs.xpc.xs_write_bytes 270944
servers.hostname.xfs.xpc.xs_xstrat_bytes 3801088
servers.hostname.xfs.xstrat.quick 58
servers.hostname.xfs.xstrat.split 0
```

