<!--This file was generated from the python source
Please edit the source to make changes
-->
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

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost | Hostname | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 5050 | Port (default is 5050; please set to 5051 for mesos-slave) | int

#### Example Output

```
servers.hostname.mesos.master.cpus_percent 0.762166666667
servers.hostname.mesos.master.cpus_total 120
servers.hostname.mesos.master.cpus_used 91.46
servers.hostname.mesos.master.disk_percent 0.0317975447795
servers.hostname.mesos.master.disk_total 12541440
servers.hostname.mesos.master.disk_used 398787
```

