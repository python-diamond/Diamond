<!--This file was generated from the python source
Please edit the source to make changes
-->
IODriveSNMPCollector
=====

SNMPCollector for Fusion IO DRives Metrics. ( Subclass of snmpCollector )
Based heavily on the NetscalerSNMPCollector.

This collector currently assumes a single IODrive I or IODrive II and not the
DUO, Octals, or multiple IODrive I or IIs. It needs to be enhanced to account
for multiple fio devices. ( Donations being accepted )

The metric path is configured to be under servers.<host>.<device> where host
and device is defined in the IODriveSNMPCollector.conf.  So given the example
conf below the metricpath would be
"servers.my_host.iodrive.<metric> name.

# EXAMPLE CONF file

enabled = True
[devices]
[[iodrive]]
host = my_host
port = 161
community = mycommunitystring


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
community |  | SNMP community | 
enabled | False | Enable collecting these metrics | bool
host |  | Host address | 
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port |  | SNMP port to collect snmp data | 
retries | 3 | Number of times to retry before bailing | int
timeout | 15 | Seconds before timing out the snmp connection | int

#### Example Output

```
__EXAMPLESHERE__
```

