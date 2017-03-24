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

For connecting via unix sockets, provide the path prefixed with ``unix:``
instead of the host, e.g.

```
enabled=True
host=unix:/var/run/redis/redis.sock
```

or

```
enabled = True
instances = nick3@unix:/var/run/redis.sock:/PASSWORD
```

In that case, for disambiguation there must be a colon ``:`` before the slash
``/`` followed by the password.

Note: when using the host/port config mode, the port number is used in
the metric key. When using the multi-instance mode, the nick will be used.
If not specified the port will be used. In case of unix sockets, the base name
without file extension (i.e. in the aforementioned examples ``redis``)
is the default metric key.


"""

import diamond.collector
import time
import os

try:
    import redis
except ImportError:
    redis = None


SOCKET_PREFIX = 'unix:'
SOCKET_PREFIX_LEN = len(SOCKET_PREFIX)


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
             'cpu.children.sys': 'used_cpu_sys_children',
             'cpu.parent.user': 'used_cpu_user',
             'cpu.children.user': 'used_cpu_user_children',
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
             'replication.master_sync_in_progress': 'master_sync_in_progress',
             'slaves.connected': 'connected_slaves',
             'slaves.last_io': 'master_last_io_seconds_ago'}
    _RENAMED_KEYS = {'last_save.changes_since': 'rdb_changes_since_last_save',
                     'last_save.time': 'rdb_last_save_time'}

    def process_config(self):
        super(RedisCollector, self).process_config()
        instance_list = self.config['instances']
        # configobj make str of single-element list, let's convert
        if isinstance(instance_list, str):
            instance_list = [instance_list]

        # process original single redis instance
        if len(instance_list) == 0:
            host = self.config['host']
            port = int(self.config['port'])
            auth = self.config['auth']
            if auth is not None:
                instance_list.append('%s:%d/%s' % (host, port, auth))
            else:
                instance_list.append('%s:%d' % (host, port))

        self.instances = {}
        for instance in instance_list:

            if '@' in instance:
                (nickname, hostport) = instance.split('@', 1)
            else:
                nickname = None
                hostport = instance

            if hostport.startswith(SOCKET_PREFIX):
                unix_socket, __, port_auth = hostport[
                    SOCKET_PREFIX_LEN:].partition(':')
                auth = port_auth.partition('/')[2] or None

                if nickname is None:
                    nickname = os.path.splitext(
                        os.path.basename(unix_socket))[0]
                self.instances[nickname] = (self._DEFAULT_HOST,
                                            self._DEFAULT_PORT,
                                            unix_socket,
                                            auth)
            else:
                if '/' in hostport:
                    parts = hostport.split('/')
                    hostport = parts[0]
                    auth = '/'.join(parts[1:])
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

                self.instances[nickname] = (host, port, None, auth)

        self.log.debug("Configured instances: %s" % self.instances.items())

    def get_default_config_help(self):
        config_help = super(RedisCollector, self).get_default_config_help()
        config_help.update({
            'host': 'Hostname to collect from',
            'port': 'Port number to collect from',
            'timeout': 'Socket timeout',
            'db': '',
            'auth': 'Password?',
            'databases': 'how many database instances to collect',
            'instances': "Redis addresses, comma separated, syntax:" +
                         " nick1@host:port, nick2@:port or nick3@host"
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

    def _client(self, host, port, unix_socket, auth):
        """Return a redis client for the configuration.

:param str host: redis host
:param int port: redis port
:rtype: redis.Redis

        """
        db = int(self.config['db'])
        timeout = int(self.config['timeout'])
        try:
            cli = redis.Redis(host=host, port=port,
                              db=db, socket_timeout=timeout, password=auth,
                              unix_socket_path=unix_socket)
            cli.ping()
            return cli
        except Exception as ex:
            self.log.error("RedisCollector: failed to connect to %s:%i. %s.",
                           unix_socket or host, port, ex)

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

    def _get_info(self, host, port, unix_socket, auth):
        """Return info dict from specified Redis instance

:param str host: redis host
:param int port: redis port
:rtype: dict

        """

        client = self._client(host, port, unix_socket, auth)
        if client is None:
            return None

        info = client.info()
        del client
        return info

    def _get_config(self, host, port, unix_socket, auth, config_key):
        """Return config string from specified Redis instance and config key

:param str host: redis host
:param int port: redis port
:param str host: redis config_key
:rtype: str

        """

        client = self._client(host, port, unix_socket, auth)
        if client is None:
            return None

        config_value = client.config_get(config_key)
        del client
        return config_value

    def collect_instance(self, nick, host, port, unix_socket, auth):
        """Collect metrics from a single Redis instance

:param str nick: nickname of redis instance
:param str host: redis host
:param int port: redis port
:param str unix_socket: unix socket, if applicable
:param str auth: authentication password

        """

        # Connect to redis and get the info
        info = self._get_info(host, port, unix_socket, auth)
        if info is None:
            return

        # The structure should include the port for multiple instances per
        # server
        data = dict()

        # Role needs to be handled outside the the _KEYS dict
        # since the value is a string, not a int / float
        # Also, master_sync_in_progress is only available if the
        # redis instance is a slave, so default it here so that
        # the metric is cleared if the instance flips from slave
        # to master
        if 'role' in info:
            if info['role'] == "master":
                data['replication.master'] = 1
                data['replication.master_sync_in_progress'] = 0
            else:
                data['replication.master'] = 0

        # Connect to redis and get the maxmemory config value
        # Then calculate the % maxmemory of memory used
        maxmemory_config = self._get_config(host, port, unix_socket, auth,
                                            'maxmemory')
        if maxmemory_config and 'maxmemory' in maxmemory_config.keys():
            maxmemory = float(maxmemory_config['maxmemory'])

            # Only report % used if maxmemory is a non zero value
            if maxmemory == 0:
                maxmemory_percent = 0.0
            else:
                maxmemory_percent = info['used_memory'] / maxmemory * 100
                maxmemory_percent = round(maxmemory_percent, 2)
            data['memory.used_percent'] = float("%.2f" % maxmemory_percent)

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
            (host, port, unix_socket, auth) = self.instances[nick]
            self.collect_instance(nick, host, int(port), unix_socket, auth)
