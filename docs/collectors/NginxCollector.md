<!--This file was generated from the python source
Please edit the source to make changes
-->
NginxCollector
=====

Collect statistics from Nginx

#### Dependencies

 * urllib2

#### Usage

To enable the nginx status page to work with defaults,
add a file to /etc/nginx/sites-enabled/ (on Ubuntu) with the
following content:
<pre>
  server {
      listen 127.0.0.1:8080;
      server_name localhost;
      location /nginx_status {
          stub_status on;
          access_log /data/server/shared/log/access.log;
          allow 127.0.0.1;
          deny all;
      }
  }
</pre>


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
precision | 0 | Number of decimal places to report to | int
req_host | localhost | Hostname | str
req_host_header | None | HTTP Host header (required for SSL) | NoneType
req_path | /nginx_status | Path | str
req_port | 8080 | Port | int
req_ssl | False | SSL Support | bool

#### Example Output

```
servers.hostname.nginx.act_reads 2
servers.hostname.nginx.act_waits 0
servers.hostname.nginx.act_writes 1
servers.hostname.nginx.active_connections 3
servers.hostname.nginx.conn_accepted 396396
servers.hostname.nginx.conn_handled 396396
servers.hostname.nginx.req_handled 396396
```

