# coding=utf-8

"""
A handler to send metrics to a Wavefront proxy.  The code is derived
from the OpenTSDB handler, as the two protocols are very similar. Tested
with the Wavefront Test Proxy.

[Wavefront](https://www.wavefront.com/) is a hosted analytics service. It
can accept data in various formats, but has the following native format:

```
<metricName> <metricValue> [<timestamp>] source=<source> [<k1>=<"v1"> ..
                                                          <kn>=<"vn">]
```

where kn=vn are "point tags".  These are key=value pairs which apply to
individual points. You can add point tags in the Handler configuration
stanza:

```
[[WavefrontHandler]]
port = 2878
tags = mytag1=myval1,mytag2=myval2
```

in which case they will be applied to all points the handler sends.

You can also set point tags through the publish() method in your
collector, using the `point_tags` parameter, with a dict as the
argument.

```
self.publish('metric', value, point_tags={'mytag1': 'myval1',
                                          'mytag2': 'myval2',})
```

Both the key and value will automatically be wrapped in soft quotes.

This handler will *not* speak directly to the Wavefront API: that is a
different problem.

"""

from Handler import Handler
import socket
import re


class WavefrontHandler(Handler):
    """
    Send metrics to a Wavefront proxy
    """

    RETRY = 3

    def __init__(self, config=None):
        """
        Create a new instance of the WavefrontHandler class
        """

        Handler.__init__(self, config)
        self.socket = None
        self.host = self.config['host']
        self.port = int(self.config['port'])
        self.timeout = int(self.config['timeout'])
        self.metric_format = str(self.config['format'])
        self.tags = self.process_handler_tags(self.config['tags'])
        self._connect()

    def process_handler_tags(self, tags):
        """
        These tags come to us via the handler config. Might be a string,
        might be a list. Whatever, we need to return a list.

        :param: one or more key=value tag pairs. (string or list)
        :returns: a list of key=value pairs. (list)
        """

        if isinstance(tags, list):
            ret = tags
        elif (isinstance(tags, basestring) and tags != ''):
            ret = [tags]
        else:
            ret = []

        return self.quote_point_tags(ret)

    def process_point_tags(self, tags):
        """
        These tags come to us as part of a Metric object. They are a
        dict. We need to make a list, compatible with the output of
        process_handler_tags().

        :param tags: a dict of {key: value} pairs. (dict)
        :returns: a list of key=value pairs. (list)
        """
        if not isinstance(tags, dict):
            return []

        return self.quote_point_tags(['%s=%s' % (k, v) for k, v in
                                     tags.items()])

    def quote_point_tags(self, tags):
        """
        Wavefront allows any characters in point tags, but they need to
        be quoted. We'll be kind and quote them for the user, and also
        throw away tags which aren't a k=v pair.

        :param tags: a list of key=value pairs. (list)
        :returns: a list of quoted and sanitized key=value pairs. (list)
        """

        ret = []

        for t in tags:
            try:
                k, v = t.split('=', 1)
                if not re.match('^".*"$', k):
                    k = '"%s"' % k

                if not re.match('^".*"$', v):
                    v = '"%s"' % v
            except:
                continue

            ret.append('%s=%s' % (k, v))

        return ret

    def get_default_config_help(self):
        """
        Return the help text for the configuration options for this
        handler.
        """

        config = super(WavefrontHandler, self).get_default_config_help()

        config.update({
            'host': 'Wavefront proxy endpoint',
            'port': 'port on Wavefront proxy',
            'timeout': '',
            'format': '',
            'tags': 'key=value point tags',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler.
        """

        config = super(WavefrontHandler, self).get_default_config()

        config.update({
            'host': '',
            'port': 2878,
            'timeout': 5,
            'format': '{Collector}.{Metric} {value} {timestamp} source={host}'
                      ' {tags}',
            'tags': '',
        })

        return config

    def __del__(self):
        """
        Destroy instance of the WavefrontHandler class.
        """

        self._close()

    def process(self, metric):
        """
        Send a metric to the Wavefront proxy. Currently the Test Proxy
        has issues with exponential notation, but the real proxies
        appear not to.

        :param metric: a Diamond metric object
        :returns: sends the metric, formatted as a space-separated
            string.
        """

        metric_str = self.metric_format.format(
            Collector=metric.getCollectorPath(),
            Path=metric.path,
            Metric=metric.getMetricPath(),
            host=metric.host,
            timestamp=metric.timestamp,
            value=metric.value,
            tags=' '.join(self.tags +
                          self.process_point_tags(metric.point_tags))
        )

        self._send(str(metric_str) + '\n')

    def _send(self, data):
        """
        Send data to Wavefront. Data that can not be sent will be
        queued. If it fails, retry until the retry interval has elapsed.

        :param data: the formatted metric. (string)
        """

        retry = self.RETRY

        while retry > 0:
            if not self.socket:
                self.log.error('WavefrontHandler: Socket unavailable.')
                self._connect()
                retry -= 1
                continue

            try:
                self.socket.sendall(data)
                break
            except socket.error, e:
                self.log.error('WavefrontHandler: Failed sending data. %s.', e)
                self._close()
                retry -= 1
                continue

    def _connect(self):
        """
        Connect to a Wavefront proxy.
        """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if socket is None:
            self.log.error('WavefrontHandler: Unable to create socket.')
            self._close()
            return

        self.socket.settimeout(self.timeout)

        try:
            self.socket.connect((self.host, self.port))
            self.log.debug('Established connection to Wavefront proxy %s:%d',
                           self.host, self.port)
        except Exception, ex:
            self.log.error('WavefrontHandler: Failed to connect to %s:%i. %s',
                           self.host, self.port, ex)
            self._close()
            return

    def _close(self):
        """
        Close the socket
        """
        if self.socket is not None:
            self.socket.close()

        self.socket = None
