<!--This file was generated from the python source
Please edit the source to make changes
-->
EtcdCollector
=====


Collects metrics from an Etcd instance.

#### Example Configuration

```
    host = localhost
    port = 2379
```

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
ca_file |  | Only applies when use_tls=true. Path to CA certificate file to use for server identity verification | str
enabled | False | Enable collecting these metrics | bool
host | localhost | Hostname | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 2379 | Port (default is 2379) | int
timeout | 5 | Timeout per HTTP(s) call | int
use_tls | False | Use TLS/SSL or just unsecure (default is unsecure) | bool

#### Example Output

```
servers.hostname.etcd.self.is_leader 1
servers.hostname.etcd.self.recvAppendRequestCnt 5870
servers.hostname.etcd.self.sendAppendRequestCnt 2097127
servers.hostname.etcd.self.sendBandwidthRate 901.090846975
servers.hostname.etcd.self.sendPkgRate 11.7635880806
servers.hostname.etcd.store.compareAndDeleteFail 0
servers.hostname.etcd.store.compareAndDeleteSuccess 2047
servers.hostname.etcd.store.compareAndSwapFail 355
servers.hostname.etcd.store.compareAndSwapSuccess 9156
servers.hostname.etcd.store.createFail 2508
servers.hostname.etcd.store.createSuccess 6468
servers.hostname.etcd.store.deleteFail 2138
servers.hostname.etcd.store.deleteSuccess 2468
servers.hostname.etcd.store.expireCount 0
servers.hostname.etcd.store.getsFail 922428
servers.hostname.etcd.store.getsSuccess 1685131
servers.hostname.etcd.store.setsFail 123
servers.hostname.etcd.store.setsSuccess 733
servers.hostname.etcd.store.updateFail 0
servers.hostname.etcd.store.updateSuccess 4576
servers.hostname.etcd.store.watchers 51
```

