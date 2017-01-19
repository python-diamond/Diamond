# coding=utf-8

"""
Collect slony metrics from postgresql

#### Dependencies

 * psycopg2

#### Example Configuration

```
enabled = True

host = localhost
port = 5432
slony_node_string = Node [0-9] - [_a-z0-9]*@(.*).example.com

[instances]

[[database1]]
slony_db = postgres
slony_schema = _slony


[[database2]]
user = postgres
password = postgres
slony_db = data_db
slony_node_string = Node [0-9] - [_a-z0-9]*@(.*).i.example.com
slony_schema = _data_db
```

"""

import diamond.collector

try:
    import psycopg2
    import psycopg2.extensions
    psycopg2  # workaround for pyflakes issue #13
except ImportError:
    psycopg2 = None


class SlonyCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(SlonyCollector, self).get_default_config_help()
        config_help.update({
            'host': 'Hostname',
            'user': 'Username',
            'password': 'Password',
            'port': 'Port number',
            'slony_node_string': 'Regex for SQL SUBSTRING to extract ' +
                                 'the hostname from sl_node.no_comment',
            'instances': 'Subcategory of slony instances that includes the ' +
                         'slony database, and slony schema to be monitored. ' +
                         'Optionally, user, password and slony_node_string ' +
                         'maybe overridden per instance (see example).'
        })
        return config_help

    def get_default_config(self):
        """
        Return default config.
        """
        config = super(SlonyCollector, self).get_default_config()
        config.update({
            'path': 'postgres',
            'host': 'localhost',
            'user': 'postgres',
            'password': 'postgres',
            'port': 5432,
            'slony_node_string': 'Node [0-9]+ - postgres@localhost',
            'method': 'Threaded',
            'instances': {},
        })
        return config

    def collect(self):
        if psycopg2 is None:
            self.log.error('Unable to import module psycopg2')
            return {}

        instances = self.config['instances']
        # HACK: setting default with subcategory messes up merging of configs,
        # so we only set the default if one wasn't provided.
        if not instances:
            instances = {
                'default': {
                    'slony_db': 'postgres',
                    'slony_schema': '_postgres',
                }
            }

        for name, instance in instances.iteritems():
            host = self.config['host']
            port = self.config['port']
            user = instance.get('user') or self.config['user']
            password = instance.get('password') or self.config['password']
            slony_node_string = instance.get('slony_node_string') or \
                self.config['slony_node_string']
            slony_db = instance['slony_db']
            slony_schema = instance['slony_schema']

            stats = self._get_stats_by_database(
                host, port, user, password, slony_db,
                slony_schema, slony_node_string
            )
            [self.publish(metric, value) for metric, value in stats]

    def _get_stats_by_database(self, host, port, user,
                               password, db, schema, node_string):
        path = "slony.%(datname)s.%(metric)s.lag_events"
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=db)

        # Avoid using transactions, set isolation level to autocommit
        conn.set_isolation_level(0)

        query = """
            SELECT SUBSTRING(sl.no_comment FROM %(node_extractor)s) AS node,
                   st.st_lag_num_events AS lag_events
            FROM %(schema)s.sl_status AS st, %(schema)s.sl_node AS sl
            WHERE sl.no_id = st.st_received
        """
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query, {
            'node_extractor': node_string,
            'schema': psycopg2.extensions.AsIs(schema),
        })

        metrics = []
        for row in cursor.fetchall():
            stats = row.copy()
            metrics.append((
                path % {'datname': db, 'metric': stats.get('node')},
                stats.get('lag_events')
            ))
        return metrics
