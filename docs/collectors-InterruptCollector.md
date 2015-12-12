InterruptCollector
=====

The InterruptCollector class collects metrics on interrupts from
/proc/interrupts

#### Dependencies

 * /proc/interrupts


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

### This file was generated from the python source
### Please edit the source to make changes

