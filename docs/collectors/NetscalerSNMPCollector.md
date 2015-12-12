<!--This file was generated from the python source
Please edit the source to make changes
-->
NetscalerSNMPCollector
=====

SNMPCollector for Netscaler Metrics

NetScaler is a network appliance manufactured by Citrix providing level 4 load
balancing, firewall, proxy and VPN functions.


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
community |  | SNMP community | 
enabled | False | Enable collecting these metrics | bool
exclude_service_type | , | list of service types to exclude (see MIB EntityProtocolType) | list
exclude_vserver_type | , | list of vserver types to exclude (see MIB EntityProtocolType) | list
host |  | netscaler dns address | 
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port |  | Netscaler port to collect snmp data | 
retries | 3 | Number of times to retry before bailing | int
timeout | 15 | Seconds before timing out the snmp connection | int

#### Example Output

```
__EXAMPLESHERE__
```

