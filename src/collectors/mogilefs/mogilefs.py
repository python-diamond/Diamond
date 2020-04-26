# coding=utf-8

"""
Collect statistics from Mogilefs

#### Dependencies

 * telnetlib
 * time


"""
import diamond.collector
import telnetlib
import time


class MogilefsCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(MogilefsCollector, self).get_default_config_help()
        config_help.update({
            'path': 'Metric path',
        })
        return config_help

    def get_default_config(self):
        config = super(MogilefsCollector, self).get_default_config()
        config.update({
            'path':     'mogilefs'
        })
        return config

    def collect(self):
        tn = telnetlib.Telnet("127.0.0.1", 7001, 3)
        time.sleep(1)
        tn.write("!stats" + '\r\n')
        out = tn.read_until('.', 3)

        myvars = {}

        for line in out.splitlines()[:-1]:
            name, var = line.partition(" ")[::2]
            myvars[name.strip()] = long(var)

        for key, value in myvars.iteritems():
            # Set Metric Name
            metric_name = key
            # Set Metric Value
            metric_value = value
            # Publish Metric
            self.publish(metric_name, metric_value)
