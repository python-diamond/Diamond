<!--This file was generated from the python source
Please edit the source to make changes
-->
BeanstalkdCollector
=====

Collects the following from beanstalkd:
    - Server statistics via the 'stats' command
    - Per tube statistics via the 'stats-tube' command

#### Dependencies

 * beanstalkc


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | localhost | Hostname | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 11300 | Port | int

#### Example Output

```
servers.hostname.beanstalkd.binlog-current-index 0
servers.hostname.beanstalkd.binlog-max-size 10485760
servers.hostname.beanstalkd.binlog-oldest-index 0
servers.hostname.beanstalkd.binlog-records-migrated 0
servers.hostname.beanstalkd.binlog-records-written 0
servers.hostname.beanstalkd.cmd-bury 0
servers.hostname.beanstalkd.cmd-delete 4331
servers.hostname.beanstalkd.cmd-ignore 0
servers.hostname.beanstalkd.cmd-kick 0
servers.hostname.beanstalkd.cmd-list-tube-used 0
servers.hostname.beanstalkd.cmd-list-tubes 0
servers.hostname.beanstalkd.cmd-list-tubes-watched 0
servers.hostname.beanstalkd.cmd-pause-tube 0
servers.hostname.beanstalkd.cmd-peek 0
servers.hostname.beanstalkd.cmd-peek-buried 0
servers.hostname.beanstalkd.cmd-peek-delayed 0
servers.hostname.beanstalkd.cmd-peek-ready 0
servers.hostname.beanstalkd.cmd-put 4331
servers.hostname.beanstalkd.cmd-release 0
servers.hostname.beanstalkd.cmd-reserve 4386
servers.hostname.beanstalkd.cmd-reserve-with-timeout 0
servers.hostname.beanstalkd.cmd-stats 1
servers.hostname.beanstalkd.cmd-stats-job 0
servers.hostname.beanstalkd.cmd-stats-tube 0
servers.hostname.beanstalkd.cmd-touch 0
servers.hostname.beanstalkd.cmd-use 4321
servers.hostname.beanstalkd.cmd-watch 55
servers.hostname.beanstalkd.current-connections 10
servers.hostname.beanstalkd.current-jobs-buried 0
servers.hostname.beanstalkd.current-jobs-delayed 0
servers.hostname.beanstalkd.current-jobs-ready 0
servers.hostname.beanstalkd.current-jobs-reserved 0
servers.hostname.beanstalkd.current-jobs-urgent 0
servers.hostname.beanstalkd.current-producers 0
servers.hostname.beanstalkd.current-tubes 7
servers.hostname.beanstalkd.current-waiting 9
servers.hostname.beanstalkd.current-workers 9
servers.hostname.beanstalkd.job-timeouts 0
servers.hostname.beanstalkd.max-job-size 65535
servers.hostname.beanstalkd.pid 23703
servers.hostname.beanstalkd.rusage-stime 295.970497
servers.hostname.beanstalkd.rusage-utime 125.92787
servers.hostname.beanstalkd.total-connections 4387
servers.hostname.beanstalkd.total-jobs 4331
servers.hostname.beanstalkd.tubes.default.cmd-delete 10
servers.hostname.beanstalkd.tubes.default.cmd-pause-tube 0
servers.hostname.beanstalkd.tubes.default.current-jobs-buried 0
servers.hostname.beanstalkd.tubes.default.current-jobs-delayed 0
servers.hostname.beanstalkd.tubes.default.current-jobs-ready 0
servers.hostname.beanstalkd.tubes.default.current-jobs-reserved 0
servers.hostname.beanstalkd.tubes.default.current-jobs-urgent 0
servers.hostname.beanstalkd.tubes.default.current-using 10
servers.hostname.beanstalkd.tubes.default.current-waiting 9
servers.hostname.beanstalkd.tubes.default.current-watching 10
servers.hostname.beanstalkd.tubes.default.pause 0
servers.hostname.beanstalkd.tubes.default.pause-time-left 0
servers.hostname.beanstalkd.tubes.default.total-jobs 10
servers.hostname.beanstalkd.uptime 182954
```

