# Example Userscripts

## Collecting Apache http status counters

we use `/usr/local/bin/logster --dry-run --output=stdout syslogapache -D /var/log/syslog`

as a user script in `/etc/diamond/user_scripts/`

to collect:
```
apache.min.http_2xx 36.0
apache.min.http_3xx 0.0
apache.min.http_4xx 0.0
apache.min.http_5xx 0.0
apache.sec.http_2xx 7.2
apache.sec.http_3xx 0.0
apache.sec.http_4xx 0.0
apache.sec.http_5xx 0.0
```

see: [logster](https://github.com/etsy/logster) for details