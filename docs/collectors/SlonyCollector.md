<!--This file was generated from the python source
Please edit the source to make changes
-->
SlonyCollector
=====

Collect slony metrics from postgresql

#### Dependencies

 * psycopg2

#### Example Configuration

```
enabled = True

host = localhost
port = 5432
slony_node_string = Node [0-9] - [_a-z0-9]*@(.*).example.com

[instances]

[[database1]]
slony_db = postgres
slony_schema = _slony


[[database2]]
user = postgres
password = postgres
slony_db = data_db
slony_node_string = Node [0-9] - [_a-z0-9]*@(.*).i.example.com
slony_schema = _data_db
```


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost | Hostname | str
instances | {} | Subcategory of slony instances that includes the slony database, and slony schema to be monitored. Optionally, user, password and slony_node_string maybe overridden per instance (see example). | dict
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
password | postgres | Password | str
port | 5432 | Port number | int
slony_node_string | Node [0-9]+ - postgres@localhost | Regex for SQL SUBSTRING to extract the hostname from sl_node.no_comment | str
user | postgres | Username | str

#### Example Output

```
__EXAMPLESHERE__
```

