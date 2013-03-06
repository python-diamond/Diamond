# coding=utf-8

"""
Collect metrics from postgresql

#### Dependencies

 * psycopg2

"""

import diamond.collector

try:
    import psycopg2
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
            'underscore': 'Convert _ to .'
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
            'method': 'Threaded'})
        return config

    def collect(self):
        if psycopg2 is None:
            self.log.error('Unable to import module psycopg2')
            return {}

        self.conn_string = "host=%s user=%s password=%s port=%s" % (
            self.config['host'],
            self.config['user'],
            self.config['password'],
            self.config['port'])

        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

        # Statistics
        self.cursor.execute("SELECT pg_stat_database.*, \
                pg_database_size(pg_database.datname) AS size \
                FROM pg_database JOIN pg_stat_database \
                ON pg_database.datname = pg_stat_database.datname \
                WHERE pg_stat_database.datname \
                NOT IN ('template0','template1','postgres')")
        stats = self.cursor.fetchall()

        # Connections
        self.cursor.execute("SELECT datname, count(datname) \
                FROM pg_stat_activity GROUP BY pg_stat_activity.datname;")
        connections = self.cursor.fetchall()

        ret = {}
        for stat in stats:
            info = {'numbackends': stat[2],
                    'xact_commit': stat[3],
                    'xact_rollback': stat[4],
                    'blks_read': stat[5],
                    'blks_hit': stat[6],
                    'tup_returned': stat[7],
                    'tup_fetched': stat[8],
                    'tup_inserted': stat[9],
                    'tup_updated': stat[10],
                    'tup_deleted': stat[11],
                    'conflicts': stat[12],
                    'size': stat[14]}

            database = stat[1]
            ret[database] = info

        for database in ret:
            if self.config['underscore']:
                database = database.replace("_", ".")

            for (metric, value) in ret[database].items():
                    self.publish("database.%s.%s" % (
                        database, metric), value)

        for (database, connection) in connections:
            self.publish("database.%s.connections" % (
                database), connection)

        self.cursor.close()
        self.conn.close()
