<!--This file was generated from the python source
Please edit the source to make changes
-->
RsyslogCollector
=====

Collects stats from rsyslog server with impstats module loaded 
Impstats formats are json/json-elasticsearch/cee/legacy, but 
only json and legacy formats are supported

#### Dependencies
 * Rsyslog Plugin – impstats (rsyslog 7.5.3+)
   (http://www.rsyslog.com/rsyslog-statistic-counter-plugin-impstats/)
   (http://www.rsyslog.com/doc/v8-stable/configuration/modules/impstats.html)

#### Metrics
 * [Rsyslog statistic counter ](http://www.rsyslog.com/rsyslog-statistic-counter/)

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
pstats_path | /var/log/rsyslog_stats.log | Path to get syslog stats. | str

#### Example Output

```
__EXAMPLESHERE__
```

