ApcupsdCollector
=====

Collects the complete status of most American Power Conversion Corp. (APC) UPSes
provided you have the apcupsd daemon installed, properly configured and
running. It can access status information from any APC UPS attached to the
localhost or attached to any computer on the network which is running
apcuspd in NIS mode.

#### Dependencies

 * apcuspd in NIS mode


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>hostname</td><td>localhost</td><td>Hostname to collect from</td><td>str</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics</td><td>LINEV, LOADPCT, BCHARGE, TIMELEFT, BATTV, NUMXFERS, TONBATT, MAXLINEV, MINLINEV, OUTPUTV, ITEMP, LINEFREQ, CUMONBATT,</td><td>List of metrics. Valid metric keys can be found [here](http://www.apcupsd.com/manual/manual.html#status-report-fields)</td><td>list</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>port</td><td>3551</td><td>port to collect from. defaults to 3551</td><td>int</td></tr>
</table>

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

### This file was generated from the python source
### Please edit the source to make changes

