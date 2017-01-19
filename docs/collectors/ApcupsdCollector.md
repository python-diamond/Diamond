<!--This file was generated from the python source
Please edit the source to make changes
-->
ApcupsdCollector
=====

Collects the complete status of most American Power Conversion Corp. (APC) UPSes
provided you have the apcupsd daemon installed, properly configured and
running. It can access status information from any APC UPS attached to the
localhost or attached to any computer on the network which is running
apcuspd in NIS mode.

#### Dependencies

 * apcuspd in NIS mode


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
hostname | localhost | Hostname to collect from | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics | LINEV, LOADPCT, BCHARGE, TIMELEFT, BATTV, NUMXFERS, TONBATT, MAXLINEV, MINLINEV, OUTPUTV, ITEMP, LINEFREQ, CUMONBATT, | List of metrics. Valid metric keys can be found [here](http://www.apcupsd.com/manual/manual.html#status-report-fields) | list
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 3551 | port to collect from. defaults to 3551 | int

#### Example Output

```
servers.hostname.apcupsd.localhost.BATTV 27.3
servers.hostname.apcupsd.localhost.BCHARGE 100.0
servers.hostname.apcupsd.localhost.LINEV 124.0
servers.hostname.apcupsd.localhost.LOADPCT 5.0
servers.hostname.apcupsd.localhost.NUMXFERS 0.0
servers.hostname.apcupsd.localhost.TIMELEFT 73.9
servers.hostname.apcupsd.localhost.TONBATT 0.0
```

