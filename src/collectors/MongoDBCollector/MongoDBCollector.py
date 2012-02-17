from numbers import Number

import diamond
import pymongo


class MongoDBCollector(diamond.collector.Collector):
    """Collects data from MongoDB's db.serverStatus() command

    Collects all number values from the db.serverStatus() command, other
    values are ignored.

    """
    def collect(self):
        """Collect number values from db.serverStatus()"""
        conn = pymongo.Connection(self.config['host'])
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
