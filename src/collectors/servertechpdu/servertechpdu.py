# coding=utf-8

"""
SNMPCollector for Server Tech PDUs

Server Tech is a manufacturer of PDUs
http://www.servertech.com/

"""

import time
import re
import os
import sys

# Fix Path for locating the SNMPCollector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../',
                                             'snmp',
                                             )))

from diamond.metric import Metric
from snmp import SNMPCollector as parent_SNMPCollector


class ServerTechPDUCollector(parent_SNMPCollector):
    """
    SNMPCollector for ServerTech PDUs
    """

    PDU_SYSTEM_GAUGES = {
        "systemTotalWatts": "1.3.6.1.4.1.1718.3.1.6"
    }

    PDU_INFEED_NAMES = "1.3.6.1.4.1.1718.3.2.2.1.3"

    PDU_INFEED_GAUGES = {
        "infeedCapacityAmps": "1.3.6.1.4.1.1718.3.2.2.1.10",
        "infeedVolts": "1.3.6.1.4.1.1718.3.2.2.1.11",
        "infeedAmps": "1.3.6.1.4.1.1718.3.2.2.1.7",
        "infeedWatts": "1.3.6.1.4.1.1718.3.2.2.1.12"
    }

    def get_default_config_help(self):
        config_help = super(ServerTechPDUCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': 'PDU dns address',
            'port': 'PDU port to collect snmp data',
            'community': 'SNMP community'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ServerTechPDUCollector, self).get_default_config()
        config.update({
            'path':     'pdu',
            'timeout': 15,
            'retries': 3,
        })
        return config

    def collect_snmp(self, device, host, port, community):
        """
        Collect stats from device
        """
        # Log
        self.log.info("Collecting ServerTech PDU statistics from: %s" % device)

        # Set timestamp
        timestamp = time.time()

        inputFeeds = {}

        # Collect PDU input gauge values
        for gaugeName, gaugeOid in self.PDU_SYSTEM_GAUGES.items():
            systemGauges = self.walk(gaugeOid, host, port, community)
            for o, gaugeValue in systemGauges.items():
                # Get Metric Name
                metricName = gaugeName
                # Get Metric Value
                metricValue = float(gaugeValue)
                # Get Metric Path
                metricPath = '.'.join(['devices', device, 'system', metricName])
                # Create Metric
                metric = Metric(metricPath, metricValue, timestamp, 2)
                # Publish Metric
                self.publish_metric(metric)

        # Collect PDU input feed names
        inputFeedNames = self.walk(self.PDU_INFEED_NAMES, host, port, community)
        for o, inputFeedName in inputFeedNames.items():
            # Extract input feed name
            inputFeed = ".".join(o.split(".")[-2:])
            inputFeeds[inputFeed] = inputFeedName

        # Collect PDU input gauge values
        for gaugeName, gaugeOid in self.PDU_INFEED_GAUGES.items():
            inputFeedGauges = self.walk(gaugeOid, host, port, community)
            for o, gaugeValue in inputFeedGauges.items():
                # Extract input feed name
                inputFeed = ".".join(o.split(".")[-2:])

                # Get Metric Name
                metricName = '.'.join([re.sub(r'\.|\\', '_',
                                              inputFeeds[inputFeed]),
                                       gaugeName])

                # Get Metric Value
                if gaugeName == "infeedVolts":
                    # Note: Voltage is in "tenth volts", so divide by 10
                    metricValue = float(gaugeValue) / 10.0
                elif gaugeName == "infeedAmps":
                    # Note: Amps is in "hundredth amps", so divide by 100
                    metricValue = float(gaugeValue) / 100.0
                else:
                    metricValue = float(gaugeValue)

                # Get Metric Path
                metricPath = '.'.join(['devices', device, 'input', metricName])
                # Create Metric
                metric = Metric(metricPath, metricValue, timestamp, 2)
                # Publish Metric
                self.publish_metric(metric)
