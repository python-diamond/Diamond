# coding=utf-8

"""
Collects /sys/kernel/debug/kvm/*

#### Dependencies

 * /sys/kernel/debug/kvm

"""

import diamond.collector
import os


class KVMCollector(diamond.collector.Collector):

    PROC = '/sys/kernel/debug/kvm'

    def get_default_config_help(self):
        config_help = super(KVMCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(KVMCollector, self).get_default_config()
        config.update({
            'path': 'kvm',
        })
        return config

    def collect(self):
        if not os.path.isdir(self.PROC):
            self.log.error('/sys/kernel/debug/kvm is missing. Did you "mount -t'
                           + ' debugfs debugfs /sys/kernel/debug"?')
            return {}

        for filename in os.listdir(self.PROC):
            filepath = os.path.abspath(os.path.join(self.PROC, filename))
            fh = open(filepath, 'r')
            metric_value = self.derivative(filename,
                                           float(fh.readline()),
                                           4294967295)
            self.publish(filename, metric_value)
