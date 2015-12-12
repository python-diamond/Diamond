<!--This file was generated from the python source
Please edit the source to make changes
-->
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

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
req_port |  | Port | 
req_url | http://localhost/, | array of full URL to get (ex : https://www.ici.net/mypage.html) | list
req_vhost |  | Host header variable if needed. Will be added to every request | str

#### Example Output

```
servers.hostname.http.http__www_my_server_com_.size 150
```

