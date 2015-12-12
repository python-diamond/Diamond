PostgresqlCollector
=====

Collect metrics from postgresql

#### Dependencies

 * psycopg2


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>dbname</td><td>postgres</td><td>DB to connect to in order to get list of DBs in PgSQL</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>extended</td><td>False</td><td>Enable collection of extended database stats.</td><td>bool</td></tr>
<tr><td>has_admin</td><td>True</td><td>Admin privileges are required to execute some queries.</td><td>bool</td></tr>
<tr><td>host</td><td>localhost</td><td>Hostname</td><td>str</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics</td><td>,</td><td>List of enabled metrics to collect</td><td>list</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>password</td><td>postgres</td><td>Password</td><td>str</td></tr>
<tr><td>password_provider</td><td>password</td><td>Whether to auth with supplied password or .pgpass file  <password|pgpass></td><td>str</td></tr>
<tr><td>pg_version</td><td>9.2</td><td>The version of postgres that you'll be monitoring eg. in format 9.2</td><td>float</td></tr>
<tr><td>port</td><td>5432</td><td>Port number</td><td>int</td></tr>
<tr><td>sslmode</td><td>disable</td><td>Whether to use SSL - <disable|allow|require|...></td><td>str</td></tr>
<tr><td>underscore</td><td>False</td><td>Convert _ to .</td><td>bool</td></tr>
<tr><td>user</td><td>postgres</td><td>Username</td><td>str</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

