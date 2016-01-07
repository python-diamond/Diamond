<!--This file was generated from the python source
Please edit the source to make changes
-->
InterruptCollector
=====

The InterruptCollector class collects metrics on interrupts from
/proc/interrupts

#### Dependencies

 * /proc/interrupts


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
servers.hostname.interrupts.IO-APIC-edge.timer.0.CPU0 318660.0
servers.hostname.interrupts.IO-APIC-edge.timer.0.total 318660.0
servers.hostname.interrupts.IO-APIC-level_3w-sas.CPU6 301014.0
servers.hostname.interrupts.IO-APIC-level_3w-sas.total 301014.0
servers.hostname.interrupts.PCI-MSI-X.eth3-rx-1.51.CPU6 293.0
servers.hostname.interrupts.PCI-MSI-X.eth3-rx-1.51.CPU7 330.0
servers.hostname.interrupts.PCI-MSI-X.eth3-rx-1.51.CPU9 286.0
servers.hostname.interrupts.PCI-MSI-X.eth3-rx-1.51.total 909.0
servers.hostname.interrupts.PCI-MSI-X.eth3-rx-2.59.CPU21 98790.0
servers.hostname.interrupts.PCI-MSI-X.eth3-rx-2.59.total 98790.0
servers.hostname.interrupts.PCI-MSI-X.eth3-rx-3.67.CPU7 743.0
servers.hostname.interrupts.PCI-MSI-X.eth3-rx-3.67.CPU9 378.0
servers.hostname.interrupts.PCI-MSI-X.eth3-rx-3.67.total 1121.0
servers.hostname.interrupts.PCI-MSI-X.eth3-tx-0.75.CPU23 304345.0
servers.hostname.interrupts.PCI-MSI-X.eth3-tx-0.75.total 304345.0
servers.hostname.interrupts.PCI-MSI-X_eth2-rx-0.CPU20 20570.0
servers.hostname.interrupts.PCI-MSI-X_eth2-rx-0.total 20570.0
servers.hostname.interrupts.PCI-MSI-X_eth2-rx-1.CPU6 94.0
servers.hostname.interrupts.PCI-MSI-X_eth2-rx-1.CPU7 15.0
servers.hostname.interrupts.PCI-MSI-X_eth2-rx-1.CPU9 50.0
servers.hostname.interrupts.PCI-MSI-X_eth2-rx-1.total 159.0
servers.hostname.interrupts.PCI-MSI-X_eth2-rx-2.CPU17 159.0
servers.hostname.interrupts.PCI-MSI-X_eth2-rx-2.total 159.0
servers.hostname.interrupts.PCI-MSI-X_eth2-rx-3.CPU8 159.0
servers.hostname.interrupts.PCI-MSI-X_eth2-rx-3.total 159.0
servers.hostname.interrupts.PCI-MSI-X_eth2-tx-0.CPU16 159.0
servers.hostname.interrupts.PCI-MSI-X_eth2-tx-0.total 159.0
servers.hostname.interrupts.PCI-MSI-X_eth3-rx-0.CPU22 224074.0
servers.hostname.interrupts.PCI-MSI-X_eth3-rx-0.total 224074.0
servers.hostname.interrupts.PCI-MSI_eth0.CPU18 10397.0
servers.hostname.interrupts.PCI-MSI_eth0.total 10397.0
servers.hostname.interrupts.PCI-MSI_eth1.CPU19 10386.0
servers.hostname.interrupts.PCI-MSI_eth1.total 10386.0
```

