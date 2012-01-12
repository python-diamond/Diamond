import MySQLdb
from MySQLdb import MySQLError
import diamond
import re

class MySQLCollector(diamond.collector.Collector):

    REPLACEMENTS = [
        ('Aborted_',                    'Aborted.'),
        ('Binlog_cache_',               'Binlog.cache.'),
        ('Binlog_stmt_',                'Binlog.stmt.'),
        ('Com_alter_',                  'Com.alter.'),
        ('Com_create_',                 'Com.create.'),
        ('Com_drop_',                   'Com.drop.'),
        ('Com_show_',                   'Com.show.'),
        ('Com_slave_',                  'Com.slave.'),
        ('Com_stmt_',                   'Com.stmt.'),
        ('Com_xa_',                     'Com.xa.'),
        ('Com_',                        'Com.'),
        ('Created_tmp_',                'Created_tmp.'),
        ('Delayed_',                    'Delayed.'),
        ('Handler_',                    'Handler.'),
        ('Innodb_adaptive_hash_',       'Innodb.adaptive_hash.'),
        ('Innodb_buffer_pool_pages_',   'Innodb.buffer_pool.pages.'),
        ('Innodb_buffer_pool_',         'Innodb.buffer_pool.'),
        ('Innodb_checkpoint_',          'Innodb.checkpoint.'),
        ('Innodb_data_',                'Innodb.data.'),
        ('Innodb_dblwr_',               'Innodb.dblwr.'),
        ('Innodb_ibuf_',                'Innodb.ibuf.'),
        ('Innodb_log_',                 'Innodb.log.'),
        ('Innodb_os_log_',              'Innodb.log.os.'),
        ('Innodb_lsn_',                 'Innodb.lsn.'),
        ('Innodb_master_thread_',       'Innodb.master_thread.'),
        ('Innodb_mem_',                 'Innodb.mem.'),
        ('Innodb_mutex_',               'Innodb.mutex.'),
        ('Innodb_pages_',               'Innodb.pages.'),
        ('Innodb_purge_',               'Innodb.purge.'),
        ('Innodb_row_lock_',            'Innodb.row_lock.'),
        ('Innodb_rows_',                'Innodb.rows.'),
        ('Innodb_s_lock_',              'Innodb.s_lock.'),
        ('Innodb_x_lock_',              'Innodb.x_lock.'),
        ('Innodb_',                     'Innodb.'),
        ('key_blocks_',                 'Key.Buffer.'),
        ('Key_blocks_',                 'Key.Buffer.'),
        ('Key_',                        'Key.'),
        ('Open_',                       'Open.'),
        ('Opened_',                     'Opened.'),
        ('Performance_schema_',         'Performance_schema.'),
        ('Qcache_',                     'Qcache.'),
        ('Select_',                     'Select.'),
        ('Slave_',                      'Slave.'),
        ('Sort_',                       'Sort.'),
        ('Ssl_',                        'Ssl.'),
        ('Table_locks_',                'Table_locks.'),
        ('Tc_log_',                     'Tc_log.'),
        ('Threads_',                    'Threads.'),
        ('binlog_',                     'binlog.'),
        ('max_used_connections',        'Connection.max_used'),
    ]

    def get_stats(self):
        params = {}
        stats = {}

        params['host']   = self.config['host']
        params['port']   = int(self.config['port'])
        params['db']     = self.config['db']
        params['user']   = self.config['user']
        params['passwd'] = self.config['passwd']

        try:
            db = MySQLdb.connect(**params)
        except MySQLError, e:
            self.log.error('Couldnt connect to database %s', e)
            return {}

        self.log.info('Connected to database.')

        cursor = db.cursor()

        cursor.execute('SHOW GLOBAL STATUS')
        stats['status'] = dict(cursor.fetchall())
        for key in stats['status']:
            try:
                stats['status'][key] = float(stats['status'][key])
            except:
                pass

        cursor.execute('SHOW GLOBAL VARIABLES')
        stats['variables'] = dict(cursor.fetchall())
        for key in stats['variables']:
            try:
                stats['variables'][key] = float(stats['variables'][key])
            except:
                pass

        db.close()

        return stats

    def collect(self):
        stats = self.get_stats()
        metrics = {}

        for metric_name in stats['status']:
            metric_value = stats['status'][metric_name]
            if type(metric_value) is not float:
                continue

            if 'publish' not in self.config:
                # Muck the keys to be more graphite friendly
                for replacement in self.REPLACEMENTS:
                    metric_name = re.sub('(?i)' + re.escape(replacement[0]), replacement[1], metric_name)

            metric_value = self.derivative(metric_name, metric_value)
            metrics[metric_name] = metric_value;

        if 'publish' not in self.config:
            # Build any extra stats here

            # http://themattreid.com/wordpress/2009/04/28/a-quick-rundown-of-per-thread-buffers/
            metrics['Connection.max_memory_per'] = stats['variables']['read_buffer_size']     \
                                                 + stats['variables']['read_rnd_buffer_size'] \
                                                 + stats['variables']['sort_buffer_size']     \
                                                 + stats['variables']['thread_stack']         \
                                                 + stats['variables']['join_buffer_size']     \
                                                 + stats['variables']['binlog_cache_size']
            metrics['Connection.max_connections'] = stats['variables']['max_connections']
            metrics['Connection.max_memory'] = metrics['Connection.max_memory_per'] * metrics['Connection.max_connections']

            metrics['Innodb.buffer_pool.total_size'] = stats['variables']['innodb_buffer_pool_size']         \
                                                     + stats['variables']['innodb_additional_mem_pool_size'] \
                                                     + stats['variables']['innodb_log_buffer_size']          \
                                                     + stats['variables']['key_buffer_size']                 \
                                                     + stats['variables']['query_cache_size']
            if metrics['Connections'] > 1:
                metrics['Connection.thread_cache_miss_rate'] = metrics['Threads.created'] / metrics['Connections']
            metrics['Connection.max'] = stats['variables']['max_connections']
            metrics['Key_Buffer.unused_bytes'] = metrics['Key.Buffer.unused'] * stats['variables']['key_cache_block_size']
            metrics['Key_Buffer.used_bytes'] = metrics['Key.Buffer.used'] * stats['variables']['key_cache_block_size']

        if 'publish' not in self.config:
            for key in metrics:
                self.publish(key, metrics[key])
        else:
            for k in self.config['publish'].split():
                if not metrics.has_key(k):
                    self.log.error("No such key '%s' available, issue 'show global status' for a full list", k)
                else:
                    self.publish(k, metrics[k])
