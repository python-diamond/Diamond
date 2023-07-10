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
except ImportError:
    psycopg2 = None


class PostgresqlVacuumCollector(diamond.collector.Collector):
    """
    PostgreSQL collector class
    """

    def get_default_config(self):
        """
        Return default config.
        """
        config = super(PostgresqlVacuumCollector, self).get_default_config()
        config.update({
            'path': 'postgres-vacuum',
        })
        return config

    def collect(self):
        """
        Do pre-flight checks, get list of db names, collect metrics, publish
        """
        if psycopg2 is None:
            self.log.error('Unable to import module psycopg2')
            return {}

        # Get list of databases
        dbs = self._get_db_names()
        if len(dbs) == 0:
            self.log.error("I have 0 databases!")
            return {}

        if self.config['metrics']:
            metrics = self.config['metrics']
        elif str_to_bool(self.config['extended']):
            metrics = registry['extended']
            if str_to_bool(self.config['has_admin']) \
                    and 'WalSegmentStats' not in metrics:
                metrics.append('WalSegmentStats')

        else:
            metrics = registry['basic']

        # Iterate every QueryStats class
        for metric_name in set(metrics):
            if metric_name not in metrics_registry:
                self.log.error(
                    'metric_name %s not found in metric registry' % metric_name)
                continue

            for dbase in dbs:
                conn = self._connect(database=dbase)
                try:
                    klass = metrics_registry[metric_name]
                    stat = klass(dbase, conn,
                                 underscore=self.config['underscore'])
                    stat.fetch(self.config['pg_version'])
                    for metric, value in stat:
                        if value is not None:
                            self.publish(metric, value)

                    # Setting multi_db to True will run this query on all known
                    # databases. This is bad for queries that hit views like
                    # pg_database, which are shared across databases.
                    #
                    # If multi_db is False, bail early after the first query
                    # iteration. Otherwise, continue to remaining databases.
                    if stat.multi_db is False:
                        break
                finally:
                    conn.close()

    def _get_db_names(self):
        """
        Try to get a list of db names
        """
        query = """
            SELECT datname FROM pg_database
            WHERE datallowconn AND NOT datistemplate
            AND NOT datname='postgres' AND NOT datname='rdsadmin' ORDER BY 1
        """
        conn = self._connect(self.config['dbname'])
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
        """
        Connect to given database
        """
        conn_args = {
            'host': self.config['host'],
            'user': self.config['user'],
            'password': self.config['password'],
            'port': self.config['port'],
            'sslmode': self.config['sslmode'],
        }

        if database:
            conn_args['database'] = database
        else:
            conn_args['database'] = 'postgres'

        # libpq will use ~/.pgpass only if no password supplied
        if self.config['password_provider'] == 'pgpass':
            del conn_args['password']

        try:
            conn = psycopg2.connect(**conn_args)
        except Exception as e:
            self.log.error(e)
            raise e

        # Avoid using transactions, set isolation level to autocommit
        conn.set_isolation_level(0)
        return conn


class QueryStats(object):
    query = None
    path = None

    def __init__(self, dbname, conn, parameters=None, underscore=False):
        self.conn = conn
        self.dbname = dbname
        self.underscore = underscore
        self.parameters = parameters
        self.data = list()

    def _translate_datname(self, datname):
        """
        Replace '_' with '.'
        """
        if self.underscore:
            datname = datname.replace("_", ".")
        return datname

    def fetch(self, pg_version):
        if float(pg_version) >= 10.0 and hasattr(self, 'post_100_query'):
            q = self.post_100_query
        elif float(pg_version) >= 9.6 and hasattr(self, 'post_96_query'):
            q = self.post_96_query
        elif float(pg_version) >= 9.2 and hasattr(self, 'post_92_query'):
            q = self.post_92_query
        else:
            q = self.query

        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(q, self.parameters)
            rows = cursor.fetchall()
            for row in rows:
                # If row is length 2, assume col1, col2 forms key: value
                if len(row) == 2:
                    self.data.append({
                        'datname': self._translate_datname(self.dbname),
                        'metric': row[0],
                        'value': row[1],
                    })

                # If row > length 2, assume each column name maps to
                # key => value
                else:
                    for key, value in row.iteritems():
                        if key in ('datname', 'schemaname', 'relname',
                                   'indexrelname', 'funcname',):
                            continue

                        self.data.append({
                            'datname': self._translate_datname(row.get(
                                'datname', self.dbname)),
                            'schemaname': row.get('schemaname', None),
                            'relname': row.get('relname', None),
                            'indexrelname': row.get('indexrelname', None),
                            'funcname': row.get('funcname', None),
                            'metric': key,
                            'value': value,
                        })

        # Clean up
        finally:
            cursor.close()

    def __iter__(self):
        for data_point in self.data:
            yield (self.path % data_point, data_point['value'])


class VacuumPhase(QueryStats):
    path = "phase.%(metric)s"
    multi_db = False
    query = """
        SELECT phase
        FROM pg_stat_progress_vacuum
    """


class VacuumProgressStat(QueryStats):
    path = "progress_stat.%(metric)s"
    multi_db = False
    query = """
        SELECT heap_blks_total, heap_blks_scanned, heap_blks_vacuumed, 
            index_vacuum_count, max_dead_tuples, num_dead_tuples
        FROM pg_stat_progress_vacuum
    """


metrics_registry = {
    'VacuumPhase': VacuumPhase,
    'VacuumProgressStat': VacuumProgressStat,
}

registry = {
    'basic': [
        'VacuumPhase',
        'VacuumProgressStat',
    ],
    'extended': [
        'VacuumPhase',
        'VacuumProgressStat'
    ],
}
