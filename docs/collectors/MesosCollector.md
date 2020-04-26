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
__EXAMPLESHERE__
```

