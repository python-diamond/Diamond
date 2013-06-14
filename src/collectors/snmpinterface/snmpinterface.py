# coding=utf-8

"""
The SNMPInterfaceCollector is designed for collecting interface data from
remote SNMP-enabled devices such as routers and switches using SNMP IF_MIB

#### Installation

The snmpinterfacecollector.py module should be installed into your Diamond
installation collectors directory. This directory is defined
in diamond.cfg under the *collectors_path* directive. This defaults to
*/usr/lib/diamond/collectors/* on Ubuntu.

The SNMPInterfaceCollector.cfg file should be installed into your diamond
installation config directory. This directory is defined
in diamond.cfg under the *collectors_config_path* directive. This defaults to
*/etc/diamond/* on Ubuntu.

Once the collector is installed and configured, you can wait for diamond to
pick up the new collector automatically, or simply restart diamond.

#### Configuration

Below is an example configuration for the SNMPInterfaceCollector. The collector
can collect data any number of devices by adding configuration sections
under the *devices* header. By default the collector will collect every 60
seconds. This might be a bit excessive and put unnecessary load on the
devices being polled. You may wish to change this to every 300 seconds. However
you need modify your graphite data retentions to handle this properly.

```
    # Options for SNMPInterfaceCollector
    path = interface
    interval = 60

    [devices]

    [[router1]]
    host = router1.example.com
    port = 161
    community = public

    [[router2]]
    host = router1.example.com
    port = 161
    community = public
```

Note: If you modify the SNMPInterfaceCollector configuration, you will need to
restart diamond.

#### Dependencies

 * pysmnp

"""

import os
import sys
import re

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'snmp'))
from snmp import SNMPCollector as parent_SNMPCollector
import diamond.convertor


class SNMPInterfaceCollector(parent_SNMPCollector):

    # IF-MIB OID
    IF_MIB_INDEX_OID = "1.3.6.1.2.1.2.2.1.1"
    IF_MIB_NAME_OID = "1.3.6.1.2.1.31.1.1.1.1"
    IF_MIB_TYPE_OID = "1.3.6.1.2.1.2.2.1.3"

    # A list of IF-MIB 32bit counters to walk
    IF_MIB_GAUGE_OID_TABLE = {'ifInDiscards': "1.3.6.1.2.1.2.2.1.13",
                              'ifInErrors': "1.3.6.1.2.1.2.2.1.14",
                              'ifOutDiscards': "1.3.6.1.2.1.2.2.1.19",
                              'ifOutErrors': "1.3.6.1.2.1.2.2.1.20"}

    # A list of IF-MIB 64bit counters to talk
    IF_MIB_COUNTER_OID_TABLE = {'ifHCInOctets': "1.3.6.1.2.1.31.1.1.1.6",
                                'ifInUcastPkts': "1.3.6.1.2.1.31.1.1.1.7",
                                'ifInMulticastPkts': "1.3.6.1.2.1.31.1.1.1.8",
                                'ifInBroadcastPkts': "1.3.6.1.2.1.31.1.1.1.9",
                                'ifHCOutOctets': "1.3.6.1.2.1.31.1.1.1.10",
                                'ifOutUcastPkts': "1.3.6.1.2.1.31.1.1.1.11",
                                'ifOutMulticastPkts': "1.3.6.1.2.1.31.1.1.1.12",
                                'ifOutBroadcastPkts': "1.3.6.1.2.1.31.1.1.1.13"}

    # A list of interface types we care about
    IF_TYPES = ["6"]

    def get_default_config_help(self):
        config_help = super(SNMPInterfaceCollector,
                            self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Override SNMPCollector.get_default_config method to provide
        default_config for the SNMPInterfaceCollector
        """
        default_config = super(SNMPInterfaceCollector,
                               self).get_default_config()
        default_config['path'] = 'interface'
        default_config['byte_unit'] = ['bit', 'byte']
        return default_config

    def collect_snmp(self, device, host, port, community):
        """
        Collect SNMP interface data from device
        """
        # Log
        self.log.info("Collecting SNMP interface statistics from: %s", device)

        # Define a list of interface indexes
        ifIndexes = []

        # Get Interface Indexes
        ifIndexOid = '.'.join([self.IF_MIB_INDEX_OID])
        ifIndexData = self.walk(ifIndexOid, host, port, community)
        ifIndexes = [v for v in ifIndexData.values()]

        for ifIndex in ifIndexes:
            # Get Interface Type
            ifTypeOid = '.'.join([self.IF_MIB_TYPE_OID, ifIndex])
            ifTypeData = self.get(ifTypeOid, host, port, community)
            if ifTypeData[ifTypeOid] not in self.IF_TYPES:
                # Skip Interface
                continue
            # Get Interface Name
            ifNameOid = '.'.join([self.IF_MIB_NAME_OID, ifIndex])
            ifNameData = self.get(ifNameOid, host, port, community)
            ifName = ifNameData[ifNameOid]
            # Remove quotes from string
            ifName = re.sub(r'(\"|\')', '', ifName)

            # Get Gauges
            for gaugeName, gaugeOid in self.IF_MIB_GAUGE_OID_TABLE.items():
                ifGaugeOid = '.'.join([self.IF_MIB_GAUGE_OID_TABLE[gaugeName],
                                       ifIndex])
                ifGaugeData = self.get(ifGaugeOid, host, port, community)
                ifGaugeValue = ifGaugeData[ifGaugeOid]
                if not ifGaugeValue:
                    continue

                # Get Metric Name and Value
                metricIfDescr = re.sub(r'\W', '_', ifName)
                metricName = '.'.join([metricIfDescr, gaugeName])
                metricValue = int(ifGaugeValue)
                # Get Metric Path
                metricPath = '.'.join(['devices',
                                       device,
                                       self.config['path'],
                                       metricName])
                # Publish Metric
                self.publish_gauge(metricPath, metricValue)

            # Get counters (64bit)
            counterItems = self.IF_MIB_COUNTER_OID_TABLE.items()
            for counterName, counterOid in counterItems:
                ifCounterOid = '.'.join(
                    [self.IF_MIB_COUNTER_OID_TABLE[counterName], ifIndex])
                ifCounterData = self.get(ifCounterOid, host, port, community)
                ifCounterValue = ifCounterData[ifCounterOid]
                if not ifCounterValue:
                    continue

                # Get Metric Name and Value
                metricIfDescr = re.sub(r'\W', '_', ifName)

                if counterName in ['ifHCInOctets', 'ifHCOutOctets']:
                    for unit in self.config['byte_unit']:
                        # Convert Metric
                        metricName = '.'.join([metricIfDescr,
                                               counterName.replace('Octets',
                                                                   unit)])
                        metricValue = diamond.convertor.binary.convert(
                            value=ifCounterValue,
                            oldUnit='byte',
                            newUnit=unit)

                        # Get Metric Path
                        metricPath = '.'.join(['devices',
                                               device,
                                               self.config['path'],
                                               metricName])
                        # Publish Metric
                        self.publish_counter(metricPath,
                                             metricValue,
                                             max_value=18446744073709600000,
                                             )
                else:
                    metricName = '.'.join([metricIfDescr, counterName])
                    metricValue = int(ifCounterValue)

                    # Get Metric Path
                    metricPath = '.'.join(['devices',
                                           device,
                                           self.config['path'],
                                           metricName])
                    # Publish Metric
                    self.publish_counter(metricPath,
                                         metricValue,
                                         max_value=18446744073709600000,
                                         )
