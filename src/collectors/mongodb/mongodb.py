"""
Collects all number values from the db.serverStatus() command, other
values are ignored.

#### Dependencies

 * pymongo

"""

import diamond.collector

try:
    from numbers import Number
    import pymongo
    from pymongo import ReadPreference
except ImportError:
    Number = None

class MongoDBCollector(diamond.collector.Collector):
    
    def get_default_config_help(self):
        config_help = super(MongoDBCollector, self).get_default_config_help()
        config_help.update({
            'host' : 'Hostname',
        })
        return config_help
    
    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MongoDBCollector, self).get_default_config()
        config.update(  {
            'path':     'mongo',
            'host':     'localhost'
        } )
        return config
    
    def collect(self):
        """Collect number values from db.serverStatus()"""

        if Number is None:
            self.log.error('Unable to import either Number or pymongo')
            return {}

        try:
            conn = pymongo.Connection(self.config['host'],read_preference=ReadPreference.SECONDARY)
        except Exception, e:
            self.log.error('Couldnt connect to mongodb: %s', e)
            return {}
        data = conn.db.command('serverStatus')
        for key in data:
            self._publish_metrics([], key, data)

    def _publish_metrics(self, prev_keys, key, data):
        """Recursively publish keys"""
        value = data[key]
        keys = prev_keys + [key]
        if isinstance(value, dict):
            for new_key in value:
                self._publish_metrics(keys, new_key, value)
        elif isinstance(value, Number):
            self.publish('.'.join(keys), value)
