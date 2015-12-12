<!--This file was generated from the python source
Please edit the source to make changes
-->
PostgresqlCollector
=====

Collect metrics from postgresql

#### Dependencies

 * psycopg2


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
dbname | postgres | DB to connect to in order to get list of DBs in PgSQL | str
enabled | False | Enable collecting these metrics | bool
extended | False | Enable collection of extended database stats. | bool
has_admin | True | Admin privileges are required to execute some queries. | bool
host | localhost | Hostname | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics | , | List of enabled metrics to collect | list
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
password | postgres | Password | str
password_provider | password | Whether to auth with supplied password or .pgpass file  <password|pgpass> | str
pg_version | 9.2 | The version of postgres that you'll be monitoring eg. in format 9.2 | float
port | 5432 | Port number | int
sslmode | disable | Whether to use SSL - <disable|allow|require|...> | str
underscore | False | Convert _ to . | bool
user | postgres | Username | str

#### Example Output

```
__EXAMPLESHERE__
```

