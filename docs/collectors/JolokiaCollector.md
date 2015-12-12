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

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>localhost</td><td>Hostname</td><td>str</td></tr>
<tr><td>mbeans</td><td>,</td><td>Pipe delimited list of MBeans for which to collect stats. If not provided, all stats will be collected.</td><td>list</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>password</td><td>None</td><td>Password for authentication</td><td>NoneType</td></tr>
<tr><td>path</td><td>jolokia</td><td>Path to jolokia.  typically "jmx" or "jolokia"</td><td>str</td></tr>
<tr><td>port</td><td>8778</td><td>Port</td><td>int</td></tr>
<tr><td>regex</td><td>False</td><td>Contols if mbeans option matches with regex, False by default.</td><td>bool</td></tr>
<tr><td>rewrite</td><td>,</td><td>This sub-section of the config contains pairs of from-to regex rewrites.</td><td>list</td></tr>
<tr><td>username</td><td>None</td><td>Username for authentication</td><td>NoneType</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

