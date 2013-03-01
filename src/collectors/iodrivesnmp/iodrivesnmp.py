# coding=utf-8

"""
SNMPCollector for Fusion IO DRives Metrics. ( Subclass of snmpCollector )
Based heavily on the NetscalerSNMPCollector.

This collecter currently assumes a single IODrive I or IODrive II and not the
DUO, Octals, or multiple IODrive I or IIs. It needs to be enhanced to account
for multiple fio devices. ( Donations being accepted )

The metric path is configured to be under servers.<host>.<device> where host
and device is defined in the IODriveSNMPCollector.conf.  So given the example
conf below the metricpath would be
"servers.my_host.iodrive.<metric> name.

# EXAMPLE CONF file

enabled = True
[devices]
[[iodrive]]
host = my_host
port = 161
community = mycommunitystring

"""

import sys
import os
import time
import struct

# Fix Path for locating the SNMPCollector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../',
                                             'snmp',
                                             )))

from diamond.metric import Metric
from snmp import SNMPCollector as parent_SNMPCollector


class IODriveSNMPCollector(parent_SNMPCollector):
    """
    SNMPCollector for a single Fusion IO Drive
    """

    IODRIVE_STATS = {

        "InternalTemp": "1.3.6.1.4.1.30018.1.2.1.1.1.24.5",

        "MilliVolts": "1.3.6.1.4.1.30018.1.2.1.1.1.32.5",
        "MilliWatts": "1.3.6.1.4.1.30018.1.2.1.1.1.35.5",
        "MilliAmps": "1.3.6.1.4.1.30018.1.2.1.1.1.37.5",
    }

    IODRIVE_BYTE_STATS = {

        "BytesReadU": "1.3.6.1.4.1.30018.1.2.2.1.1.12.5",
        "BytesReadL": "1.3.6.1.4.1.30018.1.2.2.1.1.13.5",

        "BytesWrittenU": "1.3.6.1.4.1.30018.1.2.2.1.1.14.5",
        "BytesWrittenL": "1.3.6.1.4.1.30018.1.2.2.1.1.15.5",

    }

    MAX_VALUE = 18446744073709551615

    def get_default_config_help(self):
        config_help = super(IODriveSNMPCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': 'Host address',
            'port': 'SNMP port to collect snmp data',
            'community': 'SNMP community',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(IODriveSNMPCollector, self).get_default_config()
        config.update({
            'path':     'iodrive',
            'timeout':  15,
        })
        return config

    def get_string_index_oid(self, s):
        """Turns a string into an oid format is length of name followed by
        name chars in ascii"""
        return (len(self.get_bytes(s)), ) + self.get_bytes(s)

    def get_bytes(self, s):
        """Turns a string into a list of byte values"""
        return struct.unpack('%sB' % len(s), s)

    def collect_snmp(self, device, host, port, community):
        """
        Collect Fusion IO Drive SNMP stats from device
        host and device are from the conf file. In the future device should be
        changed to be what IODRive device it being checked.
        i.e. fioa, fiob.
        """

        # Log
        #self.log.info("Collecting Fusion IO Drive statistics from: %s", device)

        # Set timestamp
        timestamp = time.time()

        for k, v in self.IODRIVE_STATS.items():
            # Get Metric Name and Value
            metricName = '.'.join([k])
            metricValue = int(self.get(v, host, port, community)[v])

            # Get Metric Path
            metricPath = '.'.join(['servers', host, device, metricName])

            # Create Metric
            metric = Metric(metricPath, metricValue, timestamp, 0)

            # Publish Metric
            self.publish_metric(metric)

        for k, v in self.IODRIVE_BYTE_STATS.items():
            # Get Metric Name and Value
            metricName = '.'.join([k])
            metricValue = int(self.get(v, host, port, community)[v])

            # Get Metric Path
            metricPath = '.'.join(['servers', host, device, metricName])

            # Create Metric
            metric = Metric(metricPath, metricValue, timestamp, 0)

            # Publish Metric
            self.publish_metric(metric)
