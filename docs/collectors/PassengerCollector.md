<!--This file was generated from the python source
Please edit the source to make changes
-->
PassengerCollector
=====

The PasengerCollector collects CPU and memory utilization of apache, nginx
and passenger processes.

Four key attributes to be published:

 * phusion_passenger_cpu
 * total_apache_memory
 * total_passenger_memory
 * total_nginx_memory

#### Dependencies

 * passenger-memory-stats


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | /usr/lib/ruby-flo/bin/passenger-memory-stats | The path to the binary | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | False | Use sudo? | bool

#### Example Output

```
__EXAMPLESHERE__
```

