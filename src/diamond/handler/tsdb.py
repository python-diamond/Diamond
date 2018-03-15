# coding=utf-8

"""
Send metrics to a [OpenTSDB](http://opentsdb.net/) server.

[OpenTSDB](http://opentsdb.net/) is a distributed, scalable Time Series
Database (TSDB) written on top of [HBase](http://hbase.org/). OpenTSDB was
written to address a common need: store, index and serve metrics collected from
computer systems (network gear, operating systems, applications) at a large
scale, and make this data easily accessible and graphable.

Thanks to HBase's scalability, OpenTSDB allows you to collect many thousands of
metrics from thousands of hosts and applications, at a high rate (every few
seconds). OpenTSDB will never delete or downsample data and can easily store
billions of data points. As a matter of fact, StumbleUpon uses it to keep track
of hundred of thousands of time series and collects over 1 billion data points
per day in their main production datacenter.

Imagine having the ability to quickly plot a graph showing the number of DELETE
statements going to your MySQL database along with the number of slow queries
and temporary files created, and correlate this with the 99th percentile of
your service's latency. OpenTSDB makes generating such graphs on the fly a
trivial operation, while manipulating millions of data point for very fine
grained, real-time monitoring.

The system per default adds a tag 'hostname' with the hostname where the
collection took place. You can add as many as you like. The 'tags' config
element allows space separated key value pairs.

Example :
tags = environment=test datacenter=north

The collectors specify the metrics with a single axis of navigation and often
include aggregation counters that OpenTSDB could calculate directly.
The openTSDB tagging system supports multiple axis and is better suited
for dynamical values. You can [read here]
(http://opentsdb.net/docs/build/html/user_guide/query/timeseries.html)
how OpenTSDB suggests to sepearate tags from metrics. when doing this you also
want to remove these aggregate values since they would lead to double counting
when requesting OpenTSDB to do the aggregation based on the tags.

The handler currently provides the ability to extract the tags from a metric
(and remove aggregate values) for following collectors :
* CPUCollector
* HaProxyCollector
* MattermostCollector


==== Notes

We don't automatically make the metrics via **mkmetric**, so either set
```
set tsd.core.auto_create_metrics = true
```
in your [OpenTSDB configuration]
(http://opentsdb.net/docs/build/html/user_guide/configuration.html)
or you can run with the null handler and log the output
and extract the key values to mkmetric yourself

- enable it in `diamond.conf` :

`    handlers = diamond.handler.tsdb.TSDBHandler
`
We will automatically split bigger packages of metrics. You have to set
tsd.http.request.enable_chunked = true
and if pakackes get to big you will also need to adjust
tsd.http.request.max_chunk which is 4096 by default. Learn more
[here](http://opentsdb.net/docs/build/html/user_guide/configuration.html).

In your diamond.conf:

You can define how many packages you want to send in one package by setting
batch<=1. We dont recommend 1 as it may have bigger impact on your CPU.

Compression can be enabled by setting compression to 1-9 while 1 is low and 9 is
high.

"""

from Handler import Handler
from diamond.metric import Metric
import urllib2
import StringIO
import gzip
import base64
import json
import re
import contextlib


class TSDBHandler(Handler):
    """
    Implements the abstract Handler class, sending data to OpenTSDB
    """

    def __init__(self, config=None):
        """
        Create a new instance of the TSDBHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)

        # Initialize Options
        # host
        self.host = str(self.config['host'])
        self.port = int(self.config['port'])
        self.timeout = int(self.config['timeout'])
        # Authorization
        self.user = str(self.config['user'])
        self.password = str(self.config['password'])
        # data
        self.batch = int(self.config['batch'])
        self.compression = int(self.config['compression'])
        # prefix
        if self.config['prefix'] != "":
            self.prefix = str(self.config['prefix'])+'.'
        else:
            self.prefix = ""
        # tags
        self.tags = []
        pattern = re.compile(r'([a-zA-Z0-9]+)=([a-zA-Z0-9]+)')
        for (key, value) in re.findall(pattern, str(self.config['tags'])):
            self.tags.append([key, value])

        # headers
        self.httpheader = {"Content-Type": "application/json"}
        # Authorization
        if self.user != "":
            self.httpheader["Authorization"] = "Basic " +\
                base64.encodestring('%s:%s' % (self.user, self.password))[:-1]
        # compression
        if self.compression >= 1:
            self.httpheader["Content-Encoding"] = "gzip"
        self.entrys = []

        self.skipAggregates = self.config['skipAggregates']
        self.cleanMetrics = self.config['cleanMetrics']

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(TSDBHandler, self).get_default_config_help()

        config.update({
            'host': '',
            'port': '',
            'timeout': '',
            'tags': '',
            'prefix': '',
            'batch': '',
            'compression': '',
            'user': '',
            'password': '',
            'cleanMetrics': True,
            'skipAggregates': True,
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(TSDBHandler, self).get_default_config()

        config.update({
            'host': '127.0.0.1',
            'port': 4242,
            'timeout': 5,
            'tags': '',
            'prefix': '',
            'batch': 1,
            'compression': 0,
            'user': '',
            'password': '',
            'cleanMetrics': True,
            'skipAggregates': True,
        })

        return config

    def __del__(self):
        """
        Destroy instance of the TSDBHandler class
        """
        self.log.debug("Stopping TSDBHandler ...")

    def process(self, metric):
        """
        Process a metric by sending it to TSDB
        """
        entry = {'timestamp': metric.timestamp, 'value': metric.value,
                 "tags": {}}
        entry["tags"]["hostname"] = metric.host

        if self.cleanMetrics:
            metric = MetricWrapper(metric, self.log)
            if self.skipAggregates and metric.isAggregate():
                return
            for tagKey in metric.getTags():
                entry["tags"][tagKey] = metric.getTags()[tagKey]

        entry['metric'] = (self.prefix + metric.getCollectorPath() +
                           '.' + metric.getMetricPath())

        for [key, value] in self.tags:
            entry["tags"][key] = value

        self.entrys.append(entry)

        # send data if list is long enough
        if (len(self.entrys) >= self.batch):
            # Compress data
            if self.compression >= 1:
                data = StringIO.StringIO()
                with contextlib.closing(gzip.GzipFile(fileobj=data,
                                        compresslevel=self.compression,
                                        mode="w")) as f:
                    f.write(json.dumps(self.entrys))
                self._send(data.getvalue())
            else:
                # no compression
                data = json.dumps(self.entrys)
                self._send(data)

    def _send(self, content):
        """
        Send content to TSDB.
        """
        retry = 0
        success = False
        while retry < 3 and success is False:
            self.log.debug(content)
            try:
                request = urllib2.Request("http://"+self.host+":" +
                                          str(self.port)+"/api/put",
                                          content, self.httpheader)
                response = urllib2.urlopen(url=request, timeout=self.timeout)
                if response.getcode() < 301:
                    self.log.debug(response.read())
                    # Transaction should be finished
                    self.log.debug(response.getcode())
                    success = True
            except urllib2.HTTPError as e:
                self.log.error("HTTP Error Code: "+str(e.code))
                self.log.error("Message : "+str(e.reason))
            except urllib2.URLError as e:
                self.log.error("Connection Error: "+str(e.reason))
            finally:
                retry += 1
        self.entrys = []


"""
This class wraps a metric and applies the additonal OpenTSDB tagging logic.
"""


class MetricWrapper(Metric):

    def isAggregate(self):
        return self.aggregate

    def getTags(self):
        return self.tags

    """
    This method does nothing and therefore keeps the existing metric unchanged.
    """
    def processDefaultMetric(self):
        self.tags = {}
        self.aggregate = False

    """
    Processes a metric of the CPUCollector. It stores the cpuId in a tag and
    marks all metrics with 'total' as aggregates, so they can be skipped if
    the skipAggregates feature is active.
    """
    def processCpuMetric(self):
        if len(self.getMetricPath().split('.')) > 1:
            self.aggregate = self.getMetricPath().split('.')[0] == 'total'

            cpuId = self.delegate.getMetricPath().split('.')[0]
            self.tags["cpuId"] = cpuId
            self.path = self.path.replace("."+cpuId+".", ".")
    """
    Processes metrics of the HaProxyCollector. It stores the backend and the
    server to which the backends send as tags. Counters with 'backend' as
    backend name are considered aggregates.
    """
    def processHaProxyMetric(self):
        if len(self.getMetricPath().split('.')) == 3:
            self.aggregate = self.getMetricPath().split('.')[1] == 'backend'

            backend = self.delegate.getMetricPath().split('.')[0]
            server = self.delegate.getMetricPath().split('.')[1]
            self.tags["backend"] = backend
            self.tags["server"] = server
            self.path = self.path.replace("."+server+".", ".")
            self.path = self.path.replace("."+backend+".", ".")

    """
    Processes metrics of the DiskspaceCollector. It stores the mountpoint as a
    tag. There are no aggregates in this collector.
    """
    def processDiskspaceMetric(self):
        if len(self.getMetricPath().split('.')) == 2:

            mountpoint = self.delegate.getMetricPath().split('.')[0]

            self.tags["mountpoint"] = mountpoint
            self.path = self.path.replace("."+mountpoint+".", ".")

    """
    Processes metrics of the DiskusageCollector. It stores the device as a
    tag. There are no aggregates in this collector.
    """
    def processDiskusageMetric(self):
        if len(self.getMetricPath().split('.')) == 2:

            device = self.delegate.getMetricPath().split('.')[0]

            self.tags["device"] = device
            self.path = self.path.replace("."+device+".", ".")

    """
    Processes metrics of the NetworkCollector. It stores the interface as a
    tag. There are no aggregates in this collector.
    """
    def processNetworkMetric(self):
        if len(self.getMetricPath().split('.')) == 2:

            interface = self.delegate.getMetricPath().split('.')[0]

            self.tags["interface"] = interface
            self.path = self.path.replace("."+interface+".", ".")

    def processMattermostMetric(self):
        split = self.getMetricPath().split('.')
        if len(split) > 2:
            if split[0] == 'teamdetails' or split[0] == 'channeldetails':
                team = split[1]
                self.tags["team"] = team
                self.path = self.path.replace("."+team+".", ".")
                # fall through for channeldetails
            if split[0] == 'channeldetails':
                channel = split[2]
                self.tags["channel"] = channel
                self.path = self.path.replace("."+channel+".", ".")
            if split[0] == 'userdetails':
                user = split[1]
                team = split[2]
                channel = split[3]
                self.tags["user"] = user
                self.tags["team"] = team
                self.tags["channel"] = channel
                self.path = self.path.replace("."+user+".", ".")
                self.path = self.path.replace("."+team+".", ".")
                self.path = self.path.replace("."+channel+".", ".")

    handlers = {'cpu': processCpuMetric, 'haproxy': processHaProxyMetric,
                'mattermost': processMattermostMetric,
                'diskspace': processDiskspaceMetric,
                'iostat': processDiskusageMetric,
                'network': processNetworkMetric,
                'default': processDefaultMetric}

    def __init__(self, delegate, logger):
        self.path = delegate.path
        self.value = delegate.value
        self.host = delegate.host
        self.raw_value = delegate.raw_value
        self.timestamp = delegate.timestamp
        self.precision = delegate.precision
        self.ttl = delegate.ttl
        self.metric_type = delegate.metric_type
        self.delegate = delegate
        self.tags = {}
        self.aggregate = False
        self.newMetricName = None
        self.logger = logger
        # call the handler for that collector
        handler = self.handlers.get(self.getCollectorPath(),
                                    self.handlers['default'])
        handler(self)
