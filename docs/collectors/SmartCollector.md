<!--This file was generated from the python source
Please edit the source to make changes
-->
SmartCollector
=====

Collect data from S.M.A.R.T.'s attribute reporting.

#### Dependencies

 * [smartmontools](http://sourceforge.net/apps/trac/smartmontools/wiki)


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | smartctl | The path to the smartctl binary | str
byte_unit | byte | Default numeric output(s) | str
devices | ^disk[0-9]$|^sd[a-z]$|^hd[a-z]$ | device regex to collect stats on | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | False | Use sudo? | bool

#### Example Output

```
servers.hostname.smart.sda.Calibration_Retry_Count 0
servers.hostname.smart.sda.Current_Pending_Sector 0
servers.hostname.smart.sda.Load_Cycle_Count 2
servers.hostname.smart.sda.Multi_Zone_Error_Rate 0
servers.hostname.smart.sda.Offline_Uncorrectable 0
servers.hostname.smart.sda.Power-Off_Retract_Count 5
servers.hostname.smart.sda.Power_Cycle_Count 7
servers.hostname.smart.sda.Power_On_Hours 6827
servers.hostname.smart.sda.Raw_Read_Error_Rate 0
servers.hostname.smart.sda.Reallocated_Event_Count 0
servers.hostname.smart.sda.Reallocated_Sector_Ct 0
servers.hostname.smart.sda.Seek_Error_Rate 0
servers.hostname.smart.sda.Spin_Retry_Count 0
servers.hostname.smart.sda.Spin_Up_Time 3991
servers.hostname.smart.sda.Start_Stop_Count 8
servers.hostname.smart.sda.Temperature_Celsius 28
servers.hostname.smart.sda.UDMA_CRC_Error_Count 0
```

