<!--This file was generated from the python source
Please edit the source to make changes
-->
ServerTechPDUCollector
=====

SNMPCollector for Server Tech PDUs

Server Tech is a manufacturer of PDUs
http://www.servertech.com/


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
community |  | SNMP community | 
enabled | False | Enable collecting these metrics | bool
host |  | PDU dns address | 
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port |  | PDU port to collect snmp data | 
retries | 3 | Number of times to retry before bailing | int
timeout | 15 | Seconds before timing out the snmp connection | int

#### Example Output

```
__EXAMPLESHERE__
```

