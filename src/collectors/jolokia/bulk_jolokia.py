# coding=utf-8

"""
 Collects JMX metrics from the Jolokia Agent. Jolokia is an HTTP bridge that
provides access to JMX MBeans without the need to write Java code. See the
[Reference Guide](http://www.jolokia.org/reference/html/index.html) for more
information.

The liste MBean patterns will be queried for metrics. All numerical values will
be published to Graphite; anything else will be ignored.
The JolokiaBulkCollector will create a reasonable namespace for each metric
based on each MBeans domain and name.
e.g) ```java.lang:name=ParNew,type=GarbageCollector``` would become
```java.lang.name_ParNew.type_GarbageCollector```.

#### Dependencies

 * Jolokia
 * A running JVM with Jolokia installed/configured

#### Example Configuration

JolokiaBulkCollector is configured to query specific MBeans by
providing a list of ```mbeans```. The list of mbeans may include the
wildcard '*' character, or any other valid Jolokia pattern
(see https://jolokia.org/reference/html/protocol.html#read).

The ```rewrite``` section provides a way of renaming the data keys before
it sent out to the handler.  The section consists of pairs of from-to
regular expressions.  If the resultant name is completely blank, the
metric is not published, providing a way to exclude specific metrics within
an mbean.

```
    host = localhost
    port = 8778
    mbeans = "java.lang:*,type=GarbageCollector",
    [rewrite]
    java = coffee
    "-v\d+\.\d+\.\d+" = "-AllVersions"
    ".*GetS2Activities.*" = ""
```
"""

import base64
import json
import urllib
import urllib2

from jolokia import JolokiaCollector


class JolokiaBulkCollector(JolokiaCollector):
    # override to allow setting which percentiles will be collected
    def get_default_config_help(self):
        config_help = super(JolokiaBulkCollector,
                            self).get_default_config_help()
        config_help.update({
            'mbeans': 'Comma separated list of mbean patterns to collect',
        })
        del config_help['regex']
        return config_help

    # override to allow setting which percentiles will be collected
    def get_default_config(self):
        config = super(JolokiaBulkCollector, self).get_default_config()
        config.update({
            'user': False,
            'passwd': False,
            'user-agent': False,
        })
        return config

    def __init__(self, *args, **kwargs):
        super(JolokiaBulkCollector, self).__init__(*args, **kwargs)

    def collect(self):
        requests = self.fetch_response()

        for listing in requests:
            if listing['status'] == 200:
                domains = listing['value']
                for domain in domains.keys():
                    if domain not in self.IGNORE_DOMAINS:
                        self.collect_bean(domain, domains[domain])
            else:
                logging.critical("%s(%s) : %s", listing['request'], listing['error_type'], listing['error'])

    def fetch_response(self):
        path = self.config['path']

        if not(path.endswith('/')):
            path = path + '/'

        url = "http://%s:%s/%s?ignoreErrors=true" % (self.config['host'],
                                                     self.config['port'],
                                                     path)

        data = []

        for mbean in self.config['mbeans']:
            data.append({'type': 'read', 'mbean': mbean})

        headers = {'content-type': 'application/json'}

        request = urllib2.Request(url, json.dumps(data), headers)

        if self.config['user']:
            base64string = base64.encodestring('%s:%s' % (
                self.config['user'], self.config['passwd'])).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)

        if self.config['user-agent']:
            request.add_header("User-Agent", self.config['user-agent'])

        response = urllib2.urlopen(request)
        return self.read_json(response)
