SmartCollector
=====

Collect data from S.M.A.R.T.'s attribute reporting.

#### Dependencies

 * [smartmontools](http://sourceforge.net/apps/trac/smartmontools/wiki)


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>bin</td><td>smartctl</td><td>The path to the smartctl binary</td><td>str</td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>devices</td><td>^disk[0-9]$|^sd[a-z]$|^hd[a-z]$</td><td>device regex to collect stats on</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>sudo_cmd</td><td>/usr/bin/sudo</td><td>Path to sudo</td><td>str</td></tr>
<tr><td>use_sudo</td><td>False</td><td>Use sudo?</td><td>bool</td></tr>
</table>

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

### This file was generated from the python source
### Please edit the source to make changes

