"""
Collects metrics on queues and queue consumers from PgQ, a PostgreSQL-based
queueing mechanism (part of the Skytools utilities released by Skype.)

#### Dependencies

 * psycopg2

#### Example Configuration

```
enabled = True

[instances]

[[database1]]
dsn = postgresql://user:secret@localhost

[[database2]]
dsn = host=localhost port=5432 dbname=mydb
```
"""
try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    psycopg2 = None

import diamond.collector


class PgQCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(PgQCollector, self).get_default_config_help()
        config_help.update({
            "instances": "The databases to be monitored. Each should have a "
                         "`dsn` attribute, which must be a valid libpq "
                         "connection string."
        })
        return config_help

    def get_default_config(self):
        config = super(PgQCollector, self).get_default_config()
        config.update({
            'instances': {},
        })
        return config

    def collect(self):
        if psycopg2 is None:
            self.log.error('Unable to import module psycopg2')
            return None

        for instance, configuration in self.config['instances'].iteritems():
            connection = psycopg2.connect(configuration['dsn'])
            connection.set_isolation_level(
                psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT,
            )
            self._collect_for_instance(instance, connection)

    def _collect_for_instance(self, instance, connection):
        "Collects metrics for a named connection."
        with connection.cursor() as cursor:
            for queue, metrics in self.get_queue_info(instance, cursor):
                for name, metric in metrics.items():
                    self.publish('.'.join((instance, queue, name)), metric)

        with connection.cursor() as cursor:
            consumers = self.get_consumer_info(instance, cursor)
            for queue, consumer, metrics in consumers:
                for name, metric in metrics.items():
                    key_parts = (instance, queue, 'consumers', consumer, name)
                    self.publish('.'.join(key_parts), metric)

    QUEUE_INFO_STATEMENT = """
        SELECT
            queue_name,
            EXTRACT(epoch from ticker_lag),
            ev_per_sec
        FROM pgq.get_queue_info()
    """

    def get_queue_info(self, instance, cursor):
        "Collects metrics for all queues on the connected database."
        cursor.execute(self.QUEUE_INFO_STATEMENT)
        for queue_name, ticker_lag, ev_per_sec in cursor:
            yield queue_name, {
                'ticker_lag': ticker_lag,
                'ev_per_sec': ev_per_sec,
            }

    CONSUMER_INFO_STATEMENT = """
        SELECT
            queue_name,
            consumer_name,
            EXTRACT(epoch from lag),
            pending_events,
            EXTRACT(epoch from last_seen)
        FROM pgq.get_consumer_info()
    """

    def get_consumer_info(self, instance, cursor):
        "Collects metrics for all consumers on the connected database."
        cursor.execute(self.CONSUMER_INFO_STATEMENT)
        for queue_name, consumer_name, lag, pending_events, last_seen in cursor:
            yield queue_name, consumer_name, {
                'lag': lag,
                'pending_events': pending_events,
                'last_seen': last_seen,
            }
