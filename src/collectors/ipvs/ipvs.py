# coding=utf-8

"""
Shells out to get ipvs statistics, which may or may not require sudo access

#### Dependencies

 * /usr/sbin/ipvsadmin

"""

import diamond.collector
import subprocess
import os
import string


class IPVSCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(IPVSCollector, self).get_default_config_help()
        config_help.update({
            'bin': 'Path to ipvsadm binary',
            'use_sudo': 'Use sudo?',
            'sudo_cmd': 'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(IPVSCollector, self).get_default_config()
        config.update({
            'bin':              '/usr/sbin/ipvsadm',
            'use_sudo':         True,
            'sudo_cmd':         '/usr/bin/sudo',
            'path':             'ipvs'
        })
        return config

    def collect(self):
        if not os.access(self.config['bin'], os.X_OK) or (self.config['use_sudo'] and not os.access(self.config['sudo_cmd'], os.X_OK)):
            return

        command = [self.config['bin'], '--list', '--stats', '--numeric', '--exact']

        if self.config['use_sudo']:
            command.insert(0, self.config['sudo_cmd'])

        p = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0][:-1]

        columns = {
            'conns': 2,
            'inpkts': 3,
            'outpkts': 4,
            'inbytes': 5,
            'outbytes': 6,
        }

        external = ""
        backend = ""
        for i, line in enumerate(p.split("\n")):
            if i < 3:
                continue
            row = line.split()

            if row[0] == "TCP" or row[0] == "UDP":
                external = string.replace(row[1], ".", "_")
                backend = "total"
            elif row[0] == "->":
                backend = string.replace(row[1], ".", "_")
            else:
                continue

            for metric, column in columns.iteritems():
                metric_name = ".".join([external, backend, metric])
                metric_value = int(row[column])

                self.publish(metric_name, metric_value)
