MesosCGroupCollector
=====

Collects Mesos Task cgroup statistics. Because Mesos Tasks
only tangentially relate to the host they are running on,
this collector uses task 'source' information to build the
naming path. The prefix is overridden in the collector to
place metrics in the graphite tree at the root under
`mesos.tasks`. The container ID contained within the
source string will serve as the container uniqueifier.

If your scheduler (this was written against a Mesos cluster
    being scheduled by Aurora) does not include uniqueifing
information in the task data under `frameworks.executors.source`,
you're going to have a bad time.

#### Example Configuration

```
    host = localhost
    port = 5051
```

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>localhost</td><td>Hostname</td><td>str</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>port</td><td>5051</td><td>Port</td><td>int</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

