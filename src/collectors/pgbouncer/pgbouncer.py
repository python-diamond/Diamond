# coding=utf-8

"""
Collect metrics from pgbouncer.

#### Dependencies

 * psycopg2

#### Example Configuration

```
enabled=True

[instances]

[[master]]
host = localhost
port = 6432

[[replica]]
host = localhost
port = 6433
password = foobar
```

"""

from collections import defaultdict

import diamond.collector

try:
    import psycopg2
    import psycopg2.extras
    psycopg2  # workaround for pyflakes issue #13
except ImportError:
    psycopg2 = None

STATS_QUERIES = ['SHOW POOLS', 'SHOW STATS']
IGNORE_COLUMNS = ['user']


class PgbouncerCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(PgbouncerCollector, self).get_default_config_help()
        config_help.update({
            'user': 'Username',
            'password': 'Password',
            'instances': 'A subcategory of pgbouncer instances with a host '
                         'and port, and optionally user and password can be '
                         'overridden per instance (see example).',
        })

        return config_help

    def get_default_config(self):
        config = super(PgbouncerCollector, self).get_default_config()
        config.update({
            'path': 'pgbouncer',
            'method': 'Threaded',
            'user': 'postgres',
            'password': '',
            'instances': {},
        })

        return config

    def collect(self):
        if psycopg2 is None:
            self.log.error('Unable to import module psycopg2.')
            return {}

        instances = self.config['instances']
        # HACK: setting default with subcategory messes up merging of configs,
        # so we only set the default if one wasn't provided.
        if not instances:
            instances = {
                'default': {
                    'host': 'localhost',
                    'port': '6432',
                }
            }

        for name, instance in instances.iteritems():
            host = instance['host']
            port = instance['port']
            user = instance.get('user') or self.config['user']
            password = instance.get('password') or self.config['password']

            for database, stats in self._get_stats_by_database(
                    host, port, user, password).iteritems():
                for stat_name, stat_value in stats.iteritems():
                    self.publish(
                        self._get_metric_name(name, database, stat_name),
                        stat_value)

    def _get_metric_name(self, name, database, stat_name):
        name = name.replace('.', '_').replace(':', '_').strip()
        return '.'.join([name, database, stat_name])

    def _get_stats_by_database(self, host, port, user, password):
        # Mapping of database name -> stats.
        databases = defaultdict(dict)
        conn = psycopg2.connect(database='pgbouncer',
                                user=user,
                                password=password,
                                host=host,
                                port=port)

        # Avoid using transactions, set isolation level to autocommit
        conn.set_isolation_level(0)

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        for query in STATS_QUERIES:
            cursor.execute(query)
            for row in cursor.fetchall():
                stats = row.copy()
                database = stats.pop('database')

                for ignore in IGNORE_COLUMNS:
                    if ignore in stats:
                        stats.pop(ignore)

                databases[database].update(stats)

        return databases
