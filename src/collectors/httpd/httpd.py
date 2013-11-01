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

    def __init__(self, *args, **kwargs):
        super(HttpdCollector, self).__init__(*args, **kwargs)
        if 'url' in self.config:
            self.config['urls'].append(self.config['url'])

        self.urls = {}
        for url in self.config['urls']:
            if ' ' in url:
                parts = url.split(' ')
                self.urls[parts[0]] = parts[1]
            else:
                self.urls[''] = url

    def get_default_config_help(self):
        config_help = super(HttpdCollector, self).get_default_config_help()
        config_help.update({
            'urls': "Urls to server-status in auto format, comma seperated,"
            + " Format 'nickname http://host:port/server-status?auto, "
            + ", nickname http://host:port/server-status?auto, etc'",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(HttpdCollector, self).get_default_config()
        config.update({
            'path':     'httpd',
            'urls':     ['localhost http://localhost:8080/server-status?auto']
        })
        return config

    def collect(self):
        for nickname in self.urls.keys():
            url = self.urls[nickname]

            metrics = ['ReqPerSec', 'BytesPerSec', 'BytesPerReq',
                       'BusyWorkers', 'IdleWorkers', 'Total Accesses']

            try:
                while True:

                    # Parse Url
                    parts = urlparse.urlparse(url)

                    # Parse host and port
                    endpoint = parts[1].split(':')
                    if len(endpoint) > 1:
                        service_host = endpoint[0]
                        service_port = int(endpoint[1])
                    else:
                        service_host = endpoint[0]
                        service_port = 80

                    # Setup Connection
                    connection = httplib.HTTPConnection(service_host,
                                                        service_port)

                    url = "%s?%s" % (parts[2], parts[4])

                    connection.request("GET", url)
                    response = connection.getresponse()
                    data = response.read()
                    headers = dict(response.getheaders())
                    if ('location' not in headers
                        or headers['location'] == url):
                        connection.close()
                        break
                    url = headers['location']
                    connection.close()
            except Exception, e:
                self.log.error(
                    "Error retrieving HTTPD stats for host %s:%s, url '%s': %s",
                    service_host, str(service_port), url, e)
                continue

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

                            # Prefix with the nickname?
                            if len(nickname) > 0:
                                metric_name = nickname + '.' + metric_name

                            # Get Metric Value
                            metric_value = "%d" % float(v)

                            # Publish Metric
                            self.publish(metric_name, metric_value)
