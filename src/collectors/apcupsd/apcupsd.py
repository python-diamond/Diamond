# coding=utf-8

"""
Collects the complete status of most American Power Conversion Corp. (APC) UPSes
provided you have the apcupsd daemon installed, properly configured and
running. It can access status information from any APC UPS attached to the
localhost or attached to any computer on the network which is running
apcuspd in NIS mode.

#### Dependencies

 * apcuspd in NIS mode

"""

import diamond.collector
import socket
from struct import pack
import re
import time


class ApcupsdCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(ApcupsdCollector, self).get_default_config_help()
        config_help.update({
            'hostname': 'Hostname to collect from',
            'port': 'port to collect from. defaults to 3551',
            'metrics': 'List of metrics. Valid metric keys can be found [here]'
            + '(http://www.apcupsd.com/manual/manual.html#status-report-fields)'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ApcupsdCollector, self).get_default_config()
        config.update({
            'path':     'apcupsd',
            'hostname': 'localhost',
            'port': 3551,
            'metrics': ['LINEV', 'LOADPCT', 'BCHARGE', 'TIMELEFT', 'BATTV',
                        'NUMXFERS', 'TONBATT', 'MAXLINEV', 'MINLINEV',
                        'OUTPUTV', 'ITEMP', 'LINEFREQ', 'CUMONBATT', ],
        })
        return config

    def getData(self):
        # Get the data via TCP stream
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.config['hostname'], int(self.config['port'])))

        # Packet is pad byte, size byte, and command
        s.send(pack('xb6s', 6, 'status'))

        # Ditch the header
        s.recv(1024)
        time.sleep(.25)
        data = s.recv(4096)

        # We're done. Close the socket
        s.close()
        return data

    def collect(self):
        metrics = {}
        raw = {}

        data = self.getData()

        data = data.split('\n\x00')
        for d in data:
            matches = re.search("([A-Z]+)\s+:\s+(.*)$", d)
            if matches:
                value = matches.group(2).strip()
                raw[matches.group(1)] = matches.group(2).strip()
                vmatch = re.search("([0-9.]+)", value)
                if not vmatch:
                    continue
                try:
                    value = float(vmatch.group(1))
                except ValueError:
                    continue
                metrics[matches.group(1)] = value

        for metric in self.config['metrics']:
            if metric not in metrics:
                continue

            metric_name = "%s.%s" % (raw['UPSNAME'], metric)

            value = metrics[metric]

            if metric in ['TONBATT', 'CUMONBATT', 'NUMXFERS']:
                value = self.derivative(metric_name, metrics[metric])

            self.publish(metric_name, value)

        return True
