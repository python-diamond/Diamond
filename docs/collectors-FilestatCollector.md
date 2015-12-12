FilestatCollector
=====

Uses lsof to collect data on number of open files per user per type

#### Config Options

 * user_include - This is list of users to collect data for. If this is left
    empty, its a wildcard to collector for all users (default = None)
 * user_exclude - This is a list of users to exclude from collecting data. If
    this is left empty, no specific users will be excluded (default = None)
 * group_include - This is a list of groups to include in data collection. If
    this DOES NOT override user_exclude. (default = None)
 * group_exclude - This is a list of groups to exclude from collecting data.
    It DOES NOT override user_include. (default = None)
 * uid_min - This creates a floor for the user's uid. This means that it WILL
    NOT collect data for any user with a uid LOWER than the specified minimum,
    unless the user is told to be included by user_include (default = None)
 * uid_max - This creates a ceiling for the user's uid. This means that it WILL
    NOT collect data for any user with a uid HIGHER than the specified maximum,
    unless the user is told to be included by user_include (default = None)

*** Priority Explanation ***
 This is an explanation of the priority in which users, groups, and uid, are
    evaluated. EXCLUDE ALWAYS OVERRULES INCLUDE within the same level (ie within
    users or group)
  * user_include/exclude (top level/priority)
    * group_include/exclude (second level: if user not in user_include/exclude,
          groups takes affect)
      * uid_min/max (third level: if user not met above qualifications, uids
            take affect)

 * type_include - This is a list of file types to collect ('REG', 'DIR", 'FIFO'
    , etc). If left empty, will collect for all file types. (Note: it suggested
    to not leave type_include empty, as it would add significant load to your
    graphite box(es) (default = None)
 * type_exclude - This is a list of tile types to exclude from being collected
    for. If left empty, no file types will be excluded. (default = None)

 * collect_user_data - This enables or disables the collection of user specific
    file handles. (default = False)

#### Dependencies

 * /proc/sys/fs/file-nr
 * /usr/sbin/lsof


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
</table>

#### Example Output

```
servers.hostname.files.assigned 576
servers.hostname.files.max 4835852
servers.hostname.files.unused 0
```

### This file was generated from the python source
### Please edit the source to make changes

