OpenstackSwiftReconCollector
=====

Openstack Swift Recon collector. Reads any present recon cache files and
reports their current metrics.

#### Dependencies

 * Running Swift services must have a recon enabled


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>recon_account_cache</td><td>/var/cache/swift/account.recon</td><td>path to swift recon account cache (default /var/cache/swift/account.recon)</td><td>str</td></tr>
<tr><td>recon_container_cache</td><td>/var/cache/swift/container.recon</td><td>path to swift recon container cache (default /var/cache/swift/container.recon)</td><td>str</td></tr>
<tr><td>recon_object_cache</td><td>/var/cache/swift/object.recon</td><td>path to swift recon object cache (default /var/cache/swift/object.recon)</td><td>str</td></tr>
</table>

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

### This file was generated from the python source
### Please edit the source to make changes

