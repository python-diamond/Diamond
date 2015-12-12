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


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>localhost</td><td>Hostname</td><td>str</td></tr>
<tr><td>instances</td><td>{}</td><td>Subcategory of slony instances that includes the slony database, and slony schema to be monitored. Optionally, user, password and slony_node_string maybe overridden per instance (see example).</td><td>dict</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>password</td><td>postgres</td><td>Password</td><td>str</td></tr>
<tr><td>port</td><td>5432</td><td>Port number</td><td>int</td></tr>
<tr><td>slony_node_string</td><td>Node [0-9]+ - postgres@localhost</td><td>Regex for SQL SUBSTRING to extract the hostname from sl_node.no_comment</td><td>str</td></tr>
<tr><td>user</td><td>postgres</td><td>Username</td><td>str</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

