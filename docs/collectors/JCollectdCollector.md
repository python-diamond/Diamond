<!--This file was generated from the python source
Please edit the source to make changes
-->
JCollectdCollector
=====

The JCollectdCollector is capable of receiving Collectd network traffic
as sent by the JCollectd jvm agent (and child Collectd processes).

Reason for developing this collector is allowing to use JCollectd, without
the need for Collectd.

A few notes:

This collector starts a UDP server to receive data. This server runs in
a separate thread and puts it on a queue, waiting for the collect() method
to pull. Because of this setup, the collector interval parameter is of
less importance. What matters is the 'sendinterval' JCollectd parameter.

See https://github.com/emicklei/jcollectd for an up-to-date jcollect fork.

#### Dependencies

 * jcollectd sending metrics


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
__EXAMPLESHERE__
```

