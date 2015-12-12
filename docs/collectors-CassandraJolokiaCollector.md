CassandraJolokiaCollector
=====

Collects Cassandra JMX metrics from the Jolokia Agent.  Extends the
JolokiaCollector to interpret Histogram beans with information about the
distribution of request latencies.

#### Example Configuration
CassandraJolokiaCollector uses a regular expression to determine which
attributes represent histograms. This regex can be overridden by providing a
`histogram_regex` in your configuration.  You can also override `percentiles` to
collect specific percentiles from the histogram statistics.  The format is shown
below with the default values.

CassandraJolokiaCollector.conf

```
    percentiles '50,95,99'
    histogram_regex '.*HistogramMicros$'
```

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>histogram_regex</td><td>.*HistogramMicros$</td><td>Filter to only process attributes that match this regex</td><td>str</td></tr>
<tr><td>host</td><td>localhost</td><td>Hostname</td><td>str</td></tr>
<tr><td>mbeans</td><td>,</td><td>Pipe delimited list of MBeans for which to collect stats. If not provided, all stats will be collected.</td><td>list</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>path</td><td>jolokia</td><td>Path to jolokia.  typically "jmx" or "jolokia"</td><td>str</td></tr>
<tr><td>percentiles</td><td>50, 95, 99,</td><td>Comma separated list of percentiles to be collected (e.g., "50,95,99").</td><td>list</td></tr>
<tr><td>port</td><td>8778</td><td>Port</td><td>int</td></tr>
<tr><td>regex</td><td>False</td><td>Contols if mbeans option matches with regex, False by default.</td><td>bool</td></tr>
<tr><td>rewrite</td><td>,</td><td>This sub-section of the config contains pairs of from-to regex rewrites.</td><td>list</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

