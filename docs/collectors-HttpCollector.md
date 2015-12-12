HttpCollector
=====

Collect statistics from a HTTP or HTTPS connexion

#### Dependencies

 * urllib2

#### Usage
Add the collector config as :

enabled = True
ttl_multiplier = 2
path_suffix = ""
measure_collector_time = False
byte_unit = byte,
req_vhost = www.my_server.com
req_url = https://www.my_server.com/, https://www.my_server.com/assets/jquery.js

Metrics are collected as :
    - servers.<hostname>.http.<url>.size (size of the page received in bytes)
    - servers.<hostname>.http.<url>.time (time to download the page in microsec)

    '.' and '/' chars are replaced by __, url looking like
       http://www.site.com/admin/page.html are replaced by
       http:__www_site_com_admin_page_html

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>req_port</td><td></td><td>Port</td><td></td></tr>
<tr><td>req_url</td><td>http://localhost/,</td><td>array of full URL to get (ex : https://www.ici.net/mypage.html)</td><td>list</td></tr>
<tr><td>req_vhost</td><td></td><td>Host header variable if needed. Will be added to every request</td><td>str</td></tr>
</table>

#### Example Output

```
servers.hostname.http.http__www_my_server_com_.size 150
```

### This file was generated from the python source
### Please edit the source to make changes

