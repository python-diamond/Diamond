<!--This file was generated from the python source
Please edit the source to make changes
-->
TSDBHandler
====

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

The handler per default adds a tag 'hostname' with the hostname where the
collection took place. You can add as many as you like via the configuration.
The 'tags' config element allows for both comma-separated or space separated
key value pairs.

The collectors specify the metrics with a single axis of navigation and often
include aggregation counters that OpenTSDB could calculate directly. The openTSDB
tagging system supports multiple axis and is better suited for dynamical values.
You can [read here](http://opentsdb.net/docs/build/html/user_guide/query/timeseries.html)
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
in your [OpenTSDB configuration](http://opentsdb.net/docs/build/html/user_guide/configuration.html)
or you can run with the null handler and log the output
and extract the key values to mkmetric yourself  

- enable it in `diamond.conf` :

`    handlers = diamond.handler.tsdb.TSDBHandler
`

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
format | {Collector}.{Metric} {timestamp} {value} hostname={host}{tags} |  | str
get_default_config_help |  | get_default_config_help |
host |  |  | str
port | 1234 |  | int
server_error_interval | 120 | How frequently to send repeated server errors | int
tags |  | Tags to be added to each metric. They should be key/value pairs. Example : tags = environment=test,datacenter=north| str
timeout | 5 |  | int
cleanMetrics| True | Extract tag values from known collectors and make the metrics more OpenTSDB style | bool
skipAggregates| True | Only has effect when cleanMetrics is true. Then the metrics that are considered aggregates are removed | bool
