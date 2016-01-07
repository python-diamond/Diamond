<!--This file was generated from the python source
Please edit the source to make changes
-->
OssecCollector
=====

Shells out to get ossec statistics, which may or may not require sudo access.

Metrics:
- agents.active
- agents.never_connected
- agents.disconnected
- agents.active_local

#### Dependencies

 * /var/ossec/bin/agent_control


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | /var/ossec/bin/agent_control | Path to agent_control binary | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | True | Use sudo? | bool

#### Example Output

```
__EXAMPLESHERE__
```

