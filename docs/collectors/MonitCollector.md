<!--This file was generated from the python source
Please edit the source to make changes
-->
MonitCollector
=====

Collect the monit stats and report on cpu/memory for monitored processes

#### Dependencies

 * monit serving up /_status


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte, | Default numeric output(s) | list
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
send_totals | False | Send cpu and memory totals | bool

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

