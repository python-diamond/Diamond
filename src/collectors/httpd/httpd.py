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

    def process_config(self):
        super(HttpdCollector, self).process_config()
        if 'url' in self.config:
            self.config['urls'].append(self.config['url'])

        self.urls = {}
        if isinstance(self.config['urls'], basestring):
            self.config['urls'] = self.config['urls'].split(',')

        for url in self.config['urls']:
            # Handle the case where there is a trailing comman on the urls list
            if len(url) == 0:
                continue
            if ' ' in url:
                parts = url.split(' ')
                self.urls[parts[0]] = parts[1]
            else:
                self.urls[''] = url

    def get_default_config_help(self):
        config_help = super(HttpdCollector, self).get_default_config_help()
        config_help.update({
            'urls': "Urls to server-status in auto format, comma seperated," +
                    " Format 'nickname http://host:port/server-status?auto, " +
                    ", nickname http://host:port/server-status?auto, etc'",
            'redirects': "The maximum number of redirect requests to follow.",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(HttpdCollector, self).get_default_config()
        config.update({
            'path': 'httpd',
            'urls': ['localhost http://localhost:8080/server-status?auto'],
            'redirects': 5,
        })
        return config

    def collect(self):
        for nickname in self.urls.keys():
            url = self.urls[nickname]

            try:
                redirects = 0
                while True:
                    # Parse Url
                    parts = urlparse.urlparse(url)

                    # Set httplib class
                    if parts.scheme == 'http':
                        connection = httplib.HTTPConnection(parts.netloc)
                    elif parts.scheme == 'https':
                        connection = httplib.HTTPSConnection(parts.netloc)
                    else:
                        raise Exception("Invalid scheme: %s" % parts.scheme)

                    # Setup Connection
                    url = "%s?%s" % (parts.path, parts.query)
                    connection.request("GET", url)
                    response = connection.getresponse()
                    data = response.read()
                    headers = dict(response.getheaders())
                    if (('location' not in headers or
                         headers['location'] == url)):
                        connection.close()
                        break
                    url = headers['location']
                    connection.close()

                    redirects += 1
                    if redirects > self.config['redirects']:
                        raise Exception("Too many redirects!")
            except Exception, e:
                self.log.error(
                    "Error retrieving HTTPD stats for '%s': %s",
                    url, e)
                continue

            exp = re.compile('^([A-Za-z ]+):\s+(.+)$')
            for line in data.split('\n'):
                if line:
                    m = exp.match(line)
                    if m:
                        k = m.group(1)
                        v = m.group(2)

                        # IdleWorkers gets determined from the scoreboard
                        if k == 'IdleWorkers':
                            continue

                        if k == 'Scoreboard':
                            for sb_kv in self._parseScoreboard(v):
                                self._publish(nickname, sb_kv[0], sb_kv[1])
                        else:
                            self._publish(nickname, k, v)

    def _publish(self, nickname, key, value):

        metrics = ['ReqPerSec', 'BytesPerSec', 'BytesPerReq', 'BusyWorkers',
                   'Total Accesses', 'IdleWorkers', 'StartingWorkers',
                   'ReadingWorkers', 'WritingWorkers', 'KeepaliveWorkers',
                   'DnsWorkers', 'ClosingWorkers', 'LoggingWorkers',
                   'FinishingWorkers', 'CleanupWorkers', 'ConnsAsyncClosing',
                   'CPUUser', 'CacheSubcaches', 'CacheCurrentEntries',
                   'CPULoad', 'Total kBytes', 'CacheIndexesPerSubcaches',
                   'CPUChildrenSystem', 'ConnsAsyncWriting',
                   'CacheSharedMemory', 'ServerUptimeSeconds',
                   'CacheStoreCount', 'CacheExpireCount',
                   'CacheReplaceCount', 'CPUChildrenUser', 'ConnsTotal',
                   'CacheRetrieveMissCount', 'CacheRetrieveHitCount',
                   'CacheTimeLeftOldestMax', 'CacheDiscardCount',
                   'CacheRemoveHitCount', 'CacheTimeLeftOldestMin',
                   'CPUSystem', 'ConnsAsyncKeepAlive',
                   'CacheTimeLeftOldestAvg', 'CacheRemoveMissCount',
                   'CacheIndexUsage', 'CacheUsage']

        metrics_precision = ['ReqPerSec', 'BytesPerSec', 'BytesPerReq',
                             'CPULoad', 'CPUUser', 'CPUSystem']

        if key in metrics:
            # Get Metric Name
            presicion_metric = False
            metric_name = "%s" % re.sub('\s+', '', key)
            if metric_name in metrics_precision:
                presicion_metric = 1

            # Prefix with the nickname?
            if len(nickname) > 0:
                metric_name = nickname + '.' + metric_name

            # Strip percent mark from Cache*Usage
            try:
                value = value.replace('%', '')
            except AttributeError:
                pass

            # Use precision for ReqPerSec BytesPerSec BytesPerReq
            if presicion_metric:
                # Get Metric Value
                metric_value = "%f" % float(value)

                # Publish Metric
                self.publish(metric_name, metric_value, precision=5)
            else:
                # Get Metric Value
                metric_value = "%d" % float(value)

                # Publish Metric
                self.publish(metric_name, metric_value)

    def _parseScoreboard(self, sb):

        ret = []

        ret.append(('IdleWorkers', sb.count('_')))
        ret.append(('ReadingWorkers', sb.count('R')))
        ret.append(('WritingWorkers', sb.count('W')))
        ret.append(('KeepaliveWorkers', sb.count('K')))
        ret.append(('DnsWorkers', sb.count('D')))
        ret.append(('ClosingWorkers', sb.count('C')))
        ret.append(('LoggingWorkers', sb.count('L')))
        ret.append(('FinishingWorkers', sb.count('G')))
        ret.append(('CleanupWorkers', sb.count('I')))

        return ret
