NfsCollector
=====

The NfsCollector collects nfs utilization metrics using /proc/net/rpc/nfs.

#### Dependencies

 * /proc/net/rpc/nfs


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
servers.hostname.nfs.net.packets 0.0
servers.hostname.nfs.net.tcpcnt 0.0
servers.hostname.nfs.net.tcpconn 0.0
servers.hostname.nfs.net.udpcnt 0.0
servers.hostname.nfs.rpc.authrefrsh 0.0
servers.hostname.nfs.rpc.calls 8042864.0
servers.hostname.nfs.rpc.retrans 0.0
servers.hostname.nfs.v2.create 0.0
servers.hostname.nfs.v2.fsstat 0.0
servers.hostname.nfs.v2.getattr 0.0
servers.hostname.nfs.v2.link 0.0
servers.hostname.nfs.v2.lookup 0.0
servers.hostname.nfs.v2.mkdir 0.0
servers.hostname.nfs.v2.null 0.0
servers.hostname.nfs.v2.read 0.0
servers.hostname.nfs.v2.readdir 0.0
servers.hostname.nfs.v2.readlink 0.0
servers.hostname.nfs.v2.remove 0.0
servers.hostname.nfs.v2.rename 0.0
servers.hostname.nfs.v2.rmdir 0.0
servers.hostname.nfs.v2.root 0.0
servers.hostname.nfs.v2.setattr 0.0
servers.hostname.nfs.v2.symlink 0.0
servers.hostname.nfs.v2.wrcache 0.0
servers.hostname.nfs.v2.write 0.0
servers.hostname.nfs.v3.access 40672.0
servers.hostname.nfs.v3.commit 0.0
servers.hostname.nfs.v3.create 91.0
servers.hostname.nfs.v3.fsinfo 0.0
servers.hostname.nfs.v3.fsstat 20830.0
servers.hostname.nfs.v3.getattr 162507.0
servers.hostname.nfs.v3.link 0.0
servers.hostname.nfs.v3.lookup 89.0
servers.hostname.nfs.v3.mkdir 0.0
servers.hostname.nfs.v3.mknod 0.0
servers.hostname.nfs.v3.null 0.0
servers.hostname.nfs.v3.pathconf 0.0
servers.hostname.nfs.v3.read 6093419.0
servers.hostname.nfs.v3.readdir 4002.0
servers.hostname.nfs.v3.readdirplus 0.0
servers.hostname.nfs.v3.readlink 0.0
servers.hostname.nfs.v3.remove 9.0
servers.hostname.nfs.v3.rename 0.0
servers.hostname.nfs.v3.rmdir 0.0
servers.hostname.nfs.v3.setattr 8640.0
servers.hostname.nfs.v3.symlink 0.0
servers.hostname.nfs.v3.write 1712605.0
servers.hostname.nfs.v4.access 0.0
servers.hostname.nfs.v4.close 0.0
servers.hostname.nfs.v4.commit 0.0
servers.hostname.nfs.v4.confirm 0.0
servers.hostname.nfs.v4.create 0.0
servers.hostname.nfs.v4.delegreturn 0.0
servers.hostname.nfs.v4.fs_locations 0.0
servers.hostname.nfs.v4.fsinfo 0.0
servers.hostname.nfs.v4.getacl 0.0
servers.hostname.nfs.v4.getattr 0.0
servers.hostname.nfs.v4.link 0.0
servers.hostname.nfs.v4.lock 0.0
servers.hostname.nfs.v4.lockt 0.0
servers.hostname.nfs.v4.locku 0.0
servers.hostname.nfs.v4.lookup 0.0
servers.hostname.nfs.v4.lookup_root 0.0
servers.hostname.nfs.v4.null 0.0
servers.hostname.nfs.v4.open 0.0
servers.hostname.nfs.v4.open_conf 0.0
servers.hostname.nfs.v4.open_dgrd 0.0
servers.hostname.nfs.v4.open_noat 0.0
servers.hostname.nfs.v4.pathconf 0.0
servers.hostname.nfs.v4.read 0.0
servers.hostname.nfs.v4.readdir 0.0
servers.hostname.nfs.v4.readlink 0.0
servers.hostname.nfs.v4.rel_lkowner 0.0
servers.hostname.nfs.v4.remove 0.0
servers.hostname.nfs.v4.rename 0.0
servers.hostname.nfs.v4.renew 0.0
servers.hostname.nfs.v4.server_caps 0.0
servers.hostname.nfs.v4.setacl 0.0
servers.hostname.nfs.v4.setattr 0.0
servers.hostname.nfs.v4.setclntid 0.0
servers.hostname.nfs.v4.statfs 0.0
servers.hostname.nfs.v4.symlink 0.0
servers.hostname.nfs.v4.write 0.0
```

### This file was generated from the python source
### Please edit the source to make changes

