<!--This file was generated from the python source
Please edit the source to make changes
-->
FlumeCollector
=====

Collect statistics from Flume

#### Dependencies

 * urllib2
 * json or simplejson


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
req_host | localhost | Hostname | str
req_path | /metrics | Path | str
req_port | 41414 | Port | int

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

