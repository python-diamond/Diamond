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
from contextlib import closing
import json
import re
import urllib
import urllib2


class JolokiaCollector(diamond.collector.Collector):

    LIST_URL = "/list"

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
            'domains': "Pipe delimited list of JMX domains from which to"
                       " collect stats. If not provided, the list of all"
                       " domains will be downloaded from jolokia.",
            'mbeans':  "Pipe delimited list of MBeans for which to collect"
                       " stats. If not provided, all stats will"
                       " be collected.",
            'regex': "Contols if mbeans option matches with regex,"
                       " False by default.",
            'username': "Username for authentication",
            'password': "Password for authentication",
            'host': 'Hostname',
            'port': 'Port',
            'rewrite': "This sub-section of the config contains pairs of"
                       " from-to regex rewrites.",
            'path': 'Path component of the reported metrics.',
            # https://github.com/rhuss/jolokia/blob/959424888a82abc2b1906c60547cd4df280f3b71/client/java/src/main/java/org/jolokia/client/request/J4pQueryParameter.java#L68
            'use_canonical_names': 'Whether property keys of ObjectNames'
                                   ' should be ordered in the canonical way'
                                   ' or in the way that they are created. The'
                                   ' allowed values are either "True" in'
                                   ' which case the canonical key order (=='
                                   ' alphabetical sorted) is used or "False"'
                                   ' for getting the keys as registered.'
                                   ' Default is "True',
            'jolokia_path': 'Path to jolokia.  typically "jmx" or "jolokia".'
                            ' Defaults to the value of "path" variable.',
        })
        return config_help

    def get_default_config(self):
        config = super(JolokiaCollector, self).get_default_config()
        config.update({
            'mbeans': [],
            'regex': False,
            'rewrite': [],
            'path': 'jolokia',
            'jolokia_path': None,
            'username': None,
            'password': None,
            'host': 'localhost',
            'port': 8778,
            'use_canonical_names': True,
        })
        return config

    def __init__(self, *args, **kwargs):
        super(JolokiaCollector, self).__init__(*args, **kwargs)
        self.mbeans = []
        if isinstance(self.config['mbeans'], basestring):
            for mbean in self.config['mbeans'].split('|'):
                self.mbeans.append(mbean.strip())
        elif isinstance(self.config['mbeans'], list):
            self.mbeans = self.config['mbeans']
        if self.config['regex'] is not None:
            self.mbeans = [re.compile(mbean) for mbean in self.mbeans]

        self.rewrite = [
            (re.compile('["\'(){}<>\[\]]'), ''),
            (re.compile('[:,.]+'), '.'),
            (re.compile('[^a-zA-Z0-9_.+-]+'), '_'),
        ]
        if isinstance(self.config['rewrite'], dict):
            self.rewrite.extend([(re.compile(old), new) for old, new in
                                 self.config['rewrite'].items()])

        self.domains = []
        if 'domains' in self.config:
            if isinstance(self.config['domains'], basestring):
                for domain in self.config['domains'].split('|'):
                    self.domains.append(domain.strip())
            elif isinstance(self.config['domains'], list):
                self.domains = self.config['domains']

        if self.config['jolokia_path'] is not None:
            self.jolokia_path = self.config['jolokia_path']
        else:
            self.jolokia_path = self.config['path']

    def _get_domains(self):
        # if not set it __init__
        if not self.domains:
            listing = self._list_request()
            try:
                if listing['status'] == 200:
                    self.domains = listing['value'].keys()
                else:
                    self.log.error('Jolokia status %s while retrieving MBean '
                                   'listing.', listing['status'])
            except KeyError:
                # The reponse was totally empty, or not an expected format
                self.log.error('Unable to retrieve MBean listing.')

    def _check_mbean(self, mbean):
        if not self.mbeans:
            return True
        mbeanfix = self.clean_up(mbean)
        if self.config['regex'] is not None:
            for chkbean in self.mbeans:
                if chkbean.match(mbean) is not None or \
                   chkbean.match(mbeanfix) is not None:
                    return True
        else:
            if mbean in self.mbeans or mbeanfix in self.mbeans:
                return True

    def collect(self):
        if not self.domains:
            self._get_domains()
        for domain in self.domains:
            if domain not in self.IGNORE_DOMAINS:
                obj = self._read_request(domain)
                try:
                    mbeans = obj['value'] if obj['status'] == 200 else {}
                except KeyError:
                    # The reponse was totally empty, or not an expected format
                    self.log.error('Unable to retrieve domain %s.', domain)
                    continue
                for k, v in mbeans.iteritems():
                    if self._check_mbean(k):
                        self.collect_bean(k, v)

    def _read_json(self, request):
        json_str = request.read()
        return json.loads(json_str)

    def _list_request(self):
        """Returns a dictionary with JMX domain names as keys"""
        try:
            # https://jolokia.org/reference/html/protocol.html
            #
            # A maxDepth of 1 restricts the return value to a map with the JMX
            # domains as keys. The values of the maps don't have any meaning
            # and are dummy values.
            #
            # maxCollectionSize=0 means "unlimited". This works around an issue
            # prior to Jolokia 1.3 where results were truncated at 1000
            #
            url = "http://%s:%s/%s%s?maxDepth=1&maxCollectionSize=0" % (
                self.config['host'],
                self.config['port'],
                self.jolokia_path,
                self.LIST_URL)
            # need some time to process the downloaded metrics, so that's why
            # timeout is lower than the interval.
            timeout = max(2, float(self.config['interval']) * 2 / 3)
            with closing(urllib2.urlopen(self._create_request(url),
                                         timeout=timeout)) as response:
                return self._read_json(response)
        except (urllib2.HTTPError, ValueError) as e:
            self.log.error('Unable to read JSON response: %s', str(e))
            return {}

    def _read_request(self, domain):
        try:
            url_path = '/?%s' % urllib.urlencode({
                'maxCollectionSize': '0',
                'ignoreErrors': 'true',
                'canonicalNaming':
                    'true' if self.config['use_canonical_names'] else 'false',
                'p': 'read/%s:*' % self._escape_domain(domain),
            })
            url = "http://%s:%s/%s%s" % (self.config['host'],
                                         self.config['port'],
                                         self.jolokia_path,
                                         url_path)
            # need some time to process the downloaded metrics, so that's why
            # timeout is lower than the interval.
            timeout = max(2, float(self.config['interval']) * 2 / 3)
            with closing(urllib2.urlopen(self._create_request(url),
                                         timeout=timeout)) as response:
                return self._read_json(response)
        except (urllib2.HTTPError, ValueError):
            self.log.error('Unable to read JSON response.')
            return {}

    # escape JMX domain per https://jolokia.org/reference/html/protocol.html
    # the Jolokia documentation suggests that when using the p query parameter,
    # simply urlencoding should be sufficient, but in practice, the '!' appears
    # necessary (and not harmful)
    def _escape_domain(self, domain):
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
        for (oldregex, newstr) in self.rewrite:
            text = oldregex.sub(newstr, text)
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
