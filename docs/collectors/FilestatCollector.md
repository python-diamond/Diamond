<!--This file was generated from the python source
Please edit the source to make changes
-->
FilestatCollector
=====

Uses lsof to collect data on number of open files per user per type

#### Config Options

 Check Options table below

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


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
collect_user_data | False | This enables or disables the collection of user specific file handles. (default = False) | bool
enabled | False | Enable collecting these metrics | bool
group_exclude | None | This is a list of groups to exclude from collecting data. It DOES NOT override user_include. (default = None) | NoneType
group_include | None | This is a list of groups to include in data collection. This DOES NOT override user_exclude. (default = None) | NoneType
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
type_exclude | None | This is a list of tile types to exclude from being collected for. If left empty, no file types will be excluded. (default = None) | NoneType
type_include | None | This is a list of file types to collect ('REG', 'DIR', 'FIFO', etc). If left empty, will collect for all file types.(Note: it's suggested to not leave type_include empty, as it would add significant load to your graphite box(es) (default = None) | NoneType
uid_max | 65536 | This creates a ceiling for the user's uid. This means that it WILL NOT collect data for any user with a uid HIGHER than the specified maximum, unless the user is told to be included by user_include (default = 65536) | int
uid_min | 0 | This creates a floor for the user's uid. This means that it WILL NOT collect data for any user with a uid LOWER than the specified minimum, unless the user is told to be included by user_include (default = 0) | int
user_exclude | None | This is a list of users to exclude from collecting data. If this is left empty, no specific users will be excluded (default = None) | NoneType
user_include | None | This is list of users to collect data for. If this is left empty, its a wildcard to collector for all users (default = None) | NoneType

#### Example Output

```
servers.hostname.files.assigned 576
servers.hostname.files.max 4835852
servers.hostname.files.unused 0
```

