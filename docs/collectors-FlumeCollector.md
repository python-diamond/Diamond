FlumeCollector
=====

Collect statistics from Flume

#### Dependencies

 * urllib2
 * json or simplejson


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>req_host</td><td>localhost</td><td>Hostname</td><td>str</td></tr>
<tr><td>req_path</td><td>/metrics</td><td>Path</td><td>str</td></tr>
<tr><td>req_port</td><td>41414</td><td>Port</td><td>int</td></tr>
</table>

#### Example Output

```
servers.hostname.flume.CHANNEL.channel1.ChannelFillPercentage 0.0
servers.hostname.flume.CHANNEL.channel1.EventPutAttempt 50272828
servers.hostname.flume.CHANNEL.channel1.EventPutSuccess 50255318
servers.hostname.flume.CHANNEL.channel1.EventTakeAttempt 50409933
servers.hostname.flume.CHANNEL.channel1.EventTakeSuccess 50255318
servers.hostname.flume.SINK.sink1.BatchComplete 251705
servers.hostname.flume.SINK.sink1.BatchEmpty 76250
servers.hostname.flume.SINK.sink1.BatchUnderflow 379
servers.hostname.flume.SINK.sink1.ConnectionClosed 6
servers.hostname.flume.SINK.sink1.ConnectionCreated 7
servers.hostname.flume.SINK.sink1.ConnectionFailed 0
servers.hostname.flume.SINK.sink1.EventDrainAttempt 25190171
servers.hostname.flume.SINK.sink1.EventDrainSuccess 25189571
servers.hostname.flume.SOURCE.source1.AppendAccepted 0
servers.hostname.flume.SOURCE.source1.AppendBatchAccepted 56227
servers.hostname.flume.SOURCE.source1.AppendBatchReceived 56258
servers.hostname.flume.SOURCE.source1.AppendReceived 0
servers.hostname.flume.SOURCE.source1.EventAccepted 50282681
servers.hostname.flume.SOURCE.source1.EventReceived 50311681
servers.hostname.flume.SOURCE.source1.OpenConnection 0
```

### This file was generated from the python source
### Please edit the source to make changes

