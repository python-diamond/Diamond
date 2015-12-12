MySQLCollector
=====


#### Grants

 * Normal usage
```
GRANT REPLICATION CLIENT on *.* TO 'user'@'hostname' IDENTIFIED BY
'password';
```

 * For innodb engine status
```
GRANT SUPER ON *.* TO 'user'@'hostname' IDENTIFIED BY
'password';
```

 * For innodb engine status on MySQL versions 5.1.24+
```
GRANT PROCESS ON *.* TO 'user'@'hostname' IDENTIFIED BY
'password';
```

#### Dependencies

 * MySQLdb


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>hosts</td><td>,</td><td>List of hosts to collect from. Format is yourusername:yourpassword@host:port/db[/nickname]use db "None" to avoid connecting to a particular db</td><td>list</td></tr>
<tr><td>innodb</td><td>False</td><td>Collect SHOW ENGINE INNODB STATUS</td><td>bool</td></tr>
<tr><td>master</td><td>False</td><td>Collect SHOW MASTER STATUS</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>publish</td><td></td><td>Which rows of '[SHOW GLOBAL STATUS](http://dev.mysql.com/doc/refman/5.1/en/show-status.html)' you would like to publish. Leave unset to publish all</td><td></td></tr>
<tr><td>slave</td><td>False</td><td>Collect SHOW SLAVE STATUS</td><td>bool</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

