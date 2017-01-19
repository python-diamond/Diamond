<!--This file was generated from the python source
Please edit the source to make changes
-->
PuppetAgentCollector
=====

Collect stats from puppet agent's last_run_summary.yaml

#### Dependencies

 * yaml


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
yaml_path | /var/lib/puppet/state/last_run_summary.yaml | Path to last_run_summary.yaml | str

#### Example Output

```
servers.hostname.puppetagent.changes.total 1
servers.hostname.puppetagent.events.failure 0
servers.hostname.puppetagent.events.success 1
servers.hostname.puppetagent.events.total 1
servers.hostname.puppetagent.resources.changed 1
servers.hostname.puppetagent.resources.failed 0
servers.hostname.puppetagent.resources.failed_to_restart 0
servers.hostname.puppetagent.resources.out_of_sync 1
servers.hostname.puppetagent.resources.restarted 0
servers.hostname.puppetagent.resources.scheduled 0
servers.hostname.puppetagent.resources.skipped 6
servers.hostname.puppetagent.resources.total 439
servers.hostname.puppetagent.time.anchor 0.009641
servers.hostname.puppetagent.time.augeas 1.286514
servers.hostname.puppetagent.time.config_retrieval 8.06442093849
servers.hostname.puppetagent.time.cron 0.00089
servers.hostname.puppetagent.time.exec 9.780635
servers.hostname.puppetagent.time.file 1.729348
servers.hostname.puppetagent.time.filebucket 0.000633
servers.hostname.puppetagent.time.firewall 0.007807
servers.hostname.puppetagent.time.group 0.013421
servers.hostname.puppetagent.time.last_run 1377125556
servers.hostname.puppetagent.time.mailalias 0.000335
servers.hostname.puppetagent.time.mount 0.002749
servers.hostname.puppetagent.time.package 1.831337
servers.hostname.puppetagent.time.resources 0.000371
servers.hostname.puppetagent.time.service 0.734021
servers.hostname.puppetagent.time.ssh_authorized_key 0.017625
servers.hostname.puppetagent.time.total 23.5117989385
servers.hostname.puppetagent.time.user 0.02927
servers.hostname.puppetagent.version.config 1377123965
```

