<!--This file was generated from the python source
Please edit the source to make changes
-->
TSDBHandler
=====

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


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
batch | 1 | Amount of metrics to send at once | int
cleanMetrics| True | Extract tag values from known collectors and make the metrics more OpenTSDB style | bool
compression | 0 | compression level 1 (low) - 9 (high) | int
get_default_config_help |  | get_default_config_help |
host |  |  | str
password | | password for Basic Authorization | str
port | 4242 |  | int
prefix | | Is added as a prefix for every metric example: 'diamond' -> diamond.metric.name | str
skipAggregates| True | Only has effect when cleanMetrics is true. Then the metrics that are considered aggregates are removed | bool
tags |  | Tags to be added to each metric| str
timeout | 5 |  | int
user | | user for Basic Authorization | str
