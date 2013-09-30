# coding=utf-8

"""
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

"""

import urllib2
import re
import diamond.collector


class NginxCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(NginxCollector, self).get_default_config_help()
        config_help.update({
            'req_host': 'Hostname',
            'req_port': 'Port',
            'req_path': 'Path',
        })
        return config_help

    def get_default_config(self):
        default_config = super(NginxCollector, self).get_default_config()
        default_config['req_host'] = 'localhost'
        default_config['req_port'] = 8080
        default_config['req_path'] = '/nginx_status'
        default_config['path'] = 'nginx'
        return default_config

    def collect(self):
        activeConnectionsRE = re.compile(r'Active connections: (?P<conn>\d+)')
        totalConnectionsRE = re.compile('^\s+(?P<conn>\d+)\s+'
                                        + '(?P<acc>\d+)\s+(?P<req>\d+)')
        connectionStatusRE = re.compile('Reading: (?P<reading>\d+) '
                                        + 'Writing: (?P<writing>\d+) '
                                        + 'Waiting: (?P<waiting>\d+)')
        req = urllib2.Request('http://%s:%i%s' % (self.config['req_host'],
                                                  int(self.config['req_port']),
                                                  self.config['req_path']))
        try:
            handle = urllib2.urlopen(req)
            for l in handle.readlines():
                l = l.rstrip('\r\n')
                if activeConnectionsRE.match(l):
                    self.publish_gauge(
                        'active_connections',
                        int(activeConnectionsRE.match(l).group('conn')))
                elif totalConnectionsRE.match(l):
                    m = totalConnectionsRE.match(l)
                    req_per_conn = float(m.group('req')) / float(m.group('acc'))
                    self.publish_counter('conn_accepted', int(m.group('conn')))
                    self.publish_counter('conn_handled', int(m.group('acc')))
                    self.publish_counter('req_handled', int(m.group('req')))
                    self.publish_gauge('req_per_conn', float(req_per_conn))
                elif connectionStatusRE.match(l):
                    m = connectionStatusRE.match(l)
                    self.publish_gauge('act_reads', int(m.group('reading')))
                    self.publish_gauge('act_writes', int(m.group('writing')))
                    self.publish_gauge('act_waits', int(m.group('waiting')))
        except IOError, e:
            self.log.error("Unable to open http://%s:%i%s",
                           self.config['req_host'],
                           int(self.config['req_port']),
                           self.config['req_path'])
        except Exception, e:
            self.log.error("Unknown error opening url: %s", e)
