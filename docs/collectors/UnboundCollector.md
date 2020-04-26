<!--This file was generated from the python source
Please edit the source to make changes
-->
UnboundCollector
=====

Collect stats from the unbound resolver

#### Dependencies

    * collections.defaultdict or kitchen


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | /usr/sbin/unbound-control | Path to unbound-control binary | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
histogram | True | Include histogram in collection | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | False | Use sudo? | bool

#### Example Output

```
servers.hostname.unbound.histogram.128ms+ 19.0
servers.hostname.unbound.histogram.16ms+ 10.0
servers.hostname.unbound.histogram.16s+ 0.0
servers.hostname.unbound.histogram.1ms 39.0
servers.hostname.unbound.histogram.1ms+ 5.0
servers.hostname.unbound.histogram.1s+ 0.0
servers.hostname.unbound.histogram.256ms+ 3.0
servers.hostname.unbound.histogram.2ms+ 0.0
servers.hostname.unbound.histogram.2s+ 0.0
servers.hostname.unbound.histogram.32ms+ 18.0
servers.hostname.unbound.histogram.32s+ 3.0
servers.hostname.unbound.histogram.4ms+ 0.0
servers.hostname.unbound.histogram.4s+ 1.0
servers.hostname.unbound.histogram.512ms+ 6.0
servers.hostname.unbound.histogram.64ms+ 20.0
servers.hostname.unbound.histogram.64s+ 9.0
servers.hostname.unbound.histogram.8ms+ 3.0
servers.hostname.unbound.histogram.8s+ 0.0
servers.hostname.unbound.mem.cache.message 71303005
servers.hostname.unbound.mem.cache.rrset 142606276
servers.hostname.unbound.mem.mod.iterator 16532
servers.hostname.unbound.mem.mod.validator 1114579
servers.hostname.unbound.mem.total.sbrk 26767360
servers.hostname.unbound.num.answer.bogus 0
servers.hostname.unbound.num.answer.rcode.NOERROR 46989
servers.hostname.unbound.num.answer.rcode.NXDOMAIN 78575
servers.hostname.unbound.num.answer.rcode.SERVFAIL 55
servers.hostname.unbound.num.answer.rcode.nodata 20566
servers.hostname.unbound.num.answer.secure 0
servers.hostname.unbound.num.query.class.IN 125609
servers.hostname.unbound.num.query.edns.DO 62
servers.hostname.unbound.num.query.edns.present 62
servers.hostname.unbound.num.query.flags.AA 0
servers.hostname.unbound.num.query.flags.AD 0
servers.hostname.unbound.num.query.flags.CD 62
servers.hostname.unbound.num.query.flags.QR 0
servers.hostname.unbound.num.query.flags.RA 0
servers.hostname.unbound.num.query.flags.RD 125609
servers.hostname.unbound.num.query.flags.TC 0
servers.hostname.unbound.num.query.flags.Z 0
servers.hostname.unbound.num.query.ipv6 0
servers.hostname.unbound.num.query.opcode.QUERY 125609
servers.hostname.unbound.num.query.tcp 0
servers.hostname.unbound.num.query.type.A 25596
servers.hostname.unbound.num.query.type.AAAA 99883
servers.hostname.unbound.num.query.type.MX 91
servers.hostname.unbound.num.query.type.PTR 39
servers.hostname.unbound.num.rrset.bogus 0
servers.hostname.unbound.thread0.num.cachehits 10021
servers.hostname.unbound.thread0.num.cachemiss 7
servers.hostname.unbound.thread0.num.prefetch 1
servers.hostname.unbound.thread0.num.queries 10028
servers.hostname.unbound.thread0.num.recursivereplies 9
servers.hostname.unbound.thread0.recursion.time.avg 9.914812
servers.hostname.unbound.thread0.recursion.time.median 0.08192
servers.hostname.unbound.thread0.requestlist.avg 1.25
servers.hostname.unbound.thread0.requestlist.current.all 1
servers.hostname.unbound.thread0.requestlist.current.user 1
servers.hostname.unbound.thread0.requestlist.exceeded 0
servers.hostname.unbound.thread0.requestlist.max 2
servers.hostname.unbound.thread0.requestlist.overwritten 0
servers.hostname.unbound.time.elapsed 9.981882
servers.hostname.unbound.time.now 1361926066.38
servers.hostname.unbound.time.up 3006293.63245
servers.hostname.unbound.total.num.cachehits 125483
servers.hostname.unbound.total.num.cachemiss 126
servers.hostname.unbound.total.num.prefetch 16
servers.hostname.unbound.total.num.queries 125609
servers.hostname.unbound.total.num.recursivereplies 136
servers.hostname.unbound.total.recursion.time.avg 13.045485
servers.hostname.unbound.total.recursion.time.median 0.06016
servers.hostname.unbound.total.requestlist.avg 5.07746
servers.hostname.unbound.total.requestlist.current.all 23
servers.hostname.unbound.total.requestlist.current.user 23
servers.hostname.unbound.total.requestlist.exceeded 0
servers.hostname.unbound.total.requestlist.max 10
servers.hostname.unbound.total.requestlist.overwritten 0
servers.hostname.unbound.unwanted.queries 0
servers.hostname.unbound.unwanted.replies 0
```

