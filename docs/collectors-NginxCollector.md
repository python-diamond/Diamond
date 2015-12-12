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


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>req_host</td><td>localhost</td><td>Hostname</td><td>str</td></tr>
<tr><td>req_path</td><td>/nginx_status</td><td>Path</td><td>str</td></tr>
<tr><td>req_port</td><td>8080</td><td>Port</td><td>int</td></tr>
</table>

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

### This file was generated from the python source
### Please edit the source to make changes

