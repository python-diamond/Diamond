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
