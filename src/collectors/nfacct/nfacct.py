# coding=utf-8

"""
Collect counters from Netfilter accounting

#### Dependencies

 * [nfacct](http://www.netfilter.org/projects/nfacct/)

"""

import diamond.collector
from subprocess import Popen, PIPE
import re

from diamond.collector import str_to_bool


class NetfilterAccountingCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = (
            super(NetfilterAccountingCollector, self).get_default_config_help())
        config_help.update({
            'bin': 'The path to the smartctl binary',
            'reset': 'Reset counters after collecting',
            'use_sudo': 'Use sudo?',
            'sudo_cmd': 'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns default configuration options.
        """
        config = super(NetfilterAccountingCollector, self).get_default_config()
        config.update({
            'path': 'nfacct',
            'bin': 'nfacct',
            'use_sudo': False,
            'reset': True,
            'sudo_cmd': '/usr/bin/sudo',
            'method': 'Threaded'
        })
        return config

    def collect(self):
        """
        Collect and publish netfilter counters
        """
        cmd = [self.config['bin'], "list"]

        if str_to_bool(self.config['reset']):
            cmd.append("reset")

        if str_to_bool(self.config['use_sudo']):
            cmd.insert(0, self.config['sudo_cmd'])

        # We avoid use of the XML format to mtaintain compatbility with older
        # versions of nfacct and also to avoid the bug where pkts and bytes were
        # flipped

        # Each line is of the format:
        # { pkts = 00000000000001121700, bytes = 00000000000587037355 } = ipv4;
        matcher = re.compile("{ pkts = (.*), bytes = (.*) } = (.*);")
        lines = Popen(cmd, stdout=PIPE).communicate()[0].strip().splitlines()

        for line in lines:
            matches = re.match(matcher, line)
            if matches:
                num_packets = int(matches.group(1))
                num_bytes = int(matches.group(2))
                name = matches.group(3)
                self.publish(name + ".pkts", num_packets)
                self.publish(name + ".bytes", num_bytes)
