# coding=utf-8

"""
Collect metrics from postgresql

#### Dependencies

 * psycopg2

"""

import diamond.collector
from diamond.collector import str_to_bool

try:
    import psycopg2
    import psycopg2.extras
    psycopg2  # workaround for pyflakes issue #13
except ImportError:
    psycopg2 = None


class PostgresqlCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(PostgresqlCollector, self).get_default_config_help()
        config_help.update({
            'host': 'Hostname',
            'user': 'Username',
            'password': 'Password',
            'port': 'Port number',
            'underscore': 'Convert _ to .',
            'extended': 'Enable collection of extended database stats.',
            'metrics': 'List of enabled metrics to collect'
        })
        return config_help

    def get_default_config(self):
        """
        Return default config.
        """
        config = super(PostgresqlCollector, self).get_default_config()
        config.update({
            'path': 'postgres',
            'host': 'localhost',
            'user': 'postgres',
            'password': 'postgres',
            'port': 5432,
            'underscore': False,
            'extended': False,
            'method': 'Threaded',
            'metrics': []
        })
        return config

    def collect(self):
        if psycopg2 is None:
            self.log.error('Unable to import module psycopg2')
            return {}

        # Create database-specific connections
        self.connections = {}
        for db in self._get_db_names():
            self.connections[db] = self._connect(database=db)

        if self.config['metrics']:
            metrics = self.config['metrics']
        elif str_to_bool(self.config['extended']):
            metrics = registry['extended']
        else:
            metrics = registry['basic']

        # Iterate every QueryStats class
        for metric_name in set(metrics):
            if metric_name not in metrics_registry:
                continue
            klass = metrics_registry[metric_name]
            stat = klass(self.connections, underscore=self.config['underscore'])
            stat.fetch()
            for metric, value in stat:
                if value is not None:
                    self.publish(metric, value)

        # Cleanup
        [conn.close() for conn in self.connections.itervalues()]

    def _get_db_names(self):
        query = """
            SELECT datname FROM pg_database
            WHERE datallowconn AND NOT datistemplate
            AND NOT datname='postgres' ORDER BY 1
        """
        conn = self._connect()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query)
        datnames = [d['datname'] for d in cursor.fetchall()]
        conn.close()

        # Exclude `postgres` database list, unless it is the
        # only database available (required for querying pg_stat_database)
        if not datnames:
            datnames = ['postgres']
        return datnames

    def _connect(self, database=None):
        conn_args = {
          'host': self.config['host'],
          'user': self.config['user'],
          'password': self.config['password'],
          'port': self.config['port']
        }

        if database:
            conn_args['database'] = database
        else:
            conn_args['database'] = 'postgres'

        conn = psycopg2.connect(**conn_args)

        # Avoid using transactions, set isolation level to autocommit
        conn.set_isolation_level(0)
        return conn


class QueryStats(object):
    def __init__(self, conns, parameters=None, underscore=False):
        self.connections = conns
        self.underscore = underscore
        self.parameters = parameters

    def _translate_datname(self, db):
        if self.underscore:
            db = db.replace("_", ".")
        return db

    def fetch(self):
        self.data = list()

        for db, conn in self.connections.iteritems():
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(self.query, self.parameters)

            for row in cursor.fetchall():
                # If row is length 2, assume col1, col2 forms key: value
                if len(row) == 2:
                    self.data.append({
                        'datname': self._translate_datname(db),
                        'metric': row[0],
                        'value': row[1],
                    })

                # If row > length 2, assume each column name maps to
                # key => value
                else:
                    for key, value in row.iteritems():
                        if key in ('datname', 'schemaname', 'relname',
                                   'indexrelname',):
                            continue

                        self.data.append({
                            'datname': self._translate_datname(row.get(
                                'datname', db)),
                            'schemaname': row.get('schemaname', None),
                            'relname': row.get('relname', None),
                            'indexrelname': row.get('indexrelname', None),
                            'metric': key,
                            'value': value,
                        })

            # Setting multi_db to True will run this query on all known
            # databases. This is bad for queries that hit views like
            # pg_database, which are shared across databases.
            #
            # If multi_db is False, bail early after the first query
            # iteration. Otherwise, continue to remaining databases.
            if not self.multi_db:
                break

    def __iter__(self):
        for data_point in self.data:
            yield (self.path % data_point, data_point['value'])


class DatabaseStats(QueryStats):
    """
    Database-level summary stats
    """
    path = "database.%(datname)s.%(metric)s"
    multi_db = False
    query = """
        SELECT pg_stat_database.datname as datname,
               pg_stat_database.numbackends as numbackends,
               pg_stat_database.xact_commit as xact_commit,
               pg_stat_database.xact_rollback as xact_rollback,
               pg_stat_database.blks_read as blks_read,
               pg_stat_database.blks_hit as blks_hit,
               pg_stat_database.tup_returned as tup_returned,
               pg_stat_database.tup_fetched as tup_fetched,
               pg_stat_database.tup_inserted as tup_inserted,
               pg_stat_database.tup_updated as tup_updated,
               pg_stat_database.tup_deleted as tup_deleted,
               pg_database_size(pg_database.datname) AS size
        FROM pg_database
        JOIN pg_stat_database
        ON pg_database.datname = pg_stat_database.datname
        WHERE pg_stat_database.datname
        NOT IN ('template0','template1','postgres')
    """


class UserTableStats(QueryStats):
    path = "%(datname)s.tables.%(schemaname)s.%(relname)s.%(metric)s"
    multi_db = True
    query = """
        SELECT relname,
               schemaname,
               seq_scan,
               seq_tup_read,
               idx_scan,
               idx_tup_fetch,
               n_tup_ins,
               n_tup_upd,
               n_tup_del,
               n_tup_hot_upd,
               n_live_tup,
               n_dead_tup
        FROM pg_stat_user_tables
    """


class UserIndexStats(QueryStats):
    path = "%(datname)s.indexes.%(schemaname)s.%(relname)s." \
           "%(indexrelname)s.%(metric)s"
    multi_db = True
    query = """
        SELECT relname,
               schemaname,
               indexrelname,
               idx_scan,
               idx_tup_read,
               idx_tup_fetch
        FROM pg_stat_user_indexes
    """


class UserTableIOStats(QueryStats):
    path = "%(datname)s.tables.%(schemaname)s.%(relname)s.%(metric)s"
    multi_db = True
    query = """
        SELECT relname,
               schemaname,
               heap_blks_read,
               heap_blks_hit,
               idx_blks_read,
               idx_blks_hit
        FROM pg_statio_user_tables
    """


class UserIndexIOStats(QueryStats):
    path = "%(datname)s.indexes.%(schemaname)s.%(relname)s." \
           "%(indexrelname)s.%(metric)s"
    multi_db = True
    query = """
        SELECT relname,
               schemaname,
               indexrelname,
               idx_blks_read,
               idx_blks_hit
        FROM pg_statio_user_indexes
    """


class ConnectionStateStats(QueryStats):
    path = "%(datname)s.connections.%(metric)s"
    multi_db = True
    query = """
        SELECT tmp.state AS key,COALESCE(count,0) FROM
               (VALUES ('active'),
                       ('waiting'),
                       ('idle'),
                       ('idletransaction'),
                       ('unknown')
                ) AS tmp(state)
        LEFT JOIN
             (SELECT CASE WHEN waiting THEN 'waiting'
                          WHEN current_query='<IDLE>' THEN 'idle'
                          WHEN current_query='<IDLE> in transaction'
                              THEN 'idletransaction'
                          WHEN current_query='<insufficient privilege>'
                              THEN 'unknown'
                          ELSE 'active' END AS state,
                     count(*) AS count
               FROM pg_stat_activity
               WHERE procpid != pg_backend_pid()
               GROUP BY CASE WHEN waiting THEN 'waiting'
                             WHEN current_query='<IDLE>' THEN 'idle'
                             WHEN current_query='<IDLE> in transaction'
                                 THEN 'idletransaction'
                             WHEN current_query='<insufficient privilege>'
                                 THEN 'unknown' ELSE 'active' END
             ) AS tmp2
        ON tmp.state=tmp2.state ORDER BY 1
    """


class LockStats(QueryStats):
    path = "%(datname)s.locks.%(metric)s"
    multi_db = False
    query = """
        SELECT lower(mode) AS key,
               count(*) AS value
        FROM pg_locks
        WHERE database IS NOT NULL
        GROUP BY mode ORDER BY 1
    """


class RelationSizeStats(QueryStats):
    path = "%(datname)s.sizes.%(schemaname)s.%(relname)s.%(metric)s"
    multi_db = True
    query = """
        SELECT pg_class.relname,
               pg_namespace.nspname as schemaname,
               pg_relation_size(pg_class.oid) as relsize
        FROM pg_class
        INNER JOIN
          pg_namespace
        ON pg_namespace.oid = pg_class.relnamespace
        WHERE reltype != 0
        AND relkind != 'S'
        AND nspname NOT IN ('pg_catalog', 'information_schema')
    """


class BackgroundWriterStats(QueryStats):
    path = "bgwriter.%(metric)s"
    multi_db = False
    query = """
        SELECT checkpoints_timed,
               checkpoints_req,
               buffers_checkpoint,
               buffers_clean,
               maxwritten_clean,
               buffers_backend,
               buffers_alloc
        FROM pg_stat_bgwriter
    """


class WalSegmentStats(QueryStats):
    path = "wals.%(metric)s"
    multi_db = False
    query = """
        SELECT count(*) AS segments
        FROM pg_ls_dir('pg_xlog') t(fn)
        WHERE fn ~ '^[0-9A-Z]{24}\$'
    """


class TransactionCount(QueryStats):
    path = "transactions.%(metric)s"
    multi_db = False
    query = """
        SELECT 'commit' AS type,
               sum(pg_stat_get_db_xact_commit(oid))
        FROM pg_database
        UNION ALL
        SELECT 'rollback',
               sum(pg_stat_get_db_xact_rollback(oid))
        FROM pg_database
    """


class IdleInTransactions(QueryStats):
    path = "%(datname)s.longest_running.%(metric)s"
    multi_db = True
    query = """
        SELECT 'idle_in_transaction',
               max(COALESCE(ROUND(EXTRACT(epoch FROM now()-query_start)),0))
                   AS idle_in_transaction
        FROM pg_stat_activity
        WHERE current_query = '<IDLE> in transaction'
        GROUP BY 1
    """


class LongestRunningQueries(QueryStats):
    path = "%(datname)s.longest_running.%(metric)s"
    multi_db = True
    query = """
        SELECT 'query',
            COALESCE(max(extract(epoch FROM CURRENT_TIMESTAMP-query_start)),0)
        FROM pg_stat_activity
        WHERE current_query NOT LIKE '<IDLE%'
        UNION ALL
        SELECT 'transaction',
            COALESCE(max(extract(epoch FROM CURRENT_TIMESTAMP-xact_start)),0)
        FROM pg_stat_activity
        WHERE 1=1
    """


class UserConnectionCount(QueryStats):
    path = "%(datname)s.user_connections.%(metric)s"
    multi_db = True
    query = """
        SELECT usename,
               count(*) as count
        FROM pg_stat_activity
        WHERE procpid != pg_backend_pid()
        GROUP BY usename
        ORDER BY 1
    """


class DatabaseConnectionCount(QueryStats):
    path = "database.%(metric)s.connections"
    multi_db = False
    query = """
        SELECT datname,
               count(datname) as connections
        FROM pg_stat_activity
        GROUP BY pg_stat_activity.datname
    """


class TableScanStats(QueryStats):
    path = "%(datname)s.scans.%(metric)s"
    multi_db = True
    query = """
        SELECT 'relname' AS relname,
               COALESCE(sum(seq_scan),0) AS sequential,
               COALESCE(sum(idx_scan),0) AS index
        FROM pg_stat_user_tables
    """


class TupleAccessStats(QueryStats):
    path = "%(datname)s.tuples.%(metric)s"
    multi_db = True
    query = """
        SELECT COALESCE(sum(seq_tup_read),0) AS seqread,
               COALESCE(sum(idx_tup_fetch),0) AS idxfetch,
               COALESCE(sum(n_tup_ins),0) AS inserted,
               COALESCE(sum(n_tup_upd),0) AS updated,
               COALESCE(sum(n_tup_del),0) AS deleted,
               COALESCE(sum(n_tup_hot_upd),0) AS hotupdated
        FROM pg_stat_user_tables
    """


metrics_registry = {
    'DatabaseStats': DatabaseStats,
    'DatabaseConnectionCount': DatabaseConnectionCount,
    'UserTableStats': UserTableStats,
    'UserIndexStats': UserIndexStats,
    'UserTableIOStats': UserTableIOStats,
    'UserIndexIOStats': UserIndexIOStats,
    'ConnectionStateStats': ConnectionStateStats,
    'LockStats': LockStats,
    'RelationSizeStats': RelationSizeStats,
    'BackgroundWriterStats': BackgroundWriterStats,
    'WalSegmentStats': WalSegmentStats,
    'TransactionCount': TransactionCount,
    'IdleInTransactions': IdleInTransactions,
    'LongestRunningQueries': LongestRunningQueries,
    'UserConnectionCount': UserConnectionCount,
    'TableScanStats': TableScanStats,
    'TupleAccessStats': TupleAccessStats,
}

registry = {
    'basic': (
        'DatabaseStats',
        'DatabaseConnectionCount',
    ),
    'extended': (
        'DatabaseStats',
        'DatabaseConnectionCount',
        'UserTableStats',
        'UserIndexStats',
        'UserTableIOStats',
        'UserIndexIOStats',
        'ConnectionStateStats',
        'LockStats',
        'RelationSizeStats',
        'BackgroundWriterStats',
        'WalSegmentStats',
        'TransactionCount',
        'IdleInTransactions',
        'LongestRunningQueries',
        'UserConnectionCount',
        'TableScanStats',
        'TupleAccessStats',
    ),
}
