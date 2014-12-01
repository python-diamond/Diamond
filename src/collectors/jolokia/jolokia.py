# coding=utf-8

"""
Collects JMX metrics from the Jolokia Agent. Jolokia is an HTTP bridge that
provides access to JMX MBeans without the need to write Java code. See the
[Reference Guide](http://www.jolokia.org/reference/html/index.html) for more
information.

By default, all MBeans will be queried for metrics. All numerical values will
be published to Graphite; anything else will be ignored. JolokiaCollector will
create a reasonable namespace for each metric based on each MBeans domain and
name. e.g) ```java.lang:name=ParNew,type=GarbageCollector``` would become
```java.lang.name_ParNew.type_GarbageCollector```.

#### Dependencies

 * Jolokia
 * A running JVM with Jolokia installed/configured

#### Example Configuration

If desired, JolokiaCollector can be configured to query specific MBeans by
providing a list of ```mbeans```. If ```mbeans``` is not provided, all MBeans
will be queried for metrics.

JolokiaCollector.conf

```
    host 'localhost'
    port '8778'
    mbeans '"java.lang:name=ParNew,type=GarbageCollector | org.apache.cassandra.metrics:name=WriteTimeouts,type=ClientRequestMetrics"'
```
"""

import diamond.collector
import json
import re
import urllib
import urllib2


class JolokiaCollector(diamond.collector.Collector):

    BASE_URL = "jolokia"
    LIST_URL = BASE_URL + "/list"
    READ_URL = BASE_URL + "/?ignoreErrors=true&p=read/%s:*"

    """
    These domains contain MBeans that are for management purposes,
    or otherwise do not contain useful metrics
    """
    IGNORE_DOMAINS = ['JMImplementation', 'jmx4perl', 'jolokia',
                      'com.sun.management', 'java.util.logging']

    def get_default_config_help(self):
        config_help = super(JolokiaCollector,
                            self).get_default_config_help()
        config_help.update({
            'mbeans': "Pipe delimited list of MBeans for which to collect "
            "stats. If not provided, all stats will be collected",
            'host': 'Hostname',
            'port': 'Port',
        })
        return config_help

    def get_default_config(self):
        config = super(JolokiaCollector, self).get_default_config()
        config.update({
            'mbeans': [],
            'path': 'jmx',
            'host': 'localhost',
            'port': 8778,
        })
        return config

    def process_config(self):
        self.mbeans = []
        if isinstance(self.config['mbeans'], basestring):
            for mbean in self.config['mbeans'].split('|'):
                self.mbeans.append(mbean.strip())
        elif isinstance(self.config['mbeans'], list):
            self.mbeans = self.config['mbeans']

    def check_mbean(self, mbean):
        if mbean in self.mbeans or not self.mbeans:
            return True
        else:
            return False

    def collect(self):
        listing = self.list_request()
        try:
            domains = listing['value'] if listing['status'] == 200 else {}
            for domain in domains.keys():
                if domain not in self.IGNORE_DOMAINS:
                    obj = self.read_request(domain)
                    mbeans = obj['value'] if obj['status'] == 200 else {}
                    for k, v in mbeans.iteritems():
                        if self.check_mbean(k):
                            self.collect_bean(k, v)
        except KeyError:
            # The reponse was totally empty, or not an expected format
            self.log.error('Unable to retrieve MBean listing.')

    def read_json(self, request):
        json_str = request.read()
        return json.loads(json_str)

    def list_request(self):
        try:
            url = "http://%s:%s/%s" % (self.config['host'],
                                       self.config['port'], self.LIST_URL)
            response = urllib2.urlopen(url)
            return self.read_json(response)
        except (urllib2.HTTPError, ValueError):
            self.log.error('Unable to read JSON response.')
            return {}

    def read_request(self, domain):
        try:
            url_path = self.READ_URL % urllib.quote(domain)
            url = "http://%s:%s/%s" % (self.config['host'],
                                       self.config['port'], url_path)
            response = urllib2.urlopen(url)
            return self.read_json(response)
        except (urllib2.HTTPError, ValueError):
            self.log.error('Unable to read JSON response.')
            return {}

    def clean_up(self, text):
        text = re.sub('[:,]', '.', text)
        text = re.sub('[=\s]', '_', text)
        text = re.sub('["\']', '', text)
        return text

    def collect_bean(self, prefix, obj):
        for k, v in obj.iteritems():
            if type(v) in [int, float, long]:
                key = "%s.%s" % (prefix, k)
                key = self.clean_up(key)
                self.publish(key, v)
            elif type(v) in [dict]:
                self.collect_bean("%s.%s" % (prefix, k), v)
