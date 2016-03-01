# Configuration

## Configuration File

If you've installed diamond via a package, a example configuration file is `/etc/diamond/diamond.conf.example`.
Please copy this to `/etc/diamond/diamond.conf` and configure at will.
By default, diamond will push to a graphite server host "graphite". You should probably change this to point to your own graphite server.

Other configuration should not be necessary.

By default diamond publishes metrics using the following form:

    systems.<hostname>.<metrics>.<metric>

You can override the "systems" portion of the metric path by changing the "path_prefix" setting in the configuration file.

Configuration is handled via `diamond.conf` and collector specific files in `/etc/diamond/collectors/` by default.
Each collector's defaults are overridden by `/etc/diamond.conf` and then by the specific collector config file, so if you want to make a change to all the collectors, please edit the default collector section in `diamond.conf`.
If you want to change a specific collector, please edit the specific collector config in `/etc/diamond/collectors/`.

We also have diamond-setup. It will walk you though setting up diamond and it's collectors. It will display information about the collector, ask you to enable or disable it, and any collector specfic settings it might have. This should be a easy way for one to setup and run diamond.

## Logging

Diamond defaults to logging at `/var/log/diamond/diamond.log`.
The following is a sample configuration to have log sent to both `/var/log/diamond/diamond.log` AND local syslog daemon:

```
[handlers]
keys = rotated_file,syslog

[loggers]
keys = root

[formatters]
keys = syslog,default

[logger_root]
level = INFO
handlers = syslog,rotated_file

[handler_syslog]
class = handlers.SysLogHandler
level = DEBUG
formatter = syslog
args = ('/dev/log',)

[formatter_syslog]
format = %(asctime)-15s diamond[%(process)d] %(message)s
datefmt = %b %d %H:%M:%S

[handler_rotated_file]
class = handlers.TimedRotatingFileHandler
level = DEBUG
formatter = default
# rotate at midnight, each day and keep 7 days
args = ('/var/log/diamond/diamond.log', 'midnight', 1, 7)

[formatter_default]
format = [%(asctime)s] [%(threadName)s] %(message)s
datefmt =
```

## Collector Settings

Every collector has some default options

Setting | Default | Description | Type
--------|---------|-------------|-----
enabled | False | Enable collecting these metrics | bool
path_prefix | servers | Base path to put all metrics | str
path | | Path on the tree to place the metrics | str
interval | 300 | Default Poll Interval (seconds) | int
splay | | Default splay time (seconds) | int
method | | Threading model to use, Sequential or Threaded | str
byte_unit | byte | List of units to convert bit/byte numeric types to | str
hostname | | Hardcode an hostname rather then finding one | str
hostname_method | | Change the method to find the hostname. Valid options are <ul><li>*fqdn:* Hostname with . replaced by _ (www_example_com)</li><li>*fqdn_short:* Default. Similar to hostname -s</li><li>*fqdn_rev:* Hostname in reverse (com.example.www)</li><li>*uname_short:* Similar to uname -n, but only the first part</li><li>*uname_rev:* uname -r in reverse (com.example.www)</li><li>*None:* no hostname autodetection. just use the statically defined hostname</li></ul> | str

## Enable / Disable Collector

Diamond collectors that require a separate configuration file should place a .conf file in `/etc/diamond/collectors/`.
The configuration file name should match the name of the diamond collector class.
For example, a collector called *examplecollector.ExampleCollector* could have its configuration file placed in `/etc/diamond/collectors/ExampleCollector.conf`.


Example:
Enable HttpdCollector
Create a file HttpdCollector.conf and set 
```
enabled = True
```

To verify if enabled or not :
```
diamond-setup --print -C HttpdCollector
```

Incase you wish to create the conf file using a setup run the command :
```
diamond-setup -C HttpdCollector
```

You can add more settings for the Collector in the same file.

Make sure to restart diamond daemon and wait at least 3 collection cycles.
