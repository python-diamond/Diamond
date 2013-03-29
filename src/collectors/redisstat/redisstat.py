# coding=utf-8

"""
Collects data from one or more Redis Servers

#### Dependencies

 * redis

#### Notes

The collector is named an odd redisstat because of an import issue with
having the python library called redis and this collector's module being called
redis, so we use an odd name for this collector. This doesn't affect the usage
of this collector.

Example config file RedisCollector.conf

```
enabled=True
host=redis.example.com
port=16379
auth=PASSWORD
```

or for multi-instance mode:

```
enabled=True
instances = nick1@host1:port1, nick2@host2:port2/PASSWORD, ...
```

Note: when using the host/port config mode, the port number is used in
the metric key. When using the multi-instance mode, the nick will be used.
If not specified the port will be used.


"""

import diamond.collector
import time

try:
    import redis
    redis  # workaround for pyflakes issue #13
except ImportError:
    redis = None


class RedisCollector(diamond.collector.Collector):

    _DATABASE_COUNT = 16
    _DEFAULT_DB = 0
    _DEFAULT_HOST = 'localhost'
    _DEFAULT_PORT = 6379
    _DEFAULT_SOCK_TIMEOUT = 5
    _KEYS = {'clients.blocked': 'blocked_clients',
             'clients.connected': 'connected_clients',
             'clients.longest_output_list': 'client_longest_output_list',
             'cpu.parent.sys': 'used_cpu_sys',
             'cpu.children.sys': 'used_cpu_sys_childrens',
             'cpu.parent.user': 'used_cpu_user',
             'cpu.children.user': 'used_cpu_user_childrens',
             'hash_max_zipmap.entries': 'hash_max_zipmap_entries',
             'hash_max_zipmap.value': 'hash_max_zipmap_value',
             'keys.evicted': 'evicted_keys',
             'keys.expired': 'expired_keys',
             'keyspace.hits': 'keyspace_hits',
             'keyspace.misses': 'keyspace_misses',
             'last_save.changes_since': 'changes_since_last_save',
             'last_save.time': 'last_save_time',
             'memory.internal_view': 'used_memory',
             'memory.external_view': 'used_memory_rss',
             'memory.fragmentation_ratio': 'mem_fragmentation_ratio',
             'process.commands_processed': 'total_commands_processed',
             'process.connections_received': 'total_connections_received',
             'process.uptime': 'uptime_in_seconds',
             'pubsub.channels': 'pubsub_channels',
             'pubsub.patterns': 'pubsub_patterns',
             'slaves.connected': 'connected_slaves'}
    _RENAMED_KEYS = {'last_save.changes_since': 'rdb_changes_since_last_save',
                     'last_save.time': 'rdb_last_save_time'}

    def __init__(self, *args, **kwargs):
        super(RedisCollector, self).__init__(*args, **kwargs)

        instance_list = self.config['instances']
        # configobj make str of single-element list, let's convert
        if isinstance(instance_list, basestring):
            instance_list = [instance_list]

        # process original single redis instance
        if len(instance_list) == 0:
            host = self.config['host']
            port = int(self.config['port'])
            auth = self.config['auth']
            if auth != None:
                instance_list.append('%s:%d/%s' % (host, port, auth))
            else:
                instance_list.append('%s:%d' % (host, port))

        self.instances = {}
        for instance in instance_list:

            if '@' in instance:
                (nickname, hostport) = instance.split('@', 2)
            else:
                nickname = None
                hostport = instance

            if '/' in hostport:
                parts = hostport.split('/')
                hostport = parts[0]
                auth = parts[1]
            else:
                auth = None

            if ':' in hostport:
                if hostport[0] == ':':
                    host = self._DEFAULT_HOST
                    port = int(hostport[1:])
                else:
                    parts = hostport.split(':')
                    host = parts[0]
                    port = int(parts[1])
            else:
                host = hostport
                port = self._DEFAULT_PORT

            if nickname is None:
                nickname = str(port)

            self.instances[nickname] = (host, port, auth)

    def get_default_config_help(self):
        config_help = super(RedisCollector, self).get_default_config_help()
        config_help.update({
            'host': 'Hostname to collect from',
            'port': 'Port number to collect from',
            'timeout': 'Socket timeout',
            'db': '',
            'auth': 'Password?',
            'databases': 'how many database instances to collect',
            'instances': "Redis addresses, comma separated, syntax:"
            + " nick1@host:port, nick2@:port or nick3@host"
        })
        return config_help

    def get_default_config(self):
        """
        Return default config

:rtype: dict

        """
        config = super(RedisCollector, self).get_default_config()
        config.update({
            'host': self._DEFAULT_HOST,
            'port': self._DEFAULT_PORT,
            'timeout': self._DEFAULT_SOCK_TIMEOUT,
            'db': self._DEFAULT_DB,
            'auth': None,
            'databases': self._DATABASE_COUNT,
            'path': 'redis',
            'instances': [],
        })
        return config

    def _client(self, host, port, auth):
        """Return a redis client for the configuration.

:param str host: redis host
:param int port: redis port
:rtype: redis.Redis

        """
        db = int(self.config['db'])
        timeout = int(self.config['timeout'])
        try:
            cli = redis.Redis(host=host, port=port,
                              db=db, socket_timeout=timeout, password=auth)
            cli.ping()
            return cli
        except Exception, ex:
            self.log.error("RedisCollector: failed to connect to %s:%i. %s.",
                           host, port, ex)

    def _precision(self, value):
        """Return the precision of the number

:param str value: The value to find the precision of
:rtype: int

        """
        value = str(value)
        decimal = value.rfind('.')
        if decimal == -1:
            return 0
        return len(value) - decimal - 1

    def _publish_key(self, nick, key):
        """Return the full key for the partial key.

:param str nick: Nickname for Redis instance
:param str key: The key name
:rtype: str

        """
        return '%s.%s' % (nick, key)

    def _get_info(self, host, port, auth):
        """Return info dict from specified Redis instance

:param str host: redis host
:param int port: redis port
:rtype: dict

        """

        client = self._client(host, port, auth)
        if client is None:
            return None

        info = client.info()
        del client
        return info

    def collect_instance(self, nick, host, port, auth):
        """Collect metrics from a single Redis instance

:param str nick: nickname of redis instance
:param str host: redis host
:param int port: redis port

        """

        # Connect to redis and get the info
        info = self._get_info(host, port, auth)
        if info is None:
            return

        # The structure should include the port for multiple instances per
        # server
        data = dict()

        # Iterate over the top level keys
        for key in self._KEYS:
            if self._KEYS[key] in info:
                data[key] = info[self._KEYS[key]]

        # Iterate over renamed keys for 2.6 support
        for key in self._RENAMED_KEYS:
            if self._RENAMED_KEYS[key] in info:
                data[key] = info[self._RENAMED_KEYS[key]]

        # Look for databaase speific stats
        for dbnum in range(0, int(self.config.get('databases',
                                  self._DATABASE_COUNT))):
            db = 'db%i' % dbnum
            if db in info:
                for key in info[db]:
                    data['%s.%s' % (db, key)] = info[db][key]

        # Time since last save
        for key in ['last_save_time', 'rdb_last_save_time']:
            if key in info:
                data['last_save.time_since'] = int(time.time()) - info[key]

        # Publish the data to graphite
        for key in data:
            self.publish(self._publish_key(nick, key),
                         data[key],
                         precision=self._precision(data[key]),
                         metric_type='GAUGE')

    def collect(self):
        """Collect the stats from the redis instance and publish them.

        """
        if redis is None:
            self.log.error('Unable to import module redis')
            return {}

        for nick in self.instances.keys():
            (host, port, auth) = self.instances[nick]
            self.collect_instance(nick, host, int(port), auth)
