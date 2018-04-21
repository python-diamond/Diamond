<!--This file was generated from the python source
Please edit the source to make changes
-->
EventstoreProjectionsCollector
=====

A Simple collector which calls the Eventstore API for
the status of projections and parses this to flat metrics.
String values are ignored, except for the name and status.
Name is used for the metric path, status is translated to
an integer (running = 1, stopped = 0).
Note: "$" are replaced by underscores (_) in the projection
name to avoid problems with hostedGraphite/Grafana.

This collector is based upon the HTTPJSONCollector.

#### Dependencies

 * urllib2


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
debug | False | Enable or disable debug mode | bool
enabled | False | Enable collecting these metrics | bool
headers | {'User-Agent': 'Diamond Eventstore metrics collector'} | Header variable if needed | dict
hostname | localhost | hostname of the eventstore instance | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
path | eventstore | name of the metric in the metricpath | str
port | 2113 | tcp port where eventstore is listening | int
protocol | http:// | protocol used to connect to eventstore | str
replace_dollarsign | _ | A value to replace a dollar sign ($) in projection names by | str
route | /projections/all-non-transient | route in eventstore for projections | str

#### Example Output

```
servers.hostname.projections._by_category.bufferedEvents 0
servers.hostname.projections._by_category.coreProcessingTime 10
servers.hostname.projections._by_category.epoch -1
servers.hostname.projections._by_category.eventsProcessedAfterRestart 886
servers.hostname.projections._by_category.partitionsCached 1
servers.hostname.projections._by_category.progress 100.0
servers.hostname.projections._by_category.readsInProgress 0
servers.hostname.projections._by_category.status 1
servers.hostname.projections._by_category.version 1
servers.hostname.projections._by_category.writePendingEventsAfterCheckpoint 0
servers.hostname.projections._by_category.writePendingEventsBeforeCheckpoint 0
servers.hostname.projections._by_category.writesInProgress 0
servers.hostname.projections._by_event_type.bufferedEvents 0
servers.hostname.projections._by_event_type.coreProcessingTime 0
servers.hostname.projections._by_event_type.epoch -1
servers.hostname.projections._by_event_type.eventsProcessedAfterRestart 0
servers.hostname.projections._by_event_type.partitionsCached 1
servers.hostname.projections._by_event_type.progress -1.0
servers.hostname.projections._by_event_type.readsInProgress 0
servers.hostname.projections._by_event_type.status 0
servers.hostname.projections._by_event_type.version 0
servers.hostname.projections._by_event_type.writePendingEventsAfterCheckpoint 0
servers.hostname.projections._by_event_type.writePendingEventsBeforeCheckpoint 0
servers.hostname.projections._by_event_type.writesInProgress 0
servers.hostname.projections._stream_by_cat.bufferedEvents 0
servers.hostname.projections._stream_by_cat.coreProcessingTime 0
servers.hostname.projections._stream_by_cat.epoch -1
servers.hostname.projections._stream_by_cat.eventsProcessedAfterRestart 0
servers.hostname.projections._stream_by_cat.partitionsCached 1
servers.hostname.projections._stream_by_cat.progress -1.0
servers.hostname.projections._stream_by_cat.readsInProgress 0
servers.hostname.projections._stream_by_cat.status 0
servers.hostname.projections._stream_by_cat.version 0
servers.hostname.projections._stream_by_cat.writePendingEventsAfterCheckpoint 0
servers.hostname.projections._stream_by_cat.writePendingEventsBeforeCheckpoint 0
servers.hostname.projections._stream_by_cat.writesInProgress 0
servers.hostname.projections._streams.bufferedEvents 0
servers.hostname.projections._streams.coreProcessingTime 0
servers.hostname.projections._streams.epoch -1
servers.hostname.projections._streams.eventsProcessedAfterRestart 0
servers.hostname.projections._streams.partitionsCached 1
servers.hostname.projections._streams.progress -1.0
servers.hostname.projections._streams.readsInProgress 0
servers.hostname.projections._streams.status 0
servers.hostname.projections._streams.version 0
servers.hostname.projections._streams.writePendingEventsAfterCheckpoint 0
servers.hostname.projections._streams.writePendingEventsBeforeCheckpoint 0
servers.hostname.projections._streams.writesInProgress 0
servers.hostname.projections.all-reports.bufferedEvents 0
servers.hostname.projections.all-reports.coreProcessingTime 46
servers.hostname.projections.all-reports.epoch -1
servers.hostname.projections.all-reports.eventsProcessedAfterRestart 88
servers.hostname.projections.all-reports.partitionsCached 1
servers.hostname.projections.all-reports.progress 100.0
servers.hostname.projections.all-reports.readsInProgress 0
servers.hostname.projections.all-reports.status 1
servers.hostname.projections.all-reports.version 1
servers.hostname.projections.all-reports.writePendingEventsAfterCheckpoint 0
servers.hostname.projections.all-reports.writePendingEventsBeforeCheckpoint 0
servers.hostname.projections.all-reports.writesInProgress 0
```

