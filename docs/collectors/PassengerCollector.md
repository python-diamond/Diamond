<!--This file was generated from the python source
Please edit the source to make changes
-->
PassengerCollector
=====

The PasengerCollector collects CPU and memory utilization of apache, nginx
and passenger processes.
It also collects requests in top-level and passenger applications group queues.

Four key attributes to be published:

 * phusion_passenger_cpu
 * total_apache_memory
 * total_apache_procs
 * total_passenger_memory
 * total_passenger_procs
 * total_nginx_memory
 * total_nginx_procs
 * top_level_queue_size
 * passenger_queue_size

#### Dependencies

 * passenger-memory-stats
 * passenger-status


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | /usr/lib/ruby-flo/bin/passenger-memory-stats | The path to the binary | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
passenger_memory_stats_bin | /usr/bin/passenger-memory-stats | The path to the binary passenger-memory-stats | str
passenger_status_bin | /usr/bin/passenger-status | The path to the binary passenger-status | str
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | False | Use sudo? | bool

#### Example Output

```
__EXAMPLESHERE__
```

