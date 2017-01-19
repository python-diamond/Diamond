<!--This file was generated from the python source
Please edit the source to make changes
-->
ProcessResourcesCollector
=====

A Diamond collector that collects memory usage of each process defined in it's
config file by matching them with their executable filepath or the process name.
This collector can also be used to collect memory usage for the Diamond process.

Example config file ProcessResourcesCollector.conf

```
enabled=True
unit=B
cpu_interval=0.1
info_keys='num_ctx_switches','cpu_percent','cpu_times','io_counters','num_threads','num_fds','memory_percent','memory_info_ex'
[process]
[[postgres]]
exe=^\/usr\/lib\/postgresql\/+d.+d\/bin\/postgres$
name=^postgres,^pg

[[elasticsearch]]
cmdline=java.*Elasticsearch

[[diamond]]
selfmon=True
```

exe and name are both lists of comma-separated regexps.

count_workers defined under [process] will determine whether to count how many
workers are there of processes which match this [process],
for example: cgi workers.


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
info_keys | num_ctx_switches, cpu_percent, cpu_times, io_counters, num_threads, num_fds, memory_percent, memory_info_ex, | List of process metrics to collect. Valid list of metrics can be found [here](https://pythonhosted.org/psutil/) | list
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
process | {} | A subcategory of settings inside of which each collected process has it's configuration | dict
unit | B | The unit in which memory data is collected. | str

#### Example Output

```
__EXAMPLESHERE__
```

