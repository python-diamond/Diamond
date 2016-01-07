<!--This file was generated from the python source
Please edit the source to make changes
-->
NagiosStatsCollector
=====

Shells out to get nagios statistics, which may or may not require sudo access

#### Dependencies

 * /usr/sbin/nagios3stats


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
bin | /usr/sbin/nagios3stats | Path to nagios3stats binary | str
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
sudo_cmd | /usr/bin/sudo | Path to sudo | str
use_sudo | True | Use sudo? | bool
vars | AVGACTHSTLAT, AVGACTSVCLAT, AVGACTHSTEXT, AVGACTSVCEXT, NUMHSTUP, NUMHSTDOWN, NUMHSTUNR, NUMSVCOK, NUMSVCWARN, NUMSVCUNKN, NUMSVCCRIT, NUMHSTACTCHK5M, NUMHSTPSVCHK5M, NUMSVCACTCHK5M, NUMSVCPSVCHK5M, NUMACTHSTCHECKS5M, NUMOACTHSTCHECKS5M, NUMCACHEDHSTCHECKS5M, NUMSACTHSTCHECKS5M, NUMPARHSTCHECKS5M, NUMSERHSTCHECKS5M, NUMPSVHSTCHECKS5M, NUMACTSVCCHECKS5M, NUMOACTSVCCHECKS5M, NUMCACHEDSVCCHECKS5M, NUMSACTSVCCHECKS5M, NUMPSVSVCCHECKS5M, | What vars to collect | list

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

