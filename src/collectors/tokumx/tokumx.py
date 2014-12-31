# coding=utf-8

"""
Collects all number values from the db.serverStatus() and db.engineStatus()
command, other values are ignored.

#### Dependencies

 * pymongo

"""

import diamond.collector
from diamond.collector import str_to_bool
import re

try:
    import pymongo
except ImportError:
    pymongo = None

try:
    from pymongo import ReadPreference
except ImportError:
    ReadPreference = None


class TokuMXCollector(diamond.collector.Collector):

    def __init__(self, *args, **kwargs):
        self.__totals = {}
        super(TokuMXCollector, self).__init__(*args, **kwargs)

    def get_default_config_help(self):
        config_help = super(TokuMXCollector, self).get_default_config_help()
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
            'network_timeout': 'Timeout for mongodb connection (in seconds).'
                               ' There is no timeout by default.',
            'simple': 'Only collect the same metrics as mongostat.',
            'translate_collections': 'Translate dot (.) to underscores (_)'
                                     ' in collection names.'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(TokuMXCollector, self).get_default_config()
        config.update({
            'path':      'mongo',
            'hosts':     ['localhost'],
            'user':      None,
            'passwd':      None,
            'databases': '.*',
            'ignore_collections': '^tmp\.mr\.',
            'network_timeout': None,
            'simple': 'False',
            'translate_collections': 'False'
        })
        return config

    def collect(self):
        """Collect number values from db.serverStatus() and db.engineStatus()"""

        if pymongo is None:
            self.log.error('Unable to import pymongo')
            return

        # we need this for backwards compatibility
        if 'host' in self.config:
            self.config['hosts'] = [self.config['host']]

        # convert network_timeout to integer
        if self.config['network_timeout']:
            self.config['network_timeout'] = int(
                self.config['network_timeout'])

        # use auth if given
        if 'user' in self.config:
            user = self.config['user']
        else:
            user = None

        if 'passwd' in self.config:
            passwd = self.config['passwd']
        else:
            passwd = None

        for host in self.config['hosts']:
            if len(self.config['hosts']) == 1:
                # one host only, no need to have a prefix
                base_prefix = []
            else:
                matches = re.search('((.+)\@)?(.+)?', host)
                alias = matches.group(2)
                host = matches.group(3)

                if alias is None:
                    base_prefix = [re.sub('[:\.]', '_', host)]
                else:
                    base_prefix = [alias]

            try:
                if ReadPreference is None:
                    conn = pymongo.Connection(
                        host,
                        network_timeout=self.config['network_timeout'],
                        slave_okay=True
                    )
                else:
                    conn = pymongo.Connection(
                        host,
                        network_timeout=self.config['network_timeout'],
                        read_preference=ReadPreference.SECONDARY,
                    )
            except Exception, e:
                self.log.error('Couldnt connect to mongodb: %s', e)
                continue

            # try auth
            if user:
                try:
                    conn.admin.authenticate(user, passwd)
                except Exception, e:
                    self.log.error('User auth given, but could not autheticate'
                                   + ' with host: %s, err: %s' % (host, e))
                    return{}

            serverStatus = conn.db.command('serverStatus')
            engineStatus = conn.db.command('engineStatus')
            data = dict(serverStatus.items() + engineStatus.items())

            self._publish_transformed(data, base_prefix)
            if str_to_bool(self.config['simple']):
                data = self._extract_simple_data(data)

            self._publish_dict_with_prefix(data, base_prefix)
            db_name_filter = re.compile(self.config['databases'])
            ignored_collections = re.compile(self.config['ignore_collections'])
            for db_name in conn.database_names():
                if not db_name_filter.search(db_name):
                    continue
                db_stats = conn[db_name].command('dbStats')
                db_prefix = base_prefix + ['databases', db_name]
                self._publish_dict_with_prefix(db_stats, db_prefix)
                for collection_name in conn[db_name].collection_names():
                    if ignored_collections.search(collection_name):
                        continue
                    collection_stats = conn[db_name].command('collstats',
                                                             collection_name)
                    if str_to_bool(self.config['translate_collections']):
                        collection_name = collection_name.replace('.', '_')
                    collection_prefix = db_prefix + [collection_name]
                    self._publish_dict_with_prefix(collection_stats,
                                                   collection_prefix)

    def _publish_transformed(self, data, base_prefix):
        """ Publish values of type: counter or percent """
        self._publish_dict_with_prefix(data.get('opcounters', {}),
                                       base_prefix + ['opcounters_per_sec'],
                                       self.publish_counter)
        self._publish_dict_with_prefix(data.get('opcountersRepl', {}),
                                       base_prefix + ['opcountersRepl_per_sec'],
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
        if not key in data:
            return
        value = data[key]
        keys = prev_keys + [key]
        if not publishfn:
            publishfn = self.publish
        if isinstance(value, dict):
            for new_key in value:
                self._publish_metrics(keys, new_key, value)
        elif isinstance(value, int) or isinstance(value, float):
            publishfn('.'.join(keys), value)
        elif isinstance(value, long):
            publishfn('.'.join(keys), float(value))

    def _extract_simple_data(self, data):
        return {
            'connections': data.get('connections'),
            'globalLock': data.get('globalLock'),
            'indexCounters': data.get('indexCounters')
        }
