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
except ImportError:
    ElementTree = None

try:
    from ElementTree import ParseError as ETParseError
except ImportError:
    ETParseError = Exception

import diamond.collector


class KafkaCollector(diamond.collector.Collector):
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
            'port': 8082,
            'path': 'kafka',
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

    def get_mbeans(self, pattern):
        query_args = {'querynames': pattern}

        mbeans = self._get('/serverbydomain', query_args)
        if mbeans is None:
            return

        found_beans = set()

        for mbean in mbeans.getiterator(tag='MBean'):
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
            # Could be multiple ='s in the string, depending on Kafka version
            #
            # java.lang:type=Threading
            #
            # "kafka.controller":type="ControllerStats",
            # name="LeaderElectionRateAndTimeMs"
            #
            # v0.10+:
            # kafka.server:type=BrokerTopicMetrics,name=TotalProduceRequestsPerSec,
            # topic=my_topic_name

            labelset = objectname.split(':')[1]
            labels = {}
            for label in labelset.split(','):
                k,v = label.split('=')
                if '"' in v:
                    v = v.split('"')[1]
                labels[k] = v
            # Here we specify the order of the labels from Kafka for a
            # sane data hierarchy
            vals = [labels[x] for x in ['topic',
                                        'type',
                                        'name',
                                        'brokerHost',
                                        'brokerPort',
                                        'broker-id'
                                        'clientId',
                                        'client-id',
                                        'fetcherType',
                                        'fetcher-id',
                                        'networkProcessor',
                                        'request',
                                        'partition'] if x in labels]
            key_prefix = '.'.join(vals)
            if 'topic' in labels:
                key_prefix = 'Topic.' + key_prefix

        metrics = {}
        for attrib in attributes.getiterator(tag='Attribute'):
            atype = attrib.get('type')

            if atype == 'java.lang.Object':
                try:
                    try:
                        value = long(attrib.get('value'))
                    except (TypeError, ValueError):
                        value = float(attrib.get('value'))
                except (TypeError, ValueError):
                    continue
            else:
                ptype = self.ATTRIBUTE_TYPES.get(atype)

                if ptype is None:
                    for mbean_attrib in attributes.getiterator(tag='MBean'):
                        if 'JmxReporter$Gauge' in mbean_attrib.get('classname'):
                            ptype = float
                            break

                if not ptype:
                    continue

                try:
                    value = ptype(attrib.get('value'))
                except (TypeError, ValueError):
                    continue

            name = '.'.join([key_prefix, attrib.get('name')])
            # Some prefixes and attributes could have spaces, thus we must
            # sanitize them
            name = name.replace(' ', '')

            metrics[name] = value

        return metrics

    def collect(self):
        if ElementTree is None:
            self.log.error('Failed to import xml.etree.ElementTree')
            return

        # Get list of gatherable stats
        query_list = [
            '*kafka*:*',
            'java.lang:type=GarbageCollector,name=*',
            'java.lang:type=Threading'
        ]
        mbeans = set()
        for pattern in query_list:
            match = self.get_mbeans(pattern)
            mbeans.update(match)

        metrics = {}

        # Query each one for stats
        for mbean in mbeans:
            stats = self.query_mbean(mbean)
            metrics.update(stats)

        # Publish stats
        for metric, value in metrics.iteritems():
            self.publish(metric, value)
