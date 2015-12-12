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


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

