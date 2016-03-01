<!--This file was generated from the python source
Please edit the source to make changes
-->
JolokiaCollector
=====

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

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost | Hostname | str
mbeans | , | Pipe delimited list of MBeans for which to collect stats. If not provided, all stats will be collected. | list
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
password | None | Password for authentication | NoneType
path | jolokia | Path to jolokia.  typically "jmx" or "jolokia" | str
port | 8778 | Port | int
regex | False | Contols if mbeans option matches with regex, False by default. | bool
rewrite | , | This sub-section of the config contains pairs of from-to regex rewrites. | list
username | None | Username for authentication | NoneType

#### Example Output

```
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.duration 2
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.id 219
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Old_Gen.committed 73400320
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Old_Gen.init 73400320
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Old_Gen.max 73400320
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Old_Gen.used 5146840
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Perm_Gen.committed 23920640
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Perm_Gen.init 21757952
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Perm_Gen.max 85983232
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.CMS_Perm_Gen.used 23796992
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Code_Cache.committed 2686976
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Code_Cache.init 2555904
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Code_Cache.max 50331648
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Code_Cache.used 2600768
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Eden_Space.committed 25165824
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Eden_Space.init 25165824
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Eden_Space.max 25165824
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Eden_Space.used 25165824
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Survivor_Space.committed 3145728
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Survivor_Space.init 3145728
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Survivor_Space.max 3145728
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.memoryUsageBeforeGc.Par_Survivor_Space.used 414088
servers.hostname.jolokia.java.lang.name_ParNew.type_GarbageCollector.LastGcInfo.startTime 14259063
```

