# coding=utf-8

"""
Collect stats via MX4J from Kafka

#### Dependencies

 * urllib2
 * xml.etree
"""

import urllib2

from urllib import urlencode

try:
    from xml.etree import ElementTree
    ElementTree  # workaround for pyflakes issue #13
except ImportError:
    ElementTree = None

try:
    from ElementTree import ParseError as ETParseError
    ETParseError  # workaround for pyflakes issue #13
except ImportError:
    ETParseError = Exception

import diamond.collector


class KafkaCollector(diamond.collector.Collector):
    MBEAN_WHITELIST = frozenset([
        'kafka.log.LogStats',
        'kafka.network.SocketServerStats',
        'kafka.message.LogFlushStats',
        'kafka.server.BrokerTopicStat',
    ])

    JVM_MBEANS = {
        'java.lang:type=GarbageCollector,name=PS MarkSweep': 'jvm.gc.marksweep',
        'java.lang:type=GarbageCollector,name=PS Scavenge': 'jvm.gc.scavenge',
        'java.lang:type=Threading': 'jvm.threading',
    }

    ATTRIBUTE_TYPES = {
        'double': float,
        'float': float,
        'int': int,
        'long': long,
    }

    def get_default_config_help(self):
        config_help = super(KafkaCollector, self).get_default_config_help()
        config_help.update({
            'host': "",
            'port': "",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(KafkaCollector, self).get_default_config()
        config.update({
            'host': '127.0.0.1',
            'port': 7200,
            'path': 'kafka',
            'method': 'Threaded',
        })
        return config

    def _get(self, path, query_args=None):
        if not path.startswith('/'):
            path = '/' + path

        qargs = {'template': 'identity'}

        if query_args:
            qargs.update(query_args)

        url = 'http://%s:%i%s?%s' % (
            self.config['host'], int(self.config['port']),
            path, urlencode(qargs))

        try:
            response = urllib2.urlopen(url)
        except urllib2.URLError, err:
            self.log.error("%s: %s", url, err)
            return None

        try:
            return ElementTree.fromstring(response.read())
        except ETParseError:
            self.log.error("Unable to parse response from mx4j")
            return None

    def get_mbeans(self):
        query_args = {'querynames': 'kafka:*'}

        mbeans = self._get('/serverbydomain', query_args)
        if mbeans is None:
            return

        found_beans = set()

        for mbean in mbeans.getiterator(tag='MBean'):
            classname = mbean.get('classname')

            if classname not in self.MBEAN_WHITELIST:
                continue

            objectname = mbean.get('objectname')
            if objectname:
                found_beans.add(objectname)

        return found_beans

    def query_mbean(self, objectname, key_prefix=None):
        query_args = {
            'objectname': objectname,
            'operations': False,
            'constructors': False,
            'notifications': False,
        }

        attributes = self._get('/mbean', query_args)
        if attributes is None:
            return

        if key_prefix is None:
            key_prefix = objectname.split('=')[1]

        metrics = {}

        for attrib in attributes.getiterator(tag='Attribute'):
            atype = attrib.get('type')

            ptype = self.ATTRIBUTE_TYPES.get(atype)
            if not ptype:
                continue

            value = ptype(attrib.get('value'))

            name = '.'.join([key_prefix, attrib.get('name')])

            metrics[name] = value

        return metrics

    def collect(self):
        if ElementTree is None:
            self.log.error('Failed to import xml.etree.ElementTree')
            return

        # Get list of gatherable stats
        mbeans = self.get_mbeans()

        metrics = {}

        # Query each one for stats
        for mbean in mbeans:
            stats = self.query_mbean(mbean)
            metrics.update(stats)

        for mbean, key_prefix in self.JVM_MBEANS.iteritems():
            stats = self.query_mbean(mbean, key_prefix)
            metrics.update(stats)

        # Publish stats
        for metric, value in metrics.iteritems():
            self.publish(metric, value)
