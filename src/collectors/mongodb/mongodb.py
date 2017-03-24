# coding=utf-8

"""
Collects all number values from the db.serverStatus() command, other
values are ignored.

**Note:** this collector expects pymongo 2.4 and onward. See the pymongo
changelog for more details:
http://api.mongodb.org/python/current/changelog.html#changes-in-version-2-4

#### Dependencies

 * pymongo

#### Example Configuration

MongoDBCollector.conf

```
    enabled = True
    hosts = localhost:27017, alias1@localhost:27018, etc
```
"""

import diamond.collector
import datetime
from diamond.collector import str_to_bool
import re
import zlib

try:
    import pymongo
except ImportError:
    pymongo = None

try:
    from pymongo import ReadPreference
except ImportError:
    ReadPreference = None


class MongoDBCollector(diamond.collector.Collector):
    MAX_CRC32 = 4294967295

    def __init__(self, *args, **kwargs):
        self.__totals = {}
        super(MongoDBCollector, self).__init__(*args, **kwargs)

    def get_default_config_help(self):
        config_help = super(MongoDBCollector, self).get_default_config_help()
        config_help.update({
            'hosts': 'Array of hostname(:port) elements to get metrics from'
                     'Set an alias by prefixing host:port with alias@',
            'host': 'A single hostname(:port) to get metrics from'
                    ' (can be used instead of hosts and overrides it)',
            'user': 'Username for authenticated login (optional)',
            'passwd': 'Password for authenticated login (optional)',
            'databases': 'A regex of which databases to gather metrics for.'
                         ' Defaults to all databases.',
            'ignore_collections': 'A regex of which collections to ignore.'
                                  ' MapReduce temporary collections (tmp.mr.*)'
                                  ' are ignored by default.',
            'collection_sample_rate': 'Only send stats for a consistent subset '
                                      'of collections. This is applied after '
                                      'collections are ignored via '
                                      'ignore_collections Sampling uses crc32 '
                                      'so it is consistent across '
                                      'replicas. Value between 0 and 1. '
                                      'Default is 1',
            'network_timeout': 'Timeout for mongodb connection (in'
                               ' milliseconds). There is no timeout by'
                               ' default.',
            'simple': 'Only collect the same metrics as mongostat.',
            'translate_collections': 'Translate dot (.) to underscores (_)'
                                     ' in collection names.',
            'ssl': 'True to enable SSL connections to the MongoDB server.'
                   ' Default is False',
            'replica': 'True to enable replica set logging. Reports health of'
                       ' individual nodes as well as basic aggregate stats.'
                       ' Default is False',
            'replset_node_name': 'Identifier for reporting replset metrics. '
                                 'Default is _id'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MongoDBCollector, self).get_default_config()
        config.update({
            'path': 'mongo',
            'hosts': ['localhost'],
            'user': None,
            'passwd': None,
            'databases': '.*',
            'ignore_collections': '^tmp\.mr\.',
            'network_timeout': None,
            'simple': 'False',
            'translate_collections': 'False',
            'collection_sample_rate': 1,
            'ssl': False,
            'replica': False,
            'replset_node_name': '_id'
        })
        return config

    def collect(self):
        """Collect number values from db.serverStatus()"""

        if pymongo is None:
            self.log.error('Unable to import pymongo')
            return

        hosts = self.config.get('hosts')

        # Convert a string config value to be an array
        if isinstance(hosts, str):
            hosts = [hosts]

        # we need this for backwards compatibility
        if 'host' in self.config:
            hosts = [self.config['host']]

        # convert network_timeout to integer
        if self.config['network_timeout']:
            self.config['network_timeout'] = int(
                self.config['network_timeout'])

        # convert collection_sample_rate to float
        if self.config['collection_sample_rate']:
            self.config['collection_sample_rate'] = float(
                self.config['collection_sample_rate'])

        # use auth if given
        if 'user' in self.config:
            user = self.config['user']
        else:
            user = None

        if 'passwd' in self.config:
            passwd = self.config['passwd']
        else:
            passwd = None

        for host in hosts:
            matches = re.search('((.+)\@)?(.+)?', host)
            alias = matches.group(2)
            host = matches.group(3)

            if alias is None:
                if len(hosts) == 1:
                    # one host only, no need to have a prefix
                    base_prefix = []
                else:
                    base_prefix = [re.sub('[:\.]', '_', host)]
            else:
                base_prefix = [alias]

            try:
                # Ensure that the SSL option is a boolean.
                if type(self.config['ssl']) is str:
                    self.config['ssl'] = str_to_bool(self.config['ssl'])

                if ReadPreference is None:
                    conn = pymongo.MongoClient(
                        host,
                        socketTimeoutMS=self.config['network_timeout'],
                        ssl=self.config['ssl'],
                    )
                else:
                    conn = pymongo.MongoClient(
                        host,
                        socketTimeoutMS=self.config['network_timeout'],
                        ssl=self.config['ssl'],
                        read_preference=ReadPreference.SECONDARY,
                    )
            except Exception as e:
                self.log.error('Couldnt connect to mongodb: %s', e)
                continue

            # try auth
            if user:
                try:
                    conn.admin.authenticate(user, passwd)
                except Exception as e:
                    self.log.error(
                        'User auth given, but could not autheticate' +
                        ' with host: %s, err: %s' % (host, e))
                    return{}

            data = conn.db.command('serverStatus')
            self._publish_transformed(data, base_prefix)
            if str_to_bool(self.config['simple']):
                data = self._extract_simple_data(data)
            if str_to_bool(self.config['replica']):
                try:
                    replset_data = conn.admin.command('replSetGetStatus')
                    self._publish_replset(replset_data, base_prefix)
                except pymongo.errors.OperationFailure as e:
                    self.log.error('error getting replica set status', e)

            self._publish_dict_with_prefix(data, base_prefix)
            db_name_filter = re.compile(self.config['databases'])
            ignored_collections = re.compile(self.config['ignore_collections'])
            sample_threshold = self.MAX_CRC32 * self.config[
                'collection_sample_rate']
            for db_name in conn.database_names():
                if not db_name_filter.search(db_name):
                    continue
                db_stats = conn[db_name].command('dbStats')
                db_prefix = base_prefix + ['databases', db_name]
                self._publish_dict_with_prefix(db_stats, db_prefix)
                for collection_name in conn[db_name].collection_names():
                    if ignored_collections.search(collection_name):
                        continue
                    if (self.config['collection_sample_rate'] < 1 and (
                            zlib.crc32(collection_name) & 0xffffffff
                    ) > sample_threshold):
                        continue

                    collection_stats = conn[db_name].command('collstats',
                                                             collection_name)
                    if str_to_bool(self.config['translate_collections']):
                        collection_name = collection_name.replace('.', '_')
                    collection_prefix = db_prefix + [collection_name]
                    self._publish_dict_with_prefix(collection_stats,
                                                   collection_prefix)

    def _publish_replset(self, data, base_prefix):
        """ Given a response to replSetGetStatus, publishes all numeric values
            of the instance, aggregate stats of healthy nodes vs total nodes,
            and the observed statuses of all nodes in the replica set.
        """
        prefix = base_prefix + ['replset']
        self._publish_dict_with_prefix(data, prefix)
        total_nodes = len(data['members'])
        healthy_nodes = reduce(lambda value, node: value + node['health'],
                               data['members'], 0)

        self._publish_dict_with_prefix({
            'healthy_nodes': healthy_nodes,
            'total_nodes': total_nodes
        }, prefix)
        for node in data['members']:
            replset_node_name = node[self.config['replset_node_name']]
            node_name = str(replset_node_name.split('.')[0])
            self._publish_dict_with_prefix(node, prefix + ['node', node_name])

    def _publish_transformed(self, data, base_prefix):
        """ Publish values of type: counter or percent """
        self._publish_dict_with_prefix(data.get('opcounters', {}),
                                       base_prefix + ['opcounters_per_sec'],
                                       self.publish_counter)
        self._publish_dict_with_prefix(data.get('opcountersRepl', {}),
                                       base_prefix +
                                       ['opcountersRepl_per_sec'],
                                       self.publish_counter)
        self._publish_metrics(base_prefix + ['backgroundFlushing_per_sec'],
                              'flushes',
                              data.get('backgroundFlushing', {}),
                              self.publish_counter)
        self._publish_dict_with_prefix(data.get('network', {}),
                                       base_prefix + ['network_per_sec'],
                                       self.publish_counter)
        self._publish_metrics(base_prefix + ['extra_info_per_sec'],
                              'page_faults',
                              data.get('extra_info', {}),
                              self.publish_counter)

        def get_dotted_value(data, key_name):
            key_name = key_name.split('.')
            for i in key_name:
                data = data.get(i, {})
                if not data:
                    return 0
            return data

        def compute_interval(data, total_name):
            current_total = get_dotted_value(data, total_name)
            total_key = '.'.join(base_prefix + [total_name])
            last_total = self.__totals.get(total_key, current_total)
            interval = current_total - last_total
            self.__totals[total_key] = current_total
            return interval

        def publish_percent(value_name, total_name, data):
            value = float(get_dotted_value(data, value_name) * 100)
            interval = compute_interval(data, total_name)
            key = '.'.join(base_prefix + ['percent', value_name])
            self.publish_counter(key, value, time_delta=bool(interval),
                                 interval=interval)

        publish_percent('globalLock.lockTime', 'globalLock.totalTime', data)
        publish_percent('indexCounters.btree.misses',
                        'indexCounters.btree.accesses', data)

        locks = data.get('locks')
        if locks:
            if '.' in locks:
                locks['_global_'] = locks['.']
                del (locks['.'])
            key_prefix = '.'.join(base_prefix + ['percent'])
            db_name_filter = re.compile(self.config['databases'])
            interval = compute_interval(data, 'uptimeMillis')
            for db_name in locks:
                if not db_name_filter.search(db_name):
                    continue
                r = get_dotted_value(
                    locks,
                    '%s.timeLockedMicros.r' % db_name)
                R = get_dotted_value(
                    locks,
                    '.%s.timeLockedMicros.R' % db_name)
                value = float(r + R) / 10
                if value:
                    self.publish_counter(
                        key_prefix + '.locks.%s.read' % db_name,
                        value, time_delta=bool(interval),
                        interval=interval)
                w = get_dotted_value(
                    locks,
                    '%s.timeLockedMicros.w' % db_name)
                W = get_dotted_value(
                    locks,
                    '%s.timeLockedMicros.W' % db_name)
                value = float(w + W) / 10
                if value:
                    self.publish_counter(
                        key_prefix + '.locks.%s.write' % db_name,
                        value, time_delta=bool(interval), interval=interval)

    def _publish_dict_with_prefix(self, dict, prefix, publishfn=None):
        for key in dict:
            self._publish_metrics(prefix, key, dict, publishfn)

    def _publish_metrics(self, prev_keys, key, data, publishfn=None):
        """Recursively publish keys"""
        if key not in data:
            return
        value = data[key]
        keys = prev_keys + [key]
        keys = [x.replace(" ", "_").replace("-", ".") for x in keys]
        if not publishfn:
            publishfn = self.publish
        if isinstance(value, dict):
            for new_key in value:
                self._publish_metrics(keys, new_key, value)
        elif isinstance(value, int) or isinstance(value, float):
            publishfn('.'.join(keys), value)
        elif isinstance(value, long):
            publishfn('.'.join(keys), float(value))
        elif isinstance(value, datetime.datetime):
            publishfn('.'.join(keys), long(value.strftime('%s')))

    def _extract_simple_data(self, data):
        return {
            'connections': data.get('connections'),
            'globalLock': data.get('globalLock'),
            'indexCounters': data.get('indexCounters')
        }
