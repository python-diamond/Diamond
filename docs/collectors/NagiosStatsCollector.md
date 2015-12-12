NagiosStatsCollector
=====

Shells out to get nagios statistics, which may or may not require sudo access

#### Dependencies

 * /usr/sbin/nagios3stats


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>bin</td><td>/usr/sbin/nagios3stats</td><td>Path to nagios3stats binary</td><td>str</td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>sudo_cmd</td><td>/usr/bin/sudo</td><td>Path to sudo</td><td>str</td></tr>
<tr><td>use_sudo</td><td>True</td><td>Use sudo?</td><td>bool</td></tr>
<tr><td>vars</td><td>AVGACTHSTLAT, AVGACTSVCLAT, AVGACTHSTEXT, AVGACTSVCEXT, NUMHSTUP, NUMHSTDOWN, NUMHSTUNR, NUMSVCOK, NUMSVCWARN, NUMSVCUNKN, NUMSVCCRIT, NUMHSTACTCHK5M, NUMHSTPSVCHK5M, NUMSVCACTCHK5M, NUMSVCPSVCHK5M, NUMACTHSTCHECKS5M, NUMOACTHSTCHECKS5M, NUMCACHEDHSTCHECKS5M, NUMSACTHSTCHECKS5M, NUMPARHSTCHECKS5M, NUMSERHSTCHECKS5M, NUMPSVHSTCHECKS5M, NUMACTSVCCHECKS5M, NUMOACTSVCCHECKS5M, NUMCACHEDSVCCHECKS5M, NUMSACTSVCCHECKS5M, NUMPSVSVCCHECKS5M,</td><td>What vars to collect</td><td>list</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

