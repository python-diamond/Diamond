# coding=utf-8

"""
Collects stats from bind 9.5's statistics server

#### Dependencies

 * [bind 9.5](http://www.isc.org/software/bind/new-features/9.5)
    configured with libxml2 and statistics-channels

"""

import diamond.collector
import sys
import urllib2

if sys.version_info >= (2, 5):
    import xml.etree.cElementTree as ElementTree
else:
    import cElementTree as ElementTree


class BindCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(BindCollector, self).get_default_config_help()
        config_help.update({
            'host': "",
            'port': "",
            'publish': "Available stats:\n" +
            " - resolver (Per-view resolver and cache statistics)\n" +
            " - server (Incoming requests and their answers)\n" +
            " - zonemgmt (Zone management requests/responses)\n" +
            " - sockets (Socket statistics)\n" +
            " - memory (Global memory usage)\n",
            'publish_view_bind': "",
            'publish_view_meta': "",
            'data_format': "Bind stats version:\n" +
            " - xml_v2 (Original bind stats version from 9.5)\n" +
            " - xml_v3 (New xml version)\n" +
            " - json_v1 (JSON replacement for XML)\n",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(BindCollector, self).get_default_config()
        config.update({
            'host': 'localhost',
            'port': 8080,
            'path': 'bind',
            # Available stats:
            # - resolver (Per-view resolver and cache statistics)
            # - server (Incoming requests and their answers)
            # - zonemgmt (Requests/responses related to zone management)
            # - sockets (Socket statistics)
            # - memory (Global memory usage)
            'publish': [
                'resolver',
                'server',
                'zonemgmt',
                'sockets',
                'memory',
            ],
            # By default we don't publish these special views
            'publish_view_bind': False,
            'publish_view_meta': False,
            'data_format': 'xml_v2',
        })
        return config

    def clean_counter(self, name, value):
        value = self.derivative(name, value)
        if value < 0:
            value = 0
        self.publish(name, value)

    def collect(self):
        if self.config['data_format'] == 'json_v1':
            return self.collect_json_v1()
        if self.config['data_format'] == 'xml_v3':
            return self.collect_xml_v3()
        if self.config['data_format'] == 'xml_v2':
            return self.collect_xml_v2()

    def collect_json_v1(self):
        try:
            # Try newest interface first (JSON has least impact)
            import json
            req = urllib2.urlopen('http://%s:%d/json/v1/status' % (
                self.config['host'], int(self.config['port'])))
        except Exception, e:
            self.log.error('JSON v1 not supported: %s', e)
            return {}

        if 'server' in self.config['publish']:
            try:
                req = urllib2.urlopen('http://%s:%d/json/v1/server' % (
                    self.config['host'], int(self.config['port'])))
            except Exception, e:
                self.log.error('Couldnt connect to bind: %s', e)
                return {}

            response = json.load(req)
            self.parse_json_v1_server(response)

    def collect_xml_v3(self):
        try:
            # Try newer interface first
            req = urllib2.urlopen('http://%s:%d/xml/v3/status' % (
                self.config['host'], int(self.config['port'])))
        except Exception, e:
            self.log.error('XML v3 not supported: %s', e)
            return {}

        if 'server' in self.config['publish']:
            try:
                req = urllib2.urlopen('http://%s:%d/xml/v3/server' % (
                    self.config['host'], int(self.config['port'])))
            except Exception, e:
                self.log.error('Couldnt connect to bind: %s', e)
                return {}
            # Proceed with v3 parsing
            tree = ElementTree.parse(req)

            if not tree:
                raise ValueError("Corrupt XML file, no statistics found")

            self.parse_xml_v3_server(tree)

    def collect_xml_v2(self):
        try:
            # NOTE: Querying this node on a large server can impact bind
            # answering queriesfor sometimes hundreds of milliseconds.
            req = urllib2.urlopen('http://%s:%d/' % (
                self.config['host'], int(self.config['port'])))
        except Exception, e:
            self.log.error('Couldnt connect to bind: %s', e)
            return {}

        tree = ElementTree.parse(req)

        if not tree:
            raise ValueError("Corrupt XML file, no statistics found")

        root = tree.find('bind/statistics')

        if not root:
            raise ValueError(
                "Missing bind/statistics tree - Wrong data_format?")

        if 'resolver' in self.config['publish']:
            for view in root.findall('views/view'):
                name = view.find('name').text
                if name == '_bind' and not self.config['publish_view_bind']:
                    continue
                if name == '_meta' and not self.config['publish_view_meta']:
                    continue
                nzones = len(view.findall('zones/zone'))
                self.publish('view.%s.zones' % name, nzones)
                for counter in view.findall('rdtype'):
                    self.clean_counter(
                        'view.%s.query.%s' % (name,
                                              counter.find('name').text),
                        int(counter.find('counter').text)
                    )
                for counter in view.findall('resstat'):
                    self.clean_counter(
                        'view.%s.resstat.%s' % (name,
                                                counter.find('name').text),
                        int(counter.find('counter').text)
                    )
                for counter in view.findall('cache/rrset'):
                    self.clean_counter(
                        'view.%s.cache.%s' % (
                            name, counter.find('name').text.replace('!',
                                                                    'NOT_')),
                        int(counter.find('counter').text)
                    )

        if 'server' in self.config['publish']:
            for counter in root.findall('server/requests/opcode'):
                self.clean_counter(
                    'requests.%s' % counter.find('name').text,
                    int(counter.find('counter').text)
                )
            for counter in root.findall('server/queries-in/rdtype'):
                self.clean_counter(
                    'queries.%s' % counter.find('name').text,
                    int(counter.find('counter').text)
                )
            for counter in root.findall('server/nsstat'):
                self.clean_counter(
                    'nsstat.%s' % counter.find('name').text,
                    int(counter.find('counter').text)
                )

        if 'zonemgmt' in self.config['publish']:
            for counter in root.findall('server/zonestat'):
                self.clean_counter(
                    'zonestat.%s' % counter.find('name').text,
                    int(counter.find('counter').text)
                )

        if 'sockets' in self.config['publish']:
            for counter in root.findall('server/sockstat'):
                self.clean_counter(
                    'sockstat.%s' % counter.find('name').text,
                    int(counter.find('counter').text)
                )

        if 'memory' in self.config['publish']:
            for counter in root.find('memory/summary').getchildren():
                self.publish(
                    'memory.%s' % counter.tag,
                    int(counter.text)
                )

    def parse_xml_v3_server(self, root):
        for counters in root.findall('server/counters'):
            for counter in counters:
                self.clean_counter(
                    'server.counters.%s.%s' % (counters.attrib['type'],
                                               counter.attrib['name']),
                    int(counter.text)
                )

        for view in root.findall('views/view'):
            for counters in view.iter('counters'):
                for counter in counters:
                    self.clean_counter(
                        'views.%s.counters.%s.%s' % (view.attrib['name'],
                                                     counters.attrib['type'],
                                                     counter.attrib['name']),
                        int(counter.text)
                    )

    def parse_json_v1_server(self, response):
        for counter_metric_name in [
            'nsstat', 'opcode', 'qtype', 'rcode', 'zonestat'
        ]:
            for counter in response[counter_metric_name+'s']:
                self.clean_counter(
                    'server.counters.%s.%s' % (counter_metric_name, counter),
                    int(response[counter_metric_name+'s'][counter])
                )

        for view in response['views']:
            for counters in response['views'][view]:
                # This mapping maps from XML v3 layout to JSON v1
                for section_name in response['views'][view]['resolver']:
                    for counter in \
                            response['views'][view]['resolver'][section_name]:
                        self.clean_counter(
                            'views.%s.counters.%s.%s' %
                            (view, section_name, counter),
                            int(response['views'][view]['resolver']
                                [section_name][counter])
                            )
