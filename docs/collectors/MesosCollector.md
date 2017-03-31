<!--This file was generated from the python source
Please edit the source to make changes
-->
MesosCollector
=====


Collects metrics from a mesos instance. By default,
the collector is set up to query the mesos-master via
port 5050. Set the port to 5051 for mesos-agent.

#### Example Configuration

```
host = localhost
port = 5050
```

#### Dependencies
 * urlib2

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost | Hostname, using http scheme by default. For https pass e.g. "https://localhost" | str
master | True | True if host is master (default is True). | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 5050 | Port (default is 5050; set to 5051 for mesos-agent) | int

#### Example Output

```
servers.hostname.mesos.failed_tasks 6
servers.hostname.mesos.finished_tasks 1
servers.hostname.mesos.frameworks.marathon-0_7_6.executors.com_domain_group_anotherApp.mem_mapped_file_bytes 45056
servers.hostname.mesos.frameworks.marathon-0_7_6.executors.task_name.06247c78-b6a9-11e4-99f6-fa163ef210c0.cpus_limit (1.1, 1)
servers.hostname.mesos.frameworks.marathon-0_7_6.executors.task_name.09b6f20c-b6a9-11e4-99f6-fa163ef210c0.cpus_limit (0.6, 1)
servers.hostname.mesos.frameworks.marathon-0_7_6.executors.task_name.cpus_limit (1.7, 1)
servers.hostname.mesos.frameworks.marathon-0_7_6.executors.task_name.instances_count (2, 0)
servers.hostname.mesos.frameworks.marathon-0_7_6.executors.task_name.mem_percent (0.19, 2)
servers.hostname.mesos.master.elected 1
servers.hostname.mesos.registrar.state_store_ms.p9999 (17.8412544, 6)
servers.hostname.mesos.staged_tasks 20
servers.hostname.mesos.system.mem_free_bytes 5663678464.1
```

