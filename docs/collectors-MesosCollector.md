MesosCollector
=====


Collects metrics from a mesos instance. By default,
the collector is set up to query the mesos-master via
port 5050. Set the port to 5051 for mesos-slaves.

#### Example Configuration

```
    host = localhost
    port = 5050
```

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>localhost</td><td>Hostname</td><td>str</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>port</td><td>5050</td><td>Port (default is 5050; please set to 5051 for mesos-slave)</td><td>int</td></tr>
</table>

#### Example Output

```
servers.hostname.mesos.master.cpus_percent 0.762166666667
servers.hostname.mesos.master.cpus_total 120
servers.hostname.mesos.master.cpus_used 91.46
servers.hostname.mesos.master.disk_percent 0.0317975447795
servers.hostname.mesos.master.disk_total 12541440
servers.hostname.mesos.master.disk_used 398787
```

### This file was generated from the python source
### Please edit the source to make changes

