# coding=utf-8

"""
Collects all number values from the db.serverStatus() command, other
values are ignored.

#### Dependencies

 * pymongo

"""

import diamond.collector
import re

try:
    import pymongo
    pymongo  # workaround for pyflakes issue #13
except ImportError:
    pymongo = None

try:
    from pymongo import ReadPreference
    ReadPreference  # workaround for pyflakes issue #13
except ImportError:
    ReadPreference = None


class MongoDBCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(MongoDBCollector, self).get_default_config_help()
        config_help.update({
            'hosts': 'Array of hostname(:port) elements to get metrics from',
            'host': 'A single hostname(:port) to get metrics from'
                   ' (can be used instead of hosts and overrides it)',
            'databases': 'A regex of which databases to gather metrics for.'
                        ' Defaults to all databases.',
            'ignore_collections': 'A regex of which collections to ignore.'
                                 ' MapReduce temporary collections (tmp.mr.*)'
                                 ' are ignored by default.',

        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MongoDBCollector, self).get_default_config()
        config.update({
            'path':      'mongo',
            'hosts':     ['localhost'],
            'databases': '.*',
            'ignore_collections': '^tmp\.mr\.',
        })
        return config

    def collect(self):
        """Collect number values from db.serverStatus()"""

        if pymongo is None:
            self.log.error('Unable to import pymongo')
            return {}

        # we need this for backwards compatibility
        if 'host' in self.config:
            self.config['hosts'] = [self.config['host']]

        for host in self.config['hosts']:
            if len(self.config['hosts']) == 1:
                # one host only, no need to have a prefix
                base_prefix = []
            else:
                base_prefix = [re.sub('[:\.]', '_', host)]

            try:
                if ReadPreference is None:
                    conn = pymongo.Connection(host)
                else:
                    conn = pymongo.Connection(
                        host,
                        read_preference=ReadPreference.SECONDARY)
            except Exception, e:
                self.log.error('Couldnt connect to mongodb: %s', e)
                return {}
            data = conn.db.command('serverStatus')
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
                    collection_prefix = db_prefix + [collection_name]
                    self._publish_dict_with_prefix(collection_stats,
                                                   collection_prefix)

    def _publish_dict_with_prefix(self, dict, prefix):
        for key in dict:
            self._publish_metrics(prefix, key, dict)

    def _publish_metrics(self, prev_keys, key, data):
        """Recursively publish keys"""
        value = data[key]
        keys = prev_keys + [key]
        if isinstance(value, dict):
            for new_key in value:
                self._publish_metrics(keys, new_key, value)
        elif isinstance(value, int) or isinstance(value, float):
            self.publish('.'.join(keys), value)
        elif isinstance(value, long):
            self.publish('.'.join(keys), float(value))
