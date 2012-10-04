# coding=utf-8

"""

Diamond collector that monitors relevant MySQL performance_schema values
For now only monitors replication load

[Blog](http://bit.ly/PbSkbN) announcement.

[Sniplet](http://bit.ly/SHwYhT) to build example graph.

#### Dependencies

 * MySQLdb
 * MySQL 5.5.3+

"""

from __future__ import division

try:
    import MySQLdb
    from MySQLdb import MySQLError
except ImportError:
    MySQLdb = None
import diamond
import time


class MySQLPerfCollector(diamond.collector.Collector):

    def __init__(self, *args, **kwargs):
        super(MySQLPerfCollector, self).__init__(*args, **kwargs)
        self.db = None
        self.cursor = None
        self.connect()
        self.last_wait_count = {}
        self.last_wait_sum = {}
        self.last_timestamp = {}
        self.last_data = {}
        self.monitors = {
            'slave_sql': {
                'wait/synch/cond/sql/MYSQL_RELAY_LOG::update_cond':
                'wait_for_update',
                'wait/io/file/innodb/innodb_data_file':
                'innodb_data_file',
                'wait/io/file/innodb/innodb_log_file':
                'innodb_log_file',
                'wait/io/file/myisam/dfile':
                'myisam_dfile',
                'wait/io/file/myisam/kfile':
                'myisam_kfile',
                'wait/io/file/sql/binlog':
                'binlog',
                'wait/io/file/sql/relay_log_info':
                'relaylog_info',
                'wait/io/file/sql/relaylog':
                'relaylog',
                'wait/synch/mutex/innodb':
                'innodb_mutex',
                'wait/synch/mutex':
                'other_mutex',
                'wait/synch/rwlock':
                'rwlocks',
                'wait/io':
                'other_io',
            },
            'slave_io': {
                'wait/io/file/sql/relaylog_index':
                'relaylog_index',
                'wait/synch/mutex/sql/MYSQL_RELAY_LOG::LOCK_index':
                'relaylog_index_lock',
                'wait/synch/mutex/sql/Master_info::data_lock':
                'master_info_lock',
                'wait/synch/mutex/mysys/IO_CACHE::append_buffer_lock':
                'append_buffer_lock',
                'wait/synch/mutex/sql/LOG::LOCK_log':
                'log_lock',
                'wait/io/file/sql/master_info':
                'master_info',
                'wait/io/file/sql/relaylog':
                'relaylog',
                'wait/synch/mutex':
                'other_mutex',
                'wait/synch/rwlock':
                'rwlocks',
                'wait/io':
                'other_io',
            }
        }

    def get_default_config_help(self):
        config_help = super(MySQLPerfCollector, self).get_default_config_help()
        config_help.update({
            'host': 'Hostname',
            'port': 'Port',
            'db': 'Database',
            'user': 'Username',
            'passwd': 'Password',
            'slave': 'Collect Slave Replication Metrics',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MySQLPerfCollector, self).get_default_config()
        config.update({
            'path':     'mysql',
            # Connection settings
            'host':     'localhost',
            'port':     3306,
            'db':       'performance_schema',
            'user':     'yourusername',
            'passwd':   'yourpassword',

            'slave':    'False',
        })
        return config

    def connect(self):
        if MySQLdb is None:
            self.log.error('Unable to import MySQLdb')
            return

        params = {}
        params['host'] = self.config['host']
        params['port'] = int(self.config['port'])
        params['db'] = self.config['db']
        params['user'] = self.config['user']
        params['passwd'] = self.config['passwd']

        try:
            self.db = MySQLdb.connect(**params)
        except MySQLError, e:
            self.log.error('MySQLPerfCollector couldnt connect to database %s',
                           e)
            return {}

        self.log.info('MySQLPerfCollector: Connected to database.')

    def slave_load(self, thread):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT
                his.event_name,
                his.sum_timer_wait,
                his.count_star,
                cur.event_name,
                UNIX_TIMESTAMP(SYSDATE())
            FROM
                events_waits_summary_by_thread_by_event_name his
                JOIN threads thr USING (thread_id)
                JOIN events_waits_current cur USING (thread_id)
            WHERE
                name = %s
            ORDER BY
                his.event_name
            """, (thread,))

        data = list(cursor.fetchall())
        wait_sum = sum([x[1] for x in data])
        wait_count = sum([x[2] for x in data])
        timestamp = int(time.time())
        
        if 0 in data and len(data[0]) > 5:
            cur_event_name, timestamp = data[0][3:]

        if thread not in self.last_wait_sum:
            # Avoid bogus data
            self.last_wait_sum[thread] = wait_sum
            self.last_wait_count[thread] = wait_count
            self.last_timestamp[thread] = timestamp
            self.last_data[thread] = data
            return

        wait_delta = wait_sum - self.last_wait_sum[thread]
        time_delta = (timestamp - self.last_timestamp[thread]) * 1000000000000

        # Summarize a few things
        thread_name = thread[thread.rfind('/') + 1:]
        data.append(['wait/synch/mutex/innodb',
                     sum([x[1] for x in data if x[0].startswith(
                         'wait/synch/mutex/innodb')])])
        data.append(['wait/synch/mutex',
                     sum([x[1] for x in data if x[0].startswith(
                         'wait/synch/mutex')
                         and x[0] not in self.monitors[thread_name]])
                     - data[-1][1]])
        data.append(['wait/synch/rwlock',
                     sum([x[1] for x in data if x[0].startswith(
                         'wait/synch/rwlock')])])
        data.append(['wait/io',
                     sum([x[1] for x in data if x[0].startswith(
                         'wait/io')
                         and x[0] not in self.monitors[thread_name]])])

        for d in zip(self.last_data[thread], data):
            if d[0][0] in self.monitors[thread_name]:
                self.publish(thread_name + '.'
                             + self.monitors[thread_name][d[0][0]],
                             (d[1][1] - d[0][1]) / time_delta * 100)

        # Also log what's unaccounted for. This is where Actual Work gets done
        self.publish(thread_name + '.other_work',
                     float(time_delta - wait_delta) / time_delta * 100)

        self.last_wait_sum[thread] = wait_sum
        self.last_wait_count[thread] = wait_count
        self.last_timestamp[thread] = timestamp
        self.last_data[thread] = data

    def collect(self):
        if self.config['slave']:
            try:
                self.slave_load('thread/sql/slave_io')
                self.slave_load('thread/sql/slave_sql')
            except MySQLdb.OperationalError:
                self.connect()
                self.slave_load('thread/sql/slave_io')
                self.slave_load('thread/sql/slave_sql')
