MonitCollector
=====

Collect the monit stats and report on cpu/memory for monitored processes

#### Dependencies

 * monit serving up /_status


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte,</td><td>Default numeric output(s)</td><td>list</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>send_totals</td><td>False</td><td>Send cpu and memory totals</td><td>bool</td></tr>
</table>

#### Example Output

```
servers.hostname.monit.app_thin_8101.cpu.percent 0.9
servers.hostname.monit.app_thin_8101.memory.kilobyte_usage 216104
servers.hostname.monit.app_thin_8102.cpu.percent 1.1
servers.hostname.monit.app_thin_8102.memory.kilobyte_usage 212736
servers.hostname.monit.app_thin_8103.cpu.percent 0.9
servers.hostname.monit.app_thin_8103.memory.kilobyte_usage 204948
servers.hostname.monit.app_thin_8104.cpu.percent 0.9
servers.hostname.monit.app_thin_8104.memory.kilobyte_usage 212464
servers.hostname.monit.cron.cpu.percent 0.0
servers.hostname.monit.cron.memory.kilobyte_usage 1036
servers.hostname.monit.haproxy.cpu.percent 0.0
servers.hostname.monit.haproxy.memory.kilobyte_usage 4040
servers.hostname.monit.nginx.cpu.percent 0.0
servers.hostname.monit.nginx.memory.kilobyte_usage 18684
servers.hostname.monit.postfix.cpu.percent 0.0
servers.hostname.monit.postfix.memory.kilobyte_usage 2304
servers.hostname.monit.rsyslogd.cpu.percent 0.0
servers.hostname.monit.rsyslogd.memory.kilobyte_usage 2664
servers.hostname.monit.sshd.cpu.percent 0.0
servers.hostname.monit.sshd.memory.kilobyte_usage 2588
```

### This file was generated from the python source
### Please edit the source to make changes

