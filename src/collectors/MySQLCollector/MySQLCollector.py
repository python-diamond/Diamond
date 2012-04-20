try:
    import MySQLdb
    from MySQLdb import MySQLError
except ImportError:
    MySQLdb = None
import diamond
import re

class MySQLCollector(diamond.collector.Collector):

    _GAUGE_KEYS = [
        'Innodb_buffer_pool_pages_data', 'Innodb_buffer_pool_pages_dirty', 'Innodb_buffer_pool_pages_free',
        'Innodb_buffer_pool_pages_misc', 'Innodb_buffer_pool_pages_total',
        'Innodb_data_pending_fsyncs', 'Innodb_data_pending_reads', 'Innodb_data_pending_writes',
        'Innodb_os_log_pending_fsyncs', 'Innodb_os_log_pending_writes',
        'Innodb_page_size',
        'Innodb_row_lock_current_waits', 'Innodb_row_lock_time', 'Innodb_row_lock_time_avg',
        'Innodb_row_lock_time_max', 
        'Key_blocks_unused', 'Last_query_cost', 'Max_used_connections',
        'Open_files', 'Open_streams', 'Open_table_definitions', 'Open_tables',
        'Qcache_free_blocks', 'Qcache_free_memory',
        'Qcache_queries_in_cache', 'Qcache_total_blocks',
        'Threads_cached', 'Threads_connected', 'Threads_created', 'Threads_running',
        ]
    _IGNORE_KEYS = [
        'Master_Port', 'Master_Server_Id',
        'Last_Errno', 'Last_IO_Errno', 'Last_SQL_Errno',
        ]

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
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
            #'publish' : '',

            'slave':    'False',
            'master':   'False',
        }

    def get_stats(self):
        params = {}
        metrics = {}

        if MySQLdb is None:
            self.log.error('Unable to import MySQLdb')
            return {}

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
                self.log.error('Couldnt get master status')
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
                self.log.error('Couldnt get slave status')
                pass

        db.close()

        return metrics

    def collect(self):
        metrics = self.get_stats()

        for metric_name in metrics:
            metric_value = metrics[metric_name]
            
            if type(metric_value) is not float:
                continue
            
            if 'publish' not in self.config or metric_name in self.config['publish']:
                if metric_name not in self._GAUGE_KEYS:
                    metric_value = self.derivative(metric_name, metric_value)
                    #All these values are incrementing counters, so if we've gone negative
                    #then someone's restarted mysqld and reset all the counters. Best not
                    #record a massive negative number. Skip this value.
                    if metric_value < 0:
                        continue
                self.publish(metric_name, metric_value)
            else:
                for k in self.config['publish'].split():
                    if not metrics.has_key(k):
                        self.log.error("No such key '%s' available, issue 'show global status' for a full list", k)
                    else:
                        self.publish(k, metrics[k])
