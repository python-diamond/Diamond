<!--This file was generated from the python source
Please edit the source to make changes
-->
PgbouncerCollector
=====

Collect metrics from pgbouncer.

#### Dependencies

 * psycopg2

#### Example Configuration

```
enabled=True

[instances]

[[master]]
host = localhost
port = 6432

[[replica]]
host = localhost
port = 6433
password = foobar
```


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
instances | {} | A subcategory of pgbouncer instances with a host and port, and optionally user and password can be overridden per instance (see example). | dict
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
password |  | Password | str
user | postgres | Username | str

#### Example Output

```
__EXAMPLESHERE__
```

