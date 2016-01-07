<!--This file was generated from the python source
Please edit the source to make changes
-->
PgQCollector
=====

Collects metrics on queues and queue consumers from PgQ, a PostgreSQL-based
queueing mechanism (part of the Skytools utilities released by Skype.)

#### Dependencies

 * psycopg2

#### Example Configuration

```
enabled = True

[instances]

[[database1]]
dsn = postgresql://user:secret@localhost

[[database2]]
dsn = host=localhost port=5432 dbname=mydb
```

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
instances | {} | The databases to be monitored. Each should have a `dsn` attribute, which must be a valid libpq connection string. | dict
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
__EXAMPLESHERE__
```

