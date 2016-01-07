<!--This file was generated from the python source
Please edit the source to make changes
-->
AmavisCollector
=====

Collector that reports amavis metrics as reported by amavisd-agent

#### Dependencies

* amavisd-agent must be present in PATH


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
amavisd_exe | /usr/sbin/amavisd-agent | The path to amavisd-agent | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_exe | /usr/bin/sudo | The path to sudo | str
sudo_user | amavis | The user to use if using sudo | str
use_sudo | False | Call amavisd-agent using sudo | bool

#### Example Output

```
servers.hostname.amavis.OutMsgsProtoSMTPRelay.count 22778
servers.hostname.amavis.OutMsgsProtoSMTPRelay.frequency 41
servers.hostname.amavis.OutMsgsProtoSMTPRelay.percentage 71.5
servers.hostname.amavis.OutMsgsSizeProtoSMTP.frequency 0
servers.hostname.amavis.OutMsgsSizeProtoSMTP.percentage 96.4
servers.hostname.amavis.OutMsgsSizeProtoSMTP.size 116
servers.hostname.amavis.TimeElapsedDecoding.frequency 0.024
servers.hostname.amavis.TimeElapsedDecoding.time 652
servers.hostname.amavis.sysUpTime.time 198103058
servers.hostname.amavis.virus.byname.Eicar-Test-Signature.count 4436
servers.hostname.amavis.virus.byname.Eicar-Test-Signature.frequency 8
servers.hostname.amavis.virus.byname.Eicar-Test-Signature.percentage 100.0
```

