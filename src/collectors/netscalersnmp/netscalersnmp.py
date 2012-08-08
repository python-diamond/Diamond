"""
SNMPCollector for Netscaler Metrics

NetScaler is a network appliance manufactured by Citrix providing level 4 load
balancing, firewall, proxy and VPN functions.

"""

import sys
import os
import time
import logging
import struct
import re

# Fix Path    
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../")))

from diamond.metric import Metric
from snmp import SNMPCollector

class NetscalerSNMPCollector(SNMPCollector):
    """
    SNMPCollector for Netscaler Metrics
    """

    NETSCALER_SYSTEM_GUAGES = {
        "cpuUsage" : "1.3.6.1.4.1.5951.4.1.1.41.1.0",
        "memUsage" : "1.3.6.1.4.1.5951.4.1.1.41.2.0",
        "surgeQueue" : "1.3.6.1.4.1.5951.4.1.1.46.15.0",
        "establishedServerConnections" : "1.3.6.1.4.1.5951.4.1.1.46.10.0",
        "establishedClientConnections" : "1.3.6.1.4.1.5951.4.1.1.46.12.0"
    }

    NETSCALER_SYSTEM_COUNTERS = {
        "httpTotRequests" : "1.3.6.1.4.1.5951.4.1.1.48.67.0"
    }

    NETSCALER_SERVICE_NAMES = "1.3.6.1.4.1.5951.4.1.2.1.1.1" 

    NETSCALER_SERVICE_TYPE = "1.3.6.1.4.1.5951.4.1.2.1.1.4"   

    NETSCALER_SERVICE_STATE = "1.3.6.1.4.1.5951.4.1.2.1.1.5"
 
    NETSCALER_SERVICE_GUAGES = {
        "svcRequestRate" : "1.3.6.1.4.1.5951.4.1.2.1.1.42",
        "svcSurgeCount" : "1.3.6.1.4.1.5951.4.1.2.1.1.10",
        "svcEstablishedConn" : "1.3.6.1.4.1.5951.4.1.2.1.1.8",
        "svcActiveConn" : "1.3.6.1.4.1.5951.4.1.2.1.1.9",
        "svcCurClntConnections" : "1.3.6.1.4.1.5951.4.1.2.1.1.41"
    }

    MAX_VALUE = 18446744073709551615

    def get_default_config_help(self):
        config_help = super(NetscalerSNMPCollector, self).get_default_config_help()
        config_help.update({
            'host' : 'netscaler dns address',
            'port' : 'Netscaler port to collect snmp data',
            'community' : 'SNMP community'
        })  
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(NetscalerSNMPCollector, self).get_default_config()
        config.update( {
            'path':     'netscaler',
            'timeout' : 15,
        } ) 
        return config

    def get_string_index_oid(self, s):
        "Turns a string into an oid format is length of name followed by name chars in ascii"
        return ( len(self.get_bytes(s)) , ) + self.get_bytes(s)

    def get_bytes(self, s):
        "Turns a string into a list of byte values"
        return struct.unpack('%sB' % len(s), s)

    def collect_snmp(self, device, host, port, community):
        """
        Collect Netscaler SNMP stats from device
        """ 
        # Log
        self.log.info("Collecting Netscaler statistics from: %s" % (device))

        # Set timestamp
        timestamp = time.time()

        # Collect Netscaler System OIDs
        for k, v in self.NETSCALER_SYSTEM_GUAGES.items():
            # Get Metric Name and Value
            metricName = '.'.join([k])
            metricValue = int(self.get(v, host, port, community)[v])
            # Get Metric Path
            metricPath = '.'.join(['devices', device, 'system', metricName])
            # Create Metric
            metric = Metric(metricPath, metricValue, timestamp, 0)
            # Publish Metric
            self.publish_metric(metric)
        
        # Collect Netscaler System Counter OIDs
        for k, v in self.NETSCALER_SYSTEM_COUNTERS.items():
            # Get Metric Name and Value
            metricName = '.'.join([k])
            # Get Metric Path
            metricPath = '.'.join(['devices', device, 'system', metricName])
            # Get Metric Value
            metricValue = self.derivative(metricPath, long(self.get(v, host, port, community)[v]), self.MAX_VALUE)
            # Create Metric
            metric = Metric(metricPath, metricValue, timestamp, 0)
            # Publish Metric
            self.publish_metric(metric)

        # Collect Netscaler Services
        serviceNames = [v.strip("\'") for v in self.walk(self.NETSCALER_SERVICE_NAMES, host, port, community).values()]

        for serviceName in serviceNames:
            # Get Service Name in OID form
            serviceNameOid = self.get_string_index_oid(serviceName) 

            # Get Service Type 
            serviceTypeOid = ".".join([self.NETSCALER_SERVICE_TYPE, self._convert_from_oid(serviceNameOid)])
            serviceType = int(self.get(serviceTypeOid, host, port, community)[serviceTypeOid].strip("\'"))

            # Filter internal services
            if serviceType in [20, 30]:
                continue

            # Get Service State
            serviceStateOid = ".".join([self.NETSCALER_SERVICE_STATE, self._convert_from_oid(serviceNameOid)])
            serviceState = int(self.get(serviceStateOid, host, port, community)[serviceStateOid].strip("\'"))

            # Filter down services
            if serviceState not in [7]:
                continue

            for k,v in self.NETSCALER_SERVICE_GUAGES.items():
                serviceGuageOid = ".".join([v, self._convert_from_oid(serviceNameOid)]) 
                # Get Metric Name
                metricName = '.'.join([re.sub(r'\.|\\', '_', serviceName), k])
                # Get Metric Value
                metricValue = int(self.get(serviceGuageOid, host, port, community)[serviceGuageOid].strip("\'"))
                # Get Metric Path
                metricPath = '.'.join(['devices', device, 'service', metricName])
                # Create Metric
                metric = Metric(metricPath, metricValue, timestamp, 0)
                # Publish Metric
                self.publish_metric(metric)

