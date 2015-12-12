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


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>instances</td><td>{}</td><td>A subcategory of pgbouncer instances with a host and port, and optionally user and password can be overridden per instance (see example).</td><td>dict</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>password</td><td></td><td>Password</td><td>str</td></tr>
<tr><td>user</td><td>postgres</td><td>Username</td><td>str</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

