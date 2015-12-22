<!--This file was generated from the python source
Please edit the source to make changes
-->
UserScriptsCollector
=====

Runs third party scripts and collects their output.

Scripts need to be +x and should output metrics in the form of

```
metric.path.a 1
metric.path.b 2
metric.path.c 3
```

They are not passed any arguments and if they return an error code,
no metrics are collected.

#### Dependencies

 * [subprocess](http://docs.python.org/library/subprocess.html)


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
scripts_path | /etc/diamond/user_scripts/ | Path to find the scripts to run | str

#### Example Output

```
servers.hostname.example.1 42
servers.hostname.example.2 24
servers.hostname.example.3 12.1212
```

