<!--This file was generated from the python source
Please edit the source to make changes
-->
OpenstackSwiftReconCollector
=====

Openstack Swift Recon collector. Reads any present recon cache files and
reports their current metrics.

#### Dependencies

 * Running Swift services must have a recon enabled


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
recon_account_cache | /var/cache/swift/account.recon | path to swift recon account cache (default /var/cache/swift/account.recon) | str
recon_container_cache | /var/cache/swift/container.recon | path to swift recon container cache (default /var/cache/swift/container.recon) | str
recon_object_cache | /var/cache/swift/object.recon | path to swift recon object cache (default /var/cache/swift/object.recon) | str

#### Example Output

```
servers.hostname.swiftrecon.object.async_pending 0
servers.hostname.swiftrecon.object.object_auditor_stats_ALL.audit_time 301695.104758
servers.hostname.swiftrecon.object.object_auditor_stats_ALL.bytes_processed 24799969235
servers.hostname.swiftrecon.object.object_auditor_stats_ALL.errors 0
servers.hostname.swiftrecon.object.object_auditor_stats_ALL.passes 43887
servers.hostname.swiftrecon.object.object_auditor_stats_ALL.quarantined 0
servers.hostname.swiftrecon.object.object_auditor_stats_ALL.start_time 1357979417.1
servers.hostname.swiftrecon.object.object_auditor_stats_ZBF.audit_time 152991.464428
servers.hostname.swiftrecon.object.object_auditor_stats_ZBF.bytes_processed 0
servers.hostname.swiftrecon.object.object_auditor_stats_ZBF.errors 0
servers.hostname.swiftrecon.object.object_auditor_stats_ZBF.passes 99350
servers.hostname.swiftrecon.object.object_auditor_stats_ZBF.quarantined 0
servers.hostname.swiftrecon.object.object_auditor_stats_ZBF.start_time 1357979462.62
servers.hostname.swiftrecon.object.object_replication_time 2409.80606843
servers.hostname.swiftrecon.object.object_updater_sweep 0.767723798752
```

