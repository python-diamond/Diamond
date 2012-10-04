# coding=utf-8

"""

#### Dependencies

 * MySQLdb

"""

import diamond.collector
import re
import time

try:
    import MySQLdb
    from MySQLdb import MySQLError
except ImportError:
    MySQLdb = None
    MySQLError = ValueError


class MySQLCollector(diamond.collector.Collector):

    _GAUGE_KEYS = [
        'Innodb_buffer_pool_pages_data', 'Innodb_buffer_pool_pages_dirty',
        'Innodb_buffer_pool_pages_free',
        'Innodb_buffer_pool_pages_misc', 'Innodb_buffer_pool_pages_total',
        'Innodb_data_pending_fsyncs', 'Innodb_data_pending_reads',
        'Innodb_data_pending_writes',
        'Innodb_os_log_pending_fsyncs', 'Innodb_os_log_pending_writes',
        'Innodb_page_size',
        'Innodb_row_lock_current_waits', 'Innodb_row_lock_time',
        'Innodb_row_lock_time_avg',
        'Innodb_row_lock_time_max',
        'Key_blocks_unused', 'Last_query_cost', 'Max_used_connections',
        'Open_files', 'Open_streams', 'Open_table_definitions', 'Open_tables',
        'Qcache_free_blocks', 'Qcache_free_memory',
        'Qcache_queries_in_cache', 'Qcache_total_blocks',
        'Seconds_Behind_Master',
        'Threads_cached', 'Threads_connected', 'Threads_created',
        'Threads_running',
        # innodb status non counter keys
        'Innodb_bp_created_per_sec',
        'Innodb_bp_pages_evicted_no_access_per_sec',
        'Innodb_bp_pages_not_young_per_sec',
        'Innodb_bp_pages_read_ahead_per_sec', 'Innodb_bp_pages_young_per_sec',
        'Innodb_bp_reads_per_sec', 'Innodb_bp_written_per_sec',
        'Innodb_bp_add_alloc', 'Innodb_bp_db_pages',
        'Innodb_bp_dictionary_alloc', 'Innodb_bp_free_buffers',
        'Innodb_bp_hit_rate', 'Innodb_bp_io_cur_pages',
        'Innodb_bp_io_sum_pages', 'Innodb_bp_io_unzip_cur_pages',
        'Innodb_bp_io_unzip_sum_pages', 'Innodb_bp_lru_len',
        'Innodb_bp_modified_pages', 'Innodb_bp_not_young_hit_rate',
        'Innodb_bp_old_db_pages', 'Innodb_bp_pending_pages',
        'Innodb_bp_pending_writes_flush_list', 'Innodb_bp_pending_writes_lru',
        'Innodb_bp_pending_writes_single_page', 'Innodb_bp_size',
        'Innodb_bp_total_alloc', 'Innodb_bp_unzip_lru_len',
        'Innodb_bp_young_hit_rate',
        'Innodb_hash_searches_per_sec',
        'Innodb_io_syncs_per_sec',
        'Innodb_log_io_per_sec',
        'Innodb_non_hash_searches_per_sec',
        'Innodb_per_sec_avg',
        'Innodb_reads_per_sec',
        'Innodb_rows_deleted_per_sec', 'Innodb_rows_inserted_per_sec',
        'Innodb_rows_read_per_sec', 'Innodb_rows_updated_per_sec',
        'Innodb_sem_spins_per_wait_mutex', 'Innodb_sem_spins_per_wait_rw_excl',
        'Innodb_sem_spins_per_wait_rw_shared',
        'Innodb_writes_per_sec',
        'Innodb_bytes_per_read',
        'Innodb_hash_node_heap', 'Innodb_hash_table_size',
        'Innodb_hash_used_cells',
        'Innodb_ibuf_free_list_len', 'Innodb_ibuf_seg_size', 'Innodb_ibuf_size',
        'Innodb_io_ibuf_logs', 'Innodb_io_ibuf_reads', 'Innodb_io_ibuf_syncs',
        'Innodb_io_pending_flush_bp', 'Innodb_io_pending_flush_log',
        'Innodb_io_pending_reads', 'Innodb_io_pending_writes', '',
        'Innodb_log_pending_checkpoint_writes', 'Innodb_log_pending_log_writes',
        'Innodb_row_queries_inside', 'Innodb_row_queries_queue',
        'Innodb_trx_history_list_length', 'Innodb_trx_total_lock_structs',
        'Innodb_status_process_time', ]
    _IGNORE_KEYS = [
        'Master_Port', 'Master_Server_Id',
        'Last_Errno', 'Last_IO_Errno', 'Last_SQL_Errno', ]

    innodb_status_keys = {
        'Innodb_bp_total_alloc,Innodb_bp_add_alloc':
        'Total memory allocated (\d+)\; in additional pool allocated (\d+)',
        'Innodb_bp_reads_per_sec,Innodb_bp_created_per_sec,'
        + 'Innodb_bp_written_per_sec':
        '(^\d+.\d+) reads/s, (\d+.\d+) creates/s, (\d+.\d+) writes/s',
        'Innodb_io_ibuf_reads,Innodb_io_ibuf_logs,Innodb_io_ibuf_syncs':
        ' ibuf aio reads: (\d+), log i/o\'s: (\d+), sync i/o\'s: (\d+)',
        'Innodb_log_pending_log_writes,Innodb_log_pending_checkpoint_writes':
        '(\d+) pending log writes, (\d+) pending chkp writes',
        'Innodb_hash_searches_per_sec,Innodb_non_hash_searches_per_sec':
        '(\d+.\d+) hash searches/s, (\d+.\d+) non-hash searches/s',
        'Innodb_row_queries_inside,Innodb_row_queries_queue':
        '(\d+) queries inside InnoDB, (\d+) queries in queue',
        'Innodb_trx_total_lock_structs':
        '(\d+) lock struct\(s\), heap size (\d+), (\d+) row lock\(s\), undo'
        + ' log entries (\d+)',
        'Innodb_log_io_total,Innodb_log_io_per_sec':
        '(\d+) log i\/o\'s done, (\d+.\d+) log i\/o\'s\/second',
        'Innodb_io_os_file_reads,Innodb_io_os_file_writes,'
        + 'Innodb_io_os_file_fsyncs':
        '(\d+) OS file reads, (\d+) OS file writes, (\d+) OS fsyncs',
        'Innodb_rows_inserted_per_sec,Innodb_rows_updated_per_sec,'
        + 'Innodb_rows_deleted_per_sec,Innodb_rows_read_per_sec':
        '(\d+.\d+) inserts\/s, (\d+.\d+) updates\/s, (\d+.\d+) deletes\/s, '
        + '(\d+.\d+) reads\/s',
        'Innodb_reads_per_sec,Innodb_bytes_per_read,Innodb_io_syncs_per_sec,'
        + 'Innodb_writes_per_sec':
        '(\d+.\d+) reads\/s, (\d+) avg bytes\/read, (\d+.\d+) writes\/s, '
        + '(\d+.\d+) fsyncs\/s',
        'Innodb_bp_pages_young_per_sec,Innodb_bp_pages_not_young_per_sec':
        '(\d+.\d+) youngs\/s, (\d+.\d+) non-youngs\/s',
        'Innodb_bp_hit_rate,Innodb_bp_young_hit_rate,'
        + 'Innodb_bp_not_young_hit_rate':
        'Buffer pool hit rate (\d+) \/ \d+, young-making rate (\d+) \/ \d+ '
        + 'not (\d+) \/ \d+',
        'Innodb_bp_size':
        'Buffer pool size   (\d+)',
        'Innodb_bp_db_pages':
        'Database pages     (\d+)',
        'Innodb_bp_dictionary_alloc':
        'Dictionary memory allocated (\d+)',
        'Innodb_bp_free_buffers':
        'Free buffers       (\d+)',
        'Innodb_hash_table_size,Innodb_hash_node_heap':
        'Hash table size (\d+), node heap has (\d+) buffer\(s\)',
        'Innodb_trx_history_list_length':
        'History list length (\d+)',
        'Innodb_bp_io_sum_pages,Innodb_bp_io_cur_pages,'
        + 'Innodb_bp_io_unzip_sum_pages,Innodb_bp_io_unzip_cur_pages':
        'I\/O sum\[(\d+)\]:cur\[(\d+)\], unzip sum\[(\d+)\]:cur\[(\d+)\]',
        'Innodb_ibuf_size,Innodb_ibuf_free_list_len,Innodb_ibuf_seg_size,'
        + 'Innodb_ibuf_merges':
        'Ibuf: size (\d+), free list len (\d+), seg size (\d+), (\d+) '
        + 'merges',
        'Innodb_bp_lru_len,Innodb_bp_unzip_lru_len':
        'LRU len: (\d+), unzip_LRU len: (\d+)',
        'Innodb_bp_modified_pages':
        'Modified db pages  (\d+)',
        'Innodb_sem_mutex_spin_waits,Innodb_sem_mutex_rounds,'
        + 'Innodb_sem_mutex_os_waits':
        'Mutex spin waits (\d+), rounds (\d+), OS waits (\d+)',
        'Innodb_rows_inserted,Innodb_rows_updated,Innodb_rows_deleted,'
        + 'Innodb_rows_read':
        'Number of rows inserted (\d+), updated (\d+), deleted (\d+), '
        + 'read (\d+)',
        'Innodb_bp_old_db_pages':
        'Old database pages (\d+)',
        'Innodb_sem_os_reservation_count,Innodb_sem_os_signal_count':
        'OS WAIT ARRAY INFO: reservation count (\d+), signal count (\d+)',
        'Innodb_bp_pages_young,Innodb_bp_pages_not_young':
        'Pages made young (\d+), not young (\d+)',
        'Innodb_bp_pages_read,Innodb_bp_pages_created,Innodb_bp_pages_written':
        'Pages read (\d+), created (\d+), written (\d+)',
        'Innodb_bp_pages_read_ahead_per_sec,'
        + 'Innodb_bp_pages_evicted_no_access_per_sec,'
        + 'Innodb_status_bp_pages_random_read_ahead':
        'Pages read ahead (\d+.\d+)/s, evicted without access (\d+.\d+)\/s,'
        + ' Random read ahead (\d+.\d+)/s',
        'Innodb_io_pending_flush_log,Innodb_io_pending_flush_bp':
        'Pending flushes \(fsync\) log: (\d+); buffer pool: (\d+)',
        'Innodb_io_pending_reads,Innodb_io_pending_writes':
        'Pending normal aio reads: (\d+) \[\d+, \d+, \d+, \d+\], aio '
        + 'writes: (\d+) \[\d+, \d+, \d+, \d+\]',
        'Innodb_bp_pending_writes_lru,Innodb_bp_pending_writes_flush_list,'
        + 'Innodb_bp_pending_writes_single_page':
        'Pending writes: LRU (\d+), flush list (\d+), single page (\d+)',
        'Innodb_per_sec_avg':
        'Per second averages calculated from the last (\d+) seconds',
        'Innodb_sem_rw_excl_spins,Innodb_sem_rw_excl_rounds,'
        + 'Innodb_sem_rw_excl_os_waits':
        'RW-excl spins (\d+), rounds (\d+), OS waits (\d+)',
        'Innodb_sem_shared_spins,Innodb_sem_shared_rounds,'
        + 'Innodb_sem_shared_os_waits':
        'RW-shared spins (\d+), rounds (\d+), OS waits (\d+)',
        'Innodb_sem_spins_per_wait_mutex,Innodb_sem_spins_per_wait_rw_shared,'
        + 'Innodb_sem_spins_per_wait_rw_excl':
        'Spin rounds per wait: (\d+.\d+) mutex, (\d+.\d+) RW-shared, '
        + '(\d+.\d+) RW-excl',
        'Innodb_main_thd_log_flush_writes':
        'srv_master_thread log flush and writes: (\d+)',
        'Innodb_main_thd_loops_one_sec,Innodb_main_thd_loops_sleeps,'
        + 'Innodb_main_thd_loops_ten_sec,Innodb_main_thd_loops_background,'
        + 'Innodb_main_thd_loops_flush':
        'srv_master_thread loops: (\d+) 1_second, (\d+) sleeps, (\d+) '
        + '10_second, (\d+) background, (\d+) flush',
        'Innodb_ibuf_inserts,Innodb_ibuf_merged_recs,Innodb_ibuf_merges':
        '(\d+) inserts, (\d+) merged recs, (\d+) merges',
    }
    innodb_status_match = {}

    def __init__(self, *args, **kwargs):
        super(MySQLCollector, self).__init__(*args, **kwargs)
        for key in self.innodb_status_keys:
            self.innodb_status_keys[key] = re.compile(
                self.innodb_status_keys[key])

    def get_default_config_help(self):
        config_help = super(MySQLCollector, self).get_default_config_help()
        config_help.update({
            'host': 'Hostname',
            'port': 'Port',
            'db': 'Database',
            'user': 'Username',
            'passwd': 'Password',
            'publish': "Which rows of '[SHOW GLOBAL STATUS](http://dev.mysql."
                       + "com/doc/refman/5.1/en/show-status.html)' you would "
                       + "like to publish. Leave unset to publish all",
            'slave': 'Collect SHOW SLAVE STATUS',
            'master': 'Collect SHOW MASTER STATUS',
            'innodb': 'Collect SHOW ENGINE INNODB STATUS',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MySQLCollector, self).get_default_config()
        config.update({
            'path':     'mysql',
            # Connection settings
            'host':     'localhost',
            'port':     3306,
            'db':       'yourdatabase',
            'user':     'yourusername',
            'passwd':   'yourpassword',

            # Which rows of 'SHOW GLOBAL STATUS' you would like to publish.
            # http://dev.mysql.com/doc/refman/5.1/en/show-status.html
            # Leave unset to publish all
            #'publish': '',

            'slave':    'False',
            'master':   'False',
            'innodb':   'False',
        })
        return config

    def get_stats(self):
        params = {}
        metrics = {}

        if MySQLdb is None:
            self.log.error('Unable to import MySQLdb')
            return {}

        params['host'] = self.config['host']
        params['port'] = int(self.config['port'])
        params['db'] = self.config['db']
        params['user'] = self.config['user']
        params['passwd'] = self.config['passwd']

        try:
            db = MySQLdb.connect(**params)
        except MySQLError, e:
            self.log.error('MySQLCollector couldnt connect to database %s', e)
            return {}

        self.log.info('MySQLCollector: Connected to database.')

        cursor = db.cursor()

        cursor.execute('SHOW GLOBAL STATUS')
        metrics['status'] = dict(cursor.fetchall())
        for key in metrics['status']:
            try:
                metrics[key] = float(metrics['status'][key])
            except:
                pass

        if self.config['master'] == 'True':
            cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            cursor.execute('SHOW MASTER STATUS')
            try:
                row_master = cursor.fetchone()
                for key, value in row_master.items():
                    if key in self._IGNORE_KEYS:
                        continue
                    try:
                        metrics[key] = float(row_master[key])
                    except:
                        pass
            except:
                self.log.error('MySQLCollector: Couldnt get master status')
                pass

        if self.config['slave'] == 'True':
            cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            cursor.execute('SHOW SLAVE STATUS')
            try:
                row_slave = cursor.fetchone()
                for key, value in row_slave.items():
                    if key in self._IGNORE_KEYS:
                        continue
                    try:
                        metrics[key] = float(row_slave[key])
                    except:
                        pass
            except:
                self.log.error('MySQLCollector: Couldnt get slave status')
                pass

        if self.config['innodb'] == 'True':
            innodb_status_timer = time.time()
            cursor = db.cursor()
            try:
                cursor.execute('SHOW ENGINE INNODB STATUS')

                innodb_status_output = cursor.fetchone()

                todo = self.innodb_status_keys.keys()
                for line in innodb_status_output[2].split('\n'):
                    for key in todo:
                        match = self.innodb_status_keys[key].match(line)
                        if match is not None:
                            todo.remove(key)
                            match_index = 1
                            for key_index in key.split(','):
                                try:
                                    value = float(match.group(match_index))
                                    # store value
                                    if key_index in metrics:
                                        self.log.debug("MySQLCollector: %s"
                                                       + " already defined, "
                                                       + " ignoring new value",
                                                       key_index)
                                    else:
                                        metrics[key_index] = value
                                    match_index += 1
                                except IndexError:
                                    self.log.debug("MySQLCollector: Cannot find"
                                                   + " value in innodb status"
                                                   + "for %s", key_index)
                for key in todo:
                    self.log.error("MySQLCollector: %s regexp not matched in"
                                   + "innodb status", key)
            except Exception, innodb_status_error:
                self.log.error('MySQLCollector: Couldnt get engine innodb'
                               + 'status, check user permissions: %s',
                               innodb_status_error)
            Innodb_status_process_time = time.time() - innodb_status_timer
            self.log.debug("MySQLCollector: innodb status process time: %f",
                           Innodb_status_process_time)
            metrics["Innodb_status_process_time"] = Innodb_status_process_time

        db.close()

        return metrics

    def collect(self):
        metrics = self.get_stats()

        for metric_name in metrics:
            metric_value = metrics[metric_name]

            if type(metric_value) is not float:
                continue

            if ('publish' not in self.config
                    or metric_name in self.config['publish']):
                if metric_name not in self._GAUGE_KEYS:
                    metric_value = self.derivative(metric_name, metric_value)
                    # All these values are incrementing counters, so if we've
                    # gone negative then someone's restarted mysqld and reset
                    # all the counters. Best not record a massive negative
                    # number. Skip this value.
                    if metric_value < 0:
                        continue
                self.publish(metric_name, metric_value)
            else:
                for k in self.config['publish'].split():
                    if k not in metrics:
                        self.log.error("No such key '%s' available, issue 'show"
                                       + "global status' for a full list", k)
                    else:
                        self.publish(k, metrics[k])
