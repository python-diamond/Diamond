<!--This file was generated from the python source
Please edit the source to make changes
-->
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

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
histogram_regex | .*HistogramMicros$ | Filter to only process attributes that match this regex | str
host | localhost | Hostname | str
mbeans | , | Pipe delimited list of MBeans for which to collect stats. If not provided, all stats will be collected. | list
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
password | None | Password for authentication | NoneType
path | jolokia | Path to jolokia.  typically "jmx" or "jolokia" | str
percentiles | 50, 95, 99, | Comma separated list of percentiles to be collected (e.g., "50,95,99"). | list
port | 8778 | Port | int
regex | False | Contols if mbeans option matches with regex, False by default. | bool
rewrite | , | This sub-section of the config contains pairs of from-to regex rewrites. | list
username | None | Username for authentication | NoneType

#### Example Output

```
__EXAMPLESHERE__
```

