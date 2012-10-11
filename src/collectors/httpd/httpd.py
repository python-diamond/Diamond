# coding=utf-8

"""
Collect stats from Apache HTTPD server using mod_status

#### Dependencies

 * mod_status
 * httplib
 * urlparse

"""

import re
import httplib
import urlparse
import diamond.collector


class HttpdCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(HttpdCollector, self).get_default_config_help()
        config_help.update({
            'url': "Url to server-status in auto format",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(HttpdCollector, self).get_default_config()
        config.update({
            'path':     'httpd',
            'url':      'http://localhost:8080/server-status?auto'
        })
        return config

    def collect(self):
        # Parse Url
        parts = urlparse.urlparse(self.config['url'])

        # Parse host and port
        endpoint = parts[1].split(':')
        if len(endpoint) > 1:
            service_host = endpoint[0]
            service_port = int(endpoint[1])
        else:
            service_host = endpoint[0]
            service_port = 80

        metrics = ['ReqPerSec', 'BytesPerSec', 'BytesPerReq',
                   'BusyWorkers', 'IdleWorkers', 'Total Accesses']

        # Setup Connection
        connection = httplib.HTTPConnection(service_host, service_port)

        try:
            connection.request("GET", "%s?%s" % (parts[2], parts[4]))
        except Exception, e:
            self.log.error("Error retrieving HTTPD stats. %s", e)
            return

        response = connection.getresponse()
        data = response.read()
        exp = re.compile('^([A-Za-z ]+):\s+(.+)$')
        for line in data.split('\n'):
            if line:
                m = exp.match(line)
                if m:
                    k = m.group(1)
                    v = m.group(2)
                    if k in metrics:
                        # Get Metric Name
                        metric_name = "%s" % re.sub('\s+', '', k)
                        # Get Metric Value
                        metric_value = "%d" % float(v)
                        # Publish Metric
                        self.publish(metric_name, metric_value)
