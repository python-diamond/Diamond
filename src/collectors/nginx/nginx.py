# coding=utf-8

"""
Collect statistics from Nginx and Nginx+

#### Dependencies

 * urllib2
 * json

#### Usage

For open source nginx:

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

For commercial nginx+:

    To enable the nginx status page to work with defaults,
    add a file to /etc/nginx/sites-enabled/ (on Ubuntu) with the
    following content:
    <pre>
    server  {
        listen *:8080;

        root /usr/share/nginx/html;

        location /nginx_status {
            status;
            allow 127.0.0.1;
            deny all;
        }

        location /status {
            status;
            allow 127.0.0.1;
            deny all;
        }
        location  = /status.html { }
    }
    </pre>

"""

import urllib2
import re
import diamond.collector
import json


class NginxCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(NginxCollector, self).get_default_config_help()
        config_help.update({
            'precision': 'Number of decimal places to report to',
            'req_host': 'Hostname',
            'req_port': 'Port',
            'req_path': 'Path',
            'req_ssl': 'SSL Support',
            'req_host_header': 'HTTP Host header (required for SSL)',
        })
        return config_help

    def get_default_config(self):
        default_config = super(NginxCollector, self).get_default_config()
        default_config['precision'] = 0
        default_config['req_host'] = 'localhost'
        default_config['req_port'] = 8080
        default_config['req_path'] = '/nginx_status'
        default_config['req_ssl'] = False
        default_config['req_host_header'] = None
        default_config['path'] = 'nginx'
        return default_config

    def collect_nginx(self, status):
        activeConnectionsRE = re.compile(r'Active connections: (?P<conn>\d+)')
        totalConnectionsRE = re.compile('^\s+(?P<conn>\d+)\s+' +
                                        '(?P<acc>\d+)\s+(?P<req>\d+)')
        connectionStatusRE = re.compile('Reading: (?P<reading>\d+) ' +
                                        'Writing: (?P<writing>\d+) ' +
                                        'Waiting: (?P<waiting>\d+)')
        precision = int(self.config['precision'])

        for l in status.readlines():
            l = l.rstrip('\r\n')
            if activeConnectionsRE.match(l):
                self.publish_gauge(
                    'active_connections',
                    int(activeConnectionsRE.match(l).group('conn')),
                    precision)
            elif totalConnectionsRE.match(l):
                m = totalConnectionsRE.match(l)
                req_per_conn = float(m.group('req')) / \
                    float(m.group('acc'))
                self.publish_counter('conn_accepted',
                                     int(m.group('conn')),
                                     precision)
                self.publish_counter('conn_handled',
                                     int(m.group('acc')),
                                     precision)
                self.publish_counter('req_handled',
                                     int(m.group('req')),
                                     precision)
                self.publish_gauge('req_per_conn',
                                   float(req_per_conn),
                                   precision)
            elif connectionStatusRE.match(l):
                m = connectionStatusRE.match(l)
                self.publish_gauge('act_reads',
                                   int(m.group('reading')),
                                   precision)
                self.publish_gauge('act_writes',
                                   int(m.group('writing')),
                                   precision)
                self.publish_gauge('act_waits',
                                   int(m.group('waiting')),
                                   precision)

    def collect_nginx_plus(self, status):
        # Collect standard stats
        self.collect_connections(status['connections'])
        self.collect_requests(status['requests'])

        # Collect specialty stats, if present
        if 'server_zones' in status:
            self.collect_server_zones(status['server_zones'])
        if 'ssl' in status:
            self.collect_ssl(status['ssl'])
        if 'upstreams' in status:
            self.collect_upstreams(status['upstreams'])

    def collect_connections(self, status):
        self.publish_gauge('conn.active', status['active'])
        self.publish_counter('conn.accepted', status['accepted'])
        self.publish_counter('conn.dropped', status['dropped'])
        self.publish_gauge('conn.idle', status['idle'])

    def collect_requests(self, status):
        self.publish_gauge('req.current', status['current'])
        self.publish_counter('req.total', status['total'])

    def collect_server_zones(self, status):
        for zone in status:
            prefix = 'servers.%s' % re.sub('\.', '_', zone)

            self.publish_gauge('%s.processing' % (prefix),
                               status[zone]['processing'])

            for counter in ['requests', 'discarded', 'received', 'sent']:
                self.publish_counter('%s.%s' % (prefix, counter),
                                     status[zone][counter])

            for code in status[zone]['responses']:
                self.publish_counter('%s.responses.%s' % (prefix, code),
                                     status[zone]['responses'][code])

    def collect_ssl(self, status):
        for stat in ['handshakes', 'session_reuses', 'handshakes_failed']:
            self.publish_counter('ssl.%s' % stat, status[stat])

    def collect_upstreams(self, status):
        for upstream in status:
            prefix = 'upstreams.%s' % re.sub('\.', '_', upstream)
            self.publish_gauge('%s.keepalive' % prefix,
                               status[upstream]['keepalive'])

            for peer in status[upstream]['peers']:

                peer_prefix = '%s.peers.%s' % (prefix, re.sub(':', "-",
                                               re.sub('\.', '_',
                                                      peer['server'])))

                self.publish_gauge('%s.active' % peer_prefix, peer['active'])
                if 'max_conns' in peer:
                    self.publish_gauge('%s.max_conns' % peer_prefix,
                                       peer['max_conns'])

                for counter in ['downtime', 'fails', 'received', 'requests',
                                'sent', 'unavail']:
                    self.publish_counter('%s.%s' %
                                         (peer_prefix, counter), peer[counter])

                for code in peer['responses']:
                    self.publish_counter('%s.responses.%s' %
                                         (peer_prefix, code),
                                         peer['responses'][code])

    def collect(self):
        # Determine what HTTP scheme to use based on SSL usage or not
        if str(self.config['req_ssl']).lower() == 'true':
            scheme = 'https'
        else:
            scheme = 'http'

        # Add host headers if present (Required for SSL cert validation)
        if self.config['req_host_header'] is not None:
            headers = {'Host': str(self.config['req_host_header'])}
        else:
            headers = {}
        url = '%s://%s:%i%s' % (scheme,
                                self.config['req_host'],
                                int(self.config['req_port']),
                                self.config['req_path'])

        req = urllib2.Request(url=url, headers=headers)
        try:
            handle = urllib2.urlopen(req)

            # Test for json payload; indicates nginx+
            if handle.info().gettype() == 'application/json':
                self.collect_nginx_plus(json.load(handle))

            # Plain payload; indicates open source nginx
            elif handle.info().gettype() == 'text/plain':
                self.collect_nginx(handle)

        except IOError, e:
            self.log.error("Unable to open %s" % url)
        except Exception, e:
            self.log.error("Unknown error opening url: %s", e)
