# coding=utf-8

"""
VarnishCollector grabs stats from Varnish and submits them the Graphite

#### Dependencies

 * /usr/bin/varnishstat

"""

import diamond.collector
import re
import subprocess
from diamond.collector import str_to_bool


class VarnishCollector(diamond.collector.Collector):

    _RE = re.compile("^(?P<stat>[\w_.,]*)\s+(?P<psa>\d*)\s+"
                     "(?P<psan>[\d.]*)\s+(?P<desc>.*)$", re.M)
    _KEYS_v3 = frozenset([
        'client_conn', 'client_drop', 'client_req', 'cache_hit',
        'cache_hitpass', 'cache_miss', 'backend_conn', 'backend_unhealthy',
        'backend_busy', 'backend_fail', 'backend_reuse', 'backend_toolate',
        'backend_recycle', 'backend_retry', 'fetch_head', 'fetch_length',
        'fetch_chunked', 'fetch_eof', 'fetch_bad', 'fetch_close',
        'fetch_oldhttp', 'fetch_zero', 'fetch_failed', 'fetch_1xx',
        'fetch_204', 'fetch_304', 'n_sess_mem',
        'n_sess', 'n_object', 'n_vampireobject', 'n_objectcore',
        'n_objecthead', 'n_waitinglist', 'n_vbc', 'n_wrk', 'n_wrk_create',
        'n_wrk_failed', 'n_wrk_max', 'n_wrk_lqueue', 'n_wrk_queued',
        'n_wrk_drop', 'n_backend', 'n_expired', 'n_lru_nuked',
        'n_lru_moved', 'losthdr', 'n_objsendfile', 'n_objwrite',
        'n_objoverflow', 's_sess', 's_req', 's_pipe', 's_pass', 's_fetch',
        's_hdrbytes', 's_bodybytes', 'sess_closed', 'sess_pipeline',
        'sess_readahead', 'sess_linger', 'sess_herd', 'shm_records',
        'shm_writes', 'shm_flushes', 'shm_cont', 'shm_cycles', 'sms_nreq',
        'sms_nobj', 'sms_nbytes', 'sms_balloc', 'sms_bfree', 'backend_req',
        'n_vcl', 'n_vcl_avail', 'n_vcl_discard', 'n_ban', 'n_ban_add',
        'n_ban_retire', 'n_ban_obj_test', 'n_ban_re_test', 'n_ban_dups',
        'hcb_nolock', 'hcb_lock', 'hcb_insert', 'esi_errors',
        'esi_warnings', 'accept_fail', 'client_drop_late', 'uptime',
        'dir_dns_lookups', 'dir_dns_failed', 'dir_dns_hit',
        'dir_dns_cache_full', 'n_gzip', 'n_gunzip',
    ])

    _KEYS_v4 = frozenset([
        'MAIN.uptime', 'MAIN.sess_conn', 'MAIN.sess_drop', 'MAIN.sess_fail',
        'MAIN.sess_pipe_overflow', 'MAIN.client_req_400', 'MAIN.client_req_411',
        'MAIN.client_req_413', 'MAIN.client_req_417', 'MAIN.client_req',
        'MAIN.cache_hit', 'MAIN.cache_hitpass', 'MAIN.cache_miss',
        'MAIN.backend_conn', 'MAIN.backend_unhealthy', 'MAIN.backend_busy',
        'MAIN.backend_fail', 'MAIN.backend_reuse', 'MAIN.backend_toolate',
        'MAIN.backend_recycle', 'MAIN.backend_retry', 'MAIN.fetch_head',
        'MAIN.fetch_length', 'MAIN.fetch_chunked', 'MAIN.fetch_eof',
        'MAIN.fetch_bad', 'MAIN.fetch_close', 'MAIN.fetch_oldhttp',
        'MAIN.fetch_zero', 'MAIN.fetch_1xx', 'MAIN.fetch_204', 'MAIN.fetch_304',
        'MAIN.fetch_failed', 'MAIN.fetch_no_thread', 'MAIN.pools',
        'MAIN.threads', 'MAIN.threads_limited',
        'MAIN.threads_created', 'MAIN.threads_destroyed', 'MAIN.threads_failed',
        'MAIN.thread_queue_len', 'MAIN.busy_sleep', 'MAIN.busy_wakeup',
        'MAIN.sess_queued', 'MAIN.sess_dropped', 'MAIN.n_object',
        'MAIN.n_vampireobject', 'MAIN.n_objectcore', 'MAIN.n_objecthead',
        'MAIN.n_waitinglist', 'MAIN.n_backend', 'MAIN.n_expired',
        'MAIN.n_lru_nuked', 'MAIN.n_lru_moved', 'MAIN.losthdr', 'MAIN.s_sess',
        'MAIN.s_req', 'MAIN.s_pipe', 'MAIN.s_pass', 'MAIN.s_fetch',
        'MAIN.s_synth',
        'MAIN.s_req_hdrbytes', 'MAIN.s_req_bodybytes', 'MAIN.s_resp_hdrbytes',
        'MAIN.s_resp_bodybytes', 'MAIN.s_pipe_hdrbytes', 'MAIN.s_pipe_in',
        'MAIN.s_pipe_out', 'MAIN.sess_closed', 'MAIN.sess_pipeline',
        'MAIN.sess_readahead', 'MAIN.sess_herd', 'MAIN.shm_records',
        'MAIN.shm_writes', 'MAIN.shm_flushes', 'MAIN.shm_cont',
        'MAIN.shm_cycles',
        'MAIN.sms_nreq', 'MAIN.sms_nobj', 'MAIN.sms_nbytes', 'MAIN.sms_balloc',
        'MAIN.sms_bfree', 'MAIN.backend_req', 'MAIN.n_vcl', 'MAIN.n_vcl_avail',
        'MAIN.n_vcl_discard', 'MAIN.bans', 'MAIN.bans_completed',
        'MAIN.bans_obj',
        'MAIN.bans_req', 'MAIN.bans_added', 'MAIN.bans_deleted',
        'MAIN.bans_tested',
        'MAIN.bans_obj_killed', 'MAIN.bans_lurker_tested',
        'MAIN.bans_tests_tested',
        'MAIN.bans_lurker_tests_tested', 'MAIN.bans_lurker_obj_killed',
        'MAIN.bans_dups', 'MAIN.bans_lurker_contention',
        'MAIN.bans_persisted_bytes',
        'MAIN.bans_persisted_fragmentation', 'MAIN.n_purges',
        'MAIN.n_obj_purged', 'MAIN.exp_mailed', 'MAIN.exp_received',
        'MAIN.hcb_nolock', 'MAIN.hcb_lock', 'MAIN.hcb_insert',
        'MAIN.esi_errors',
        'MAIN.esi_warnings', 'MAIN.vmods', 'MAIN.n_gzip', 'MAIN.n_gunzip',
        'MAIN.vsm_free', 'MAIN.vsm_used', 'MAIN.vsm_cooling',
        'MAIN.vsm_overflow',
        'MAIN.vsm_overflowed', 'MGT.uptime', 'MGT.child_start',
        'MGT.child_exit',
        'MGT.child_stop', 'MGT.child_died', 'MGT.child_dump', 'MGT.child_panic',
        'LCK.sms.creat', 'LCK.sms.destroy', 'LCK.sms.locks', 'LCK.smp.creat',
        'LCK.smp.destroy', 'LCK.smp.locks', 'LCK.sma.creat', 'LCK.sma.destroy',
        'LCK.sma.locks', 'LCK.smf.creat', 'LCK.smf.destroy', 'LCK.smf.locks',
        'LCK.hsl.creat', 'LCK.hsl.destroy', 'LCK.hsl.locks', 'LCK.hcb.creat',
        'LCK.hcb.destroy', 'LCK.hcb.locks', 'LCK.hcl.creat', 'LCK.hcl.destroy',
        'LCK.hcl.locks', 'LCK.vcl.creat', 'LCK.vcl.destroy', 'LCK.vcl.locks',
        'LCK.sessmem.creat', 'LCK.sessmem.destroy', 'LCK.sessmem.locks',
        'LCK.sess.creat', 'LCK.sess.destroy', 'LCK.sess.locks',
        'LCK.wstat.creat',
        'LCK.wstat.destroy', 'LCK.wstat.locks', 'LCK.herder.creat',
        'LCK.herder.destroy', 'LCK.herder.locks', 'LCK.wq.creat',
        'LCK.wq.destroy',
        'LCK.wq.locks', 'LCK.objhdr.creat', 'LCK.objhdr.destroy',
        'LCK.objhdr.locks',
        'LCK.exp.creat', 'LCK.exp.destroy', 'LCK.exp.locks', 'LCK.lru.creat',
        'LCK.lru.destroy', 'LCK.lru.locks', 'LCK.cli.creat', 'LCK.cli.destroy',
        'LCK.cli.locks', 'LCK.ban.creat', 'LCK.ban.destroy', 'LCK.ban.locks',
        'LCK.vbp.creat', 'LCK.vbp.destroy', 'LCK.vbp.locks',
        'LCK.backend.creat',
        'LCK.backend.destroy', 'LCK.backend.locks', 'LCK.vcapace.creat',
        'LCK.vcapace.destroy', 'LCK.vcapace.locks', 'LCK.nbusyobj.creat',
        'LCK.nbusyobj.destroy', 'LCK.nbusyobj.locks', 'LCK.busyobj.creat',
        'LCK.busyobj.destroy', 'LCK.busyobj.locks', 'LCK.mempool.creat',
        'LCK.mempool.destroy', 'LCK.mempool.locks', 'LCK.vxid.creat',
        'LCK.vxid.destroy', 'LCK.vxid.locks', 'LCK.pipestat.creat',
        'LCK.pipestat.destroy', 'LCK.pipestat.locks'
    ])

    def get_default_config_help(self):
        config_help = super(VarnishCollector, self).get_default_config_help()
        config_help.update({
            'bin':         'The path to the varnishstat binary',
            'use_sudo':    'Use sudo?',
            'sudo_cmd':    'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(VarnishCollector, self).get_default_config()
        config.update({
            'path':             'varnish',
            'bin':             '/usr/bin/varnishstat',
            'use_sudo':         False,
            'sudo_cmd':         '/usr/bin/sudo',
        })
        return config

    def collect(self):
        data = {}
        output = self.poll()

        matches = self._RE.findall(output)
        # No matches at all, bail out
        if not matches:
            return

        # Check first line to see if it begins with MAIN.,
        # If so, this is varnish 4.0 stats
        if matches[0][0].startswith('MAIN.'):
            keys = self._KEYS_v4
        else:
            keys = self._KEYS_v3

        for line in matches:
            if line[0] in keys:
                data[line[0]] = line[1]

        for key in data:
            self.publish(key, int(data[key]))

    def poll(self):
        try:
            command = [self.config['bin'], '-1']

            if str_to_bool(self.config['use_sudo']):
                command.insert(0, self.config['sudo_cmd'])

            output = subprocess.Popen(command,
                                      stdout=subprocess.PIPE).communicate()[0]
        except OSError:
            output = ""

        return output
