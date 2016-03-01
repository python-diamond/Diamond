<!--This file was generated from the python source
Please edit the source to make changes
-->
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

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost | Hostname | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 5051 | Port | int

#### Example Output

```
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.cpu.nr_periods 26848849
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.cpu.nr_throttled 85144
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.cpu.throttled_time 34709931864651
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.cpuacct.system 2774846
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.cpuacct.usage 170379797227518
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.cpuacct.user 9333852
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.active_anon 1789911040
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.active_file 180727808
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.cache 233398272
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.hierarchical_memory_limit 3355443200
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.inactive_anon 0
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.inactive_file 52654080
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.mapped_file 1118208
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.pgfault 353980394
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.pgmajfault 157
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.pgpgin 375953210
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.pgpgout 385688436
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.rss 1789911040
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.rss_huge 1642070016
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_active_anon 1789911040
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_active_file 180727808
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_cache 233398272
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_inactive_anon 0
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_inactive_file 52654080
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_mapped_file 1118208
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_pgfault 353980394
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_pgmajfault 157
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_pgpgin 375953210
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_pgpgout 385688436
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_rss 1789911040
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_rss_huge 1642070016
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_unevictable 0
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.total_writeback 0
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.unevictable 0
servers.hostname.tasks.ENVIRONMENT.ROLE.TASK.0.memory.writeback 0
```

