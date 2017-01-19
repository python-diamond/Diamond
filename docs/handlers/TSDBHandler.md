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

==== Notes

We don't automatically make the metrics via mkmetric, so we recommand you run
with the null handler and log the output and extract the key values to mkmetric
yourself.

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
tags |  |  | str
timeout | 5 |  | int
