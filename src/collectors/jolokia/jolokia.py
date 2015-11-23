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
will be queried for metrics.  Note that the mbean prefix is checked both
with and without rewrites (including fixup re-writes) applied.  This allows
you to specify "java.lang:name=ParNew,type=GarbageCollector" (the raw name from
jolokia) or "java.lang.name_ParNew.type_GarbageCollector" (the fixed name
as used for output)

If the ```regex``` flag is set to True, mbeans will match based on regular
expressions rather than a plain textual match.

The ```rewrite``` section provides a way of renaming the data keys before
it sent out to the handler.  The section consists of pairs of from-to
regular expressions.  If the resultant name is completely blank, the
metric is not published, providing a way to exclude specific metrics within
an mbean.

```
    host = localhost
    port = 8778
    mbeans = "java.lang:name=ParNew,type=GarbageCollector",
     "org.apache.cassandra.metrics:name=WriteTimeouts,type=ClientRequestMetrics"
    [rewrite]
    java = coffee
    "-v\d+\.\d+\.\d+" = "-AllVersions"
    ".*GetS2Activities.*" = ""
```
"""

import diamond.collector
import base64
import json
import re
import urllib
import urllib2


class JolokiaCollector(diamond.collector.Collector):

    LIST_URL = "/list"
    READ_URL = "/?ignoreErrors=true&p=read/%s:*"

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
            'mbeans':  "Pipe delimited list of MBeans for which to collect"
                       " stats. If not provided, all stats will"
                       " be collected.",
            'regex': "Contols if mbeans option matches with regex,"
                       " False by default.",
            'username': None,
            'password': None,
            'host': 'Hostname',
            'port': 'Port',
            'rewrite': "This sub-section of the config contains pairs of"
                       " from-to regex rewrites.",
            'path': 'Path to jolokia.  typically "jmx" or "jolokia"'
        })
        return config_help

    def get_default_config(self):
        config = super(JolokiaCollector, self).get_default_config()
        config.update({
            'mbeans': [],
            'regex': False,
            'rewrite': [],
            'path': 'jolokia',
            'username': None,
            'password': None,
            'host': 'localhost',
            'port': 8778,
        })
        return config

    def __init__(self, *args, **kwargs):
        super(JolokiaCollector, self).__init__(*args, **kwargs)
        self.mbeans = []
        self.rewrite = {}
        if isinstance(self.config['mbeans'], basestring):
            for mbean in self.config['mbeans'].split('|'):
                self.mbeans.append(mbean.strip())
        elif isinstance(self.config['mbeans'], list):
            self.mbeans = self.config['mbeans']
        if isinstance(self.config['rewrite'], dict):
            self.rewrite = self.config['rewrite']

    def check_mbean(self, mbean):
        if not self.mbeans:
            return True
        mbeanfix = self.clean_up(mbean)
        if self.config['regex'] is not None:
            for chkbean in self.mbeans:
                if re.match(chkbean, mbean) is not None or \
                   re.match(chkbean, mbeanfix) is not None:
                    return True
        else:
            if mbean in self.mbeans or mbeanfix in self.mbeans:
                return True

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
            url = "http://%s:%s/%s%s" % (self.config['host'],
                                         self.config['port'],
                                         self.config['path'],
                                         self.LIST_URL)
            response = urllib2.urlopen(self._create_request(url))
            return self.read_json(response)
        except (urllib2.HTTPError, ValueError):
            self.log.error('Unable to read JSON response.')
            return {}

    def read_request(self, domain):
        try:
            url_path = self.READ_URL % self.escape_domain(domain)
            url = "http://%s:%s/%s%s" % (self.config['host'],
                                         self.config['port'],
                                         self.config['path'],
                                         url_path)
            response = urllib2.urlopen(self._create_request(url))
            return self.read_json(response)
        except (urllib2.HTTPError, ValueError):
            self.log.error('Unable to read JSON response.')
            return {}

    # escape the JMX domain per https://jolokia.org/reference/html/protocol.html
    # the Jolokia documentation suggests that, when using the p query parameter,
    # simply urlencoding should be sufficient, but in practice, the '!' appears
    # necessary (and not harmful)
    def escape_domain(self, domain):
        domain = re.sub('!', '!!', domain)
        domain = re.sub('/', '!/', domain)
        domain = re.sub('"', '!"', domain)
        domain = urllib.quote(domain)
        return domain

    def _create_request(self, url):
        req = urllib2.Request(url)
        username = self.config["username"]
        password = self.config["password"]
        if username is not None and password is not None:
            base64string = base64.encodestring('%s:%s' % (
                username, password)).replace('\n', '')
            req.add_header("Authorization", "Basic %s" % base64string)
        return req

    def clean_up(self, text):
        text = re.sub('["\'(){}<>\[\]]', '', text)
        text = re.sub('[:,.]+', '.', text)
        text = re.sub('[^a-zA-Z0-9_.+-]+', '_', text)
        for (oldstr, newstr) in self.rewrite.items():
            text = re.sub(oldstr, newstr, text)
        return text

    def collect_bean(self, prefix, obj):
        for k, v in obj.iteritems():
            if type(v) in [int, float, long]:
                key = "%s.%s" % (prefix, k)
                key = self.clean_up(key)
                if key != "":
                    self.publish(key, v)
            elif type(v) in [dict]:
                self.collect_bean("%s.%s" % (prefix, k), v)
            elif type(v) in [list]:
                self.interpret_bean_with_list("%s.%s" % (prefix, k), v)

    # There's no unambiguous way to interpret list values, so
    # this hook lets subclasses handle them.
    def interpret_bean_with_list(self, prefix, values):
        pass
