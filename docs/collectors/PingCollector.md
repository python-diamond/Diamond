<!--This file was generated from the python source
Please edit the source to make changes
-->
PingCollector
=====

Collect icmp round trip times
Only valid for ipv4 hosts currently

#### Dependencies

 * ping

#### Configuration

Configuration is done by:

Create a file named: PingCollector.conf in the collectors_config_path

 * enabled = true
 * interval = 60
 * target_1 = example.org
 * target_fw = 192.168.0.1
 * target_localhost = localhost

Test your configuration using the following command:

diamond-setup --print -C PingCollector

You should get a response back that indicates 'enabled': True and see entries
for your targets in pairs like:

'target_1': 'example.org'

We extract out the key after target_ and use it in the graphite node we push.


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | /bin/ping | The path to the ping binary | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | False | Use sudo? | bool

#### Example Output

```
servers.hostname.ping.localhost 11
```

