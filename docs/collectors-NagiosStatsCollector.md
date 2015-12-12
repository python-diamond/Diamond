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
servers.hostname.nagiosstats.AVGACTHSTEXT 4037
servers.hostname.nagiosstats.AVGACTHSTLAT 196
servers.hostname.nagiosstats.AVGACTSVCEXT 340
servers.hostname.nagiosstats.AVGACTSVCLAT 242
servers.hostname.nagiosstats.NUMACTHSTCHECKS5M 56
servers.hostname.nagiosstats.NUMACTSVCCHECKS5M 1101
servers.hostname.nagiosstats.NUMCACHEDHSTCHECKS5M 1
servers.hostname.nagiosstats.NUMCACHEDSVCCHECKS5M 0
servers.hostname.nagiosstats.NUMHSTACTCHK5M 56
servers.hostname.nagiosstats.NUMHSTDOWN 0
servers.hostname.nagiosstats.NUMHSTPSVCHK5M 0
servers.hostname.nagiosstats.NUMHSTUNR 0
servers.hostname.nagiosstats.NUMHSTUP 63
servers.hostname.nagiosstats.NUMOACTHSTCHECKS5M 1
servers.hostname.nagiosstats.NUMOACTSVCCHECKS5M 0
servers.hostname.nagiosstats.NUMPARHSTCHECKS5M 55
servers.hostname.nagiosstats.NUMPSVHSTCHECKS5M 0
servers.hostname.nagiosstats.NUMPSVSVCCHECKS5M 0
servers.hostname.nagiosstats.NUMSACTHSTCHECKS5M 55
servers.hostname.nagiosstats.NUMSACTSVCCHECKS5M 1101
servers.hostname.nagiosstats.NUMSERHSTCHECKS5M 0
servers.hostname.nagiosstats.NUMSVCACTCHK5M 541
servers.hostname.nagiosstats.NUMSVCCRIT 7
servers.hostname.nagiosstats.NUMSVCOK 1409
servers.hostname.nagiosstats.NUMSVCPSVCHK5M 0
servers.hostname.nagiosstats.NUMSVCUNKN 0
servers.hostname.nagiosstats.NUMSVCWARN 3
```

### This file was generated from the python source
### Please edit the source to make changes

