<!--This file was generated from the python source
Please edit the source to make changes
-->
NfsdCollector
=====

The NfsdCollector collects nfsd utilization metrics using /proc/net/rpc/nfsd.

#### Dependencies

 * /proc/net/rpc/nfsd


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.nfsd.input_output.bytes-read 3139369493.0
servers.hostname.nfsd.input_output.bytes-written 15691669.0
servers.hostname.nfsd.net.cnt 14564086.0
servers.hostname.nfsd.net.tcpcnt 14562696.0
servers.hostname.nfsd.net.tcpconn 30773.0
servers.hostname.nfsd.read-ahead.10-pct 8751152.0
servers.hostname.nfsd.read-ahead.cache-size 32.0
servers.hostname.nfsd.read-ahead.not-found 18612.0
servers.hostname.nfsd.reply_cache.misses 71080.0
servers.hostname.nfsd.reply_cache.nocache 14491982.0
servers.hostname.nfsd.rpc.cnt 14563007.0
servers.hostname.nfsd.threads.10-20-pct 22163.0
servers.hostname.nfsd.threads.100-pct 22111.0
servers.hostname.nfsd.threads.20-30-pct 8448.0
servers.hostname.nfsd.threads.30-40-pct 1642.0
servers.hostname.nfsd.threads.50-60-pct 5072.0
servers.hostname.nfsd.threads.60-70-pct 1210.0
servers.hostname.nfsd.threads.70-80-pct 3889.0
servers.hostname.nfsd.threads.80-90-pct 2654.0
servers.hostname.nfsd.threads.fullcnt 1324492.0
servers.hostname.nfsd.threads.threads 8.0
servers.hostname.nfsd.v2.unknown 18.0
servers.hostname.nfsd.v3.access 136921.0
servers.hostname.nfsd.v3.commit 635.0
servers.hostname.nfsd.v3.create 1655.0
servers.hostname.nfsd.v3.fsinfo 11.0
servers.hostname.nfsd.v3.fsstat 34450.0
servers.hostname.nfsd.v3.getattr 724974.0
servers.hostname.nfsd.v3.lookup 213165.0
servers.hostname.nfsd.v3.null 8.0
servers.hostname.nfsd.v3.read 8761683.0
servers.hostname.nfsd.v3.readdir 11295.0
servers.hostname.nfsd.v3.readdirplus 132298.0
servers.hostname.nfsd.v3.remove 1488.0
servers.hostname.nfsd.v3.unknown 22.0
servers.hostname.nfsd.v3.write 67937.0
servers.hostname.nfsd.v4.compound 4476320.0
servers.hostname.nfsd.v4.null 18.0
servers.hostname.nfsd.v4.ops.access 2083822.0
servers.hostname.nfsd.v4.ops.close 34801.0
servers.hostname.nfsd.v4.ops.commit 3955.0
servers.hostname.nfsd.v4.ops.getattr 2302848.0
servers.hostname.nfsd.v4.ops.getfh 51791.0
servers.hostname.nfsd.v4.ops.lookup 68501.0
servers.hostname.nfsd.v4.ops.open 34847.0
servers.hostname.nfsd.v4.ops.open_conf 29002.0
servers.hostname.nfsd.v4.ops.putfh 4435270.0
servers.hostname.nfsd.v4.ops.putrootfh 6237.0
servers.hostname.nfsd.v4.ops.read 8030.0
servers.hostname.nfsd.v4.ops.readdir 272.0
servers.hostname.nfsd.v4.ops.remove 7802.0
servers.hostname.nfsd.v4.ops.renew 28594.0
servers.hostname.nfsd.v4.ops.restorefh 34839.0
servers.hostname.nfsd.v4.ops.savefh 34847.0
servers.hostname.nfsd.v4.ops.setattr 7870.0
servers.hostname.nfsd.v4.ops.setcltid 6226.0
servers.hostname.nfsd.v4.ops.setcltidconf 6227.0
servers.hostname.nfsd.v4.ops.unknown 40.0
servers.hostname.nfsd.v4.ops.write 76562.0
servers.hostname.nfsd.v4.unknown 2.0
```

