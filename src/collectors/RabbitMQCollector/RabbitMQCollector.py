try:
    from numbers import Number
    import pyrabbit.api
except ImportError:
    Number = None
import diamond

from pprint import pprint

class RabbitMQCollector(diamond.collector.Collector):
    """Collects data from RabbitMQ through the admin interface

    """

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'path':     'rabbitmq',
            'host':     'localhost:55672',
            'user':     'guest',
            'password': 'guest',
        }

    def collect(self):
        if Number is None:
            self.log.error('Unable to import either Number or pyrabbit.api')
            return {}

        client = pyrabbit.api.Client(self.config['host'],
                                     self.config['user'],
                                     self.config['password'])

        for queue in client.get_queues():
            for key in queue:
                name = '{0}.{1}'.format('queues', queue['name'])
                self._publish_metrics(name, [], key, queue)

        overview = client.get_overview()
        for key in overview:
            self._publish_metrics('', [], key, overview)

    def _publish_metrics(self, name, prev_keys, key, data):
        """Recursively publish keys"""
        value = data[key]
        keys = prev_keys + [key]
        if isinstance(value, dict):
            for new_key in value:
                self._publish_metrics(name, keys, new_key, value)
        elif isinstance(value, Number):
            joined_keys = '.'.join(keys)
            if name:
                publish_key = '{0}.{1}'.format(name, joined_keys)
            else:
                publish_key = joined_keys
            self.publish(publish_key, value)

