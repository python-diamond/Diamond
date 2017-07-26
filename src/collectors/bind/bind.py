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
            'publish_zeros': True
        })
        return config

    def clean_counter(self, name, value):
        # Since all values are counters zero here means that this event had never occured
        if value <= 0 and not self.config['publish_zeros']:
            return

        self.publish_counter(name, value, time_delta=False, allow_negative=False)

    def collect(self):
        try:
            req = urllib2.urlopen('http://%s:%d/' % (
                self.config['host'], int(self.config['port'])))
        except Exception, e:
            self.log.error('Couldnt connect to bind: %s', e)
            return {}

        tree = ElementTree.parse(req)

        if not tree:
            raise ValueError("Corrupt XML file, no statistics found")

        root = tree.getroot() if tree.getroot().tag == 'statistics' else tree.find('statistics')
        version = int(root.get('version', '').split('.')[0])

        if version == 2:
            self.collect_v2(root)
        elif version == 3:
            self.collect_v3(root)
        else:
            raise ValueError("Unsupported statistics version")

    def collect_v3(self, root):
        if 'resolver' in self.config['publish']:
            for view in root.findall('views/view'):
                name = view.get('name')

                if name == '_bind' and not self.config['publish_view_bind']:
                    continue

                if name == '_meta' and not self.config['publish_view_meta']:
                    continue

                nzones = len(view.findall('zones/zone'))
                self.publish('view.%s.zones' % name, nzones)

                for counter in view.findall('counters[@type="resstats"/counter'):
                    self.clean_counter(
                        'view.%s.resstats.%s' % (name, counter.get('name')),
                        int(counter.text)
                    )

                for counter in view.findall('counters[@type="cachestats"]/counter'):
                    self.clean_counter(
                        'view.%s.cache.%s' % (name, counter.get('name')),
                        int(counter.text)
                    )

        if 'server' in self.config['publish']:
            for counter in root.findall('server/counters[@type="opcode"]/counter'):
                self.clean_counter(
                    'requests.%s' % counter.get('name'),
                    int(counter.text)
                )

            for counter in root.findall('server/counters[@type="qtype"]/counter'):
                self.clean_counter(
                    'queries.%s' % counter.get('name'),
                    int(counter.text)
                )

            for counter in root.findall('server/counters[@type="nsstat"]/counter'):
                self.clean_counter(
                    'nsstat.%s' % counter.get('name'),
                    int(counter.text)
                )

        if 'zonemgmt' in self.config['publish']:
            for counter in root.findall('server/counters[@type="zonestat"]/counter'):
                self.clean_counter(
                    'zonestat.%s' % counter.get('name'),
                    int(counter.text)
                )


        if 'sockets' in self.config['publish']:
            for counter in root.findall('server/counters[@type="sockstat"]/counter'):
                self.clean_counter(
                    'sockstat.%s' % counter.get('name'),
                    int(counter.text)
                )

        if 'memory' in self.config['publish']:
            for counter in root.find('memory/summary').getchildren():
                self.publish(
                    'memory.%s' % counter.tag,
                    int(counter.text)
                )

    def collect_v2(self, root):
        if 'resolver' in self.config['publish']:
            for view in root.findall('views/view'):
                name = view.find('name').text

                if name == '_bind' and not self.config['publish_view_bind']:
                    continue

                if name == '_meta' and not self.config['publish_view_meta']:
                    continue

                nzones = len(view.findall('zones/zone'))
                self.publish('view.%s.zones' % name, nzones)

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
