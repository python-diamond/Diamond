VarnishCollector
=====

VarnishCollector grabs stats from Varnish and submits them the Graphite

#### Dependencies

 * /usr/bin/varnishstat


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>bin</td><td>/usr/bin/varnishstat</td><td>The path to the varnishstat binary</td><td>str</td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>sudo_cmd</td><td>/usr/bin/sudo</td><td>Path to sudo</td><td>str</td></tr>
<tr><td>use_sudo</td><td>False</td><td>Use sudo?</td><td>bool</td></tr>
</table>

#### Example Output

```
servers.hostname.varnish.accept_fail 0
servers.hostname.varnish.backend_busy 0
servers.hostname.varnish.backend_conn 13363
servers.hostname.varnish.backend_fail 0
servers.hostname.varnish.backend_recycle 0
servers.hostname.varnish.backend_req 13363
servers.hostname.varnish.backend_retry 0
servers.hostname.varnish.backend_reuse 0
servers.hostname.varnish.backend_toolate 0
servers.hostname.varnish.backend_unhealthy 0
servers.hostname.varnish.cache_hit 6580
servers.hostname.varnish.cache_hitpass 0
servers.hostname.varnish.cache_miss 2566
servers.hostname.varnish.client_conn 10799
servers.hostname.varnish.client_drop 0
servers.hostname.varnish.client_drop_late 0
servers.hostname.varnish.client_req 10796
servers.hostname.varnish.dir_dns_cache_full 0
servers.hostname.varnish.dir_dns_failed 0
servers.hostname.varnish.dir_dns_hit 0
servers.hostname.varnish.dir_dns_lookups 0
servers.hostname.varnish.esi_errors 0
servers.hostname.varnish.esi_warnings 0
servers.hostname.varnish.fetch_1xx 0
servers.hostname.varnish.fetch_204 0
servers.hostname.varnish.fetch_304 45
servers.hostname.varnish.fetch_bad 0
servers.hostname.varnish.fetch_chunked 0
servers.hostname.varnish.fetch_close 331
servers.hostname.varnish.fetch_eof 0
servers.hostname.varnish.fetch_failed 0
servers.hostname.varnish.fetch_head 0
servers.hostname.varnish.fetch_length 12986
servers.hostname.varnish.fetch_oldhttp 0
servers.hostname.varnish.fetch_zero 0
servers.hostname.varnish.hcb_insert 2379
servers.hostname.varnish.hcb_lock 2379
servers.hostname.varnish.hcb_nolock 9146
servers.hostname.varnish.losthdr 0
servers.hostname.varnish.n_backend 4
servers.hostname.varnish.n_ban 1
servers.hostname.varnish.n_ban_add 1
servers.hostname.varnish.n_ban_dups 0
servers.hostname.varnish.n_ban_obj_test 0
servers.hostname.varnish.n_ban_re_test 0
servers.hostname.varnish.n_ban_retire 0
servers.hostname.varnish.n_expired 2557
servers.hostname.varnish.n_gunzip 11982
servers.hostname.varnish.n_gzip 8277
servers.hostname.varnish.n_lru_moved 5588
servers.hostname.varnish.n_lru_nuked 0
servers.hostname.varnish.n_object 9
servers.hostname.varnish.n_objectcore 17
servers.hostname.varnish.n_objecthead 27
servers.hostname.varnish.n_objoverflow 0
servers.hostname.varnish.n_objsendfile 0
servers.hostname.varnish.n_objwrite 2546
servers.hostname.varnish.n_sess 1
servers.hostname.varnish.n_sess_mem 19
servers.hostname.varnish.n_vampireobject 0
servers.hostname.varnish.n_vbc 1
servers.hostname.varnish.n_vcl 1
servers.hostname.varnish.n_vcl_avail 1
servers.hostname.varnish.n_vcl_discard 0
servers.hostname.varnish.n_waitinglist 10
servers.hostname.varnish.n_wrk 10
servers.hostname.varnish.n_wrk_create 10
servers.hostname.varnish.n_wrk_drop 0
servers.hostname.varnish.n_wrk_failed 0
servers.hostname.varnish.n_wrk_lqueue 0
servers.hostname.varnish.n_wrk_max 11451
servers.hostname.varnish.n_wrk_queued 0
servers.hostname.varnish.s_bodybytes 23756354
servers.hostname.varnish.s_fetch 13362
servers.hostname.varnish.s_hdrbytes 4764593
servers.hostname.varnish.s_pass 10796
servers.hostname.varnish.s_pipe 0
servers.hostname.varnish.s_req 10796
servers.hostname.varnish.s_sess 10798
servers.hostname.varnish.sess_closed 10798
servers.hostname.varnish.sess_herd 0
servers.hostname.varnish.sess_linger 0
servers.hostname.varnish.sess_pipeline 0
servers.hostname.varnish.sess_readahead 0
servers.hostname.varnish.shm_cont 0
servers.hostname.varnish.shm_cycles 0
servers.hostname.varnish.shm_flushes 0
servers.hostname.varnish.shm_records 1286246
servers.hostname.varnish.shm_writes 102894
servers.hostname.varnish.sms_balloc 0
servers.hostname.varnish.sms_bfree 0
servers.hostname.varnish.sms_nbytes 0
servers.hostname.varnish.sms_nobj 0
servers.hostname.varnish.sms_nreq 0
servers.hostname.varnish.uptime 35440
```

### This file was generated from the python source
### Please edit the source to make changes

