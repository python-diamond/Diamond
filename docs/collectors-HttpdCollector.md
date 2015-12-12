HttpdCollector
=====

Collect stats from Apache HTTPD server using mod_status

#### Dependencies

 * mod_status
 * httplib
 * urlparse


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>urls</td><td>localhost http://localhost:8080/server-status?auto,</td><td>Urls to server-status in auto format, comma seperated, Format 'nickname http://host:port/server-status?auto, , nickname http://host:port/server-status?auto, etc'</td><td>list</td></tr>
</table>

#### Example Output

```
servers.hostname.httpd.nickname1.BusyWorkers 9
servers.hostname.httpd.nickname1.BytesPerReq 5418.55
servers.hostname.httpd.nickname1.BytesPerSec 165
servers.hostname.httpd.nickname1.CleanupWorkers 0
servers.hostname.httpd.nickname1.ClosingWorkers 0
servers.hostname.httpd.nickname1.DnsWorkers 0
servers.hostname.httpd.nickname1.FinishingWorkers 0
servers.hostname.httpd.nickname1.IdleWorkers 0
servers.hostname.httpd.nickname1.KeepaliveWorkers 7
servers.hostname.httpd.nickname1.LoggingWorkers 0
servers.hostname.httpd.nickname1.ReadingWorkers 1
servers.hostname.httpd.nickname1.ReqPerSec 0
servers.hostname.httpd.nickname1.TotalAccesses 8314
servers.hostname.httpd.nickname1.WritingWorkers 1
servers.hostname.httpd.nickname2.BusyWorkers 9
servers.hostname.httpd.nickname2.BytesPerReq 5418.55
servers.hostname.httpd.nickname2.BytesPerSec 165
servers.hostname.httpd.nickname2.CleanupWorkers 0
servers.hostname.httpd.nickname2.ClosingWorkers 0
servers.hostname.httpd.nickname2.DnsWorkers 0
servers.hostname.httpd.nickname2.FinishingWorkers 0
servers.hostname.httpd.nickname2.IdleWorkers 0
servers.hostname.httpd.nickname2.KeepaliveWorkers 7
servers.hostname.httpd.nickname2.LoggingWorkers 0
servers.hostname.httpd.nickname2.ReadingWorkers 1
servers.hostname.httpd.nickname2.ReqPerSec 0
servers.hostname.httpd.nickname2.TotalAccesses 8314
servers.hostname.httpd.nickname2.WritingWorkers 1
```

### This file was generated from the python source
### Please edit the source to make changes

