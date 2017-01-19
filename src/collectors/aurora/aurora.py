import diamond.collector

import urllib2


class AuroraCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(AuroraCollector,
                            self).get_default_config_help()

        config_help.update({
            'host': 'Scheduler Hostname',
            'port': 'Scheduler HTTP Metrics Port',
            'path': 'Collector path. Defaults to "aurora"',
            'scheme': 'http'
        })
        return config_help

    def get_default_config(self):
        config = super(AuroraCollector, self).get_default_config()
        config.update({
            'path': 'aurora',
            'host': 'localhost',
            'port': 8081,
            'scheme': 'http'
        })
        return config

    def collect(self):
        url = "%s://%s:%s/vars" % (self.config['scheme'],
                                   self.config['host'],
                                   self.config['port'])

        response = urllib2.urlopen(url)

        for line in response.readlines():
            properties = line.split()

            # Not all lines returned will have a numeric metric.
            # To account for this, we attempt to cast the 'value'
            # portion as a float. If that's not possible, NBD, we
            # just move on.
            try:
                if len(properties) > 1:
                    subpath = properties[0].replace('/', '.').replace('_', '.')
                    value = float(properties[1])

                    self.publish(subpath, value)
            except ValueError:
                continue
