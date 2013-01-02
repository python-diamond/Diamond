# coding=utf-8

"""
SNMPCollector for Netscaler Metrics

NetScaler is a network appliance manufactured by Citrix providing level 4 load
balancing, firewall, proxy and VPN functions.

"""

import sys
import os
import time
import struct
import re

# Fix Path for locating the SNMPCollector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../',
                                             'snmp',
                                             )))

from diamond.metric import Metric
from snmp import SNMPCollector as parent_SNMPCollector


class NetscalerSNMPCollector(parent_SNMPCollector):
    """
    SNMPCollector for Netscaler Metrics
    """

    """
    EntityProtocolType ::=
    INTEGER{    http(0),
                ftp(1),
                tcp(2),
                udp(3),
                sslBridge(4),
                monitor(5),
                monitorUdp(6),
                nntp(7),
                httpserver(8),
                httpclient(9),
                rpcserver(10),
                rpcclient(11),
                nat(12),
                any(13),
                ssl(14),
                dns(15),
                adns(16),
                snmp(17),
                ha(18),
                monitorPing(19),
                sslOtherTcp(20),
                aaa(21),
                secureMonitor(23),
                sslvpnUdp(24),
                rip(25),
                dnsClient(26),
                rpcServer(27),
                rpcClient(28),
                dhcrpa(36),
                sipudp(39),
                dnstcp(44),
                adnstcp(45),
                rtsp(46),
                push(48),
                sslPush(49),
                dhcpClient(50),
                radius(51),
                serviceUnknown(62) }

    EntityState ::=
    INTEGER{    down(1),
                unknown(2),
                busy(3),
                outOfService(4),
                transitionToOutOfService(5),
                up(7),
                transitionToOutOfServiceDown(8) }
    """

    NETSCALER_SYSTEM_GUAGES = {
        "cpuUsage": "1.3.6.1.4.1.5951.4.1.1.41.1.0",
        "memUsage": "1.3.6.1.4.1.5951.4.1.1.41.2.0",
        "surgeQueue": "1.3.6.1.4.1.5951.4.1.1.46.15.0",
        "establishedServerConnections": "1.3.6.1.4.1.5951.4.1.1.46.10.0",
        "establishedClientConnections": "1.3.6.1.4.1.5951.4.1.1.46.12.0"
    }

    NETSCALER_SYSTEM_COUNTERS = {
        "httpTotRequests": "1.3.6.1.4.1.5951.4.1.1.48.67.0"
    }

    NETSCALER_VSERVER_NAMES = "1.3.6.1.4.1.5951.4.1.3.1.1.1"

    NETSCALER_VSERVER_TYPE = "1.3.6.1.4.1.5951.4.1.3.1.1.4"

    NETSCALER_VSERVER_STATE = "1.3.6.1.4.1.5951.4.1.3.1.1.5"

    NETSCALER_VSERVER_GUAGES = {
        "vsvrRequestRate": "1.3.6.1.4.1.5951.4.1.3.1.1.43",
        "vsvrRxBytesRate": "1.3.6.1.4.1.5951.4.1.3.1.1.44",
        "vsvrTxBytesRate": "1.3.6.1.4.1.5951.4.1.3.1.1.45",
        "vsvrCurServicesUp": "1.3.6.1.4.1.5951.4.1.3.1.1.41",
        "vsvrCurServicesDown": "1.3.6.1.4.1.5951.4.1.3.1.1.37",
        "vsvrCurServicesUnknown": "1.3.6.1.4.1.5951.4.1.3.1.1.38",
        "vsvrCurServicesTransToOutOfSvc": "1.3.6.1.4.1.5951.4.1.3.1.1.40"
    }

    NETSCALER_SERVICE_NAMES = "1.3.6.1.4.1.5951.4.1.2.1.1.1"

    NETSCALER_SERVICE_TYPE = "1.3.6.1.4.1.5951.4.1.2.1.1.4"

    NETSCALER_SERVICE_STATE = "1.3.6.1.4.1.5951.4.1.2.1.1.5"

    NETSCALER_SERVICE_GUAGES = {
        "svcRequestRate": "1.3.6.1.4.1.5951.4.1.2.1.1.42",
        "svcSurgeCount": "1.3.6.1.4.1.5951.4.1.2.1.1.10",
        "svcEstablishedConn": "1.3.6.1.4.1.5951.4.1.2.1.1.8",
        "svcActiveConn": "1.3.6.1.4.1.5951.4.1.2.1.1.9",
        "svcCurClntConnections": "1.3.6.1.4.1.5951.4.1.2.1.1.41"
    }

    MAX_VALUE = 18446744073709551615

    def get_default_config_help(self):
        config_help = super(NetscalerSNMPCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': 'netscaler dns address',
            'port': 'Netscaler port to collect snmp data',
            'community': 'SNMP community',
            'exclude_service_type': "list of service types to exclude"
            + " (see MIB EntityProtocolType)",
            'exclude_vserver_type': "list of vserver types to exclude"
            + " (see MIB EntityProtocolType)"
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(NetscalerSNMPCollector, self).get_default_config()
        config.update({
            'path':     'netscaler',
            'timeout':  15,
            'exclude_service_type': [],
            'exclude_vserver_type': [],
            'exclude_service_state': [],
            'exclude_vserver_state': []
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
        Collect Netscaler SNMP stats from device
        """
        # Log
        self.log.info("Collecting Netscaler statistics from: %s", device)

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
            metricValue = self.derivative(metricPath, long(
                self.get(v, host, port, community)[v]), self.MAX_VALUE)
            # Create Metric
            metric = Metric(metricPath, metricValue, timestamp, 0)
            # Publish Metric
            self.publish_metric(metric)

        # Collect Netscaler Services
        serviceNames = [v.strip("\'") for v in self.walk(
            self.NETSCALER_SERVICE_NAMES, host, port, community).values()]

        for serviceName in serviceNames:
            # Get Service Name in OID form
            serviceNameOid = self.get_string_index_oid(serviceName)

            # Get Service Type
            serviceTypeOid = ".".join([self.NETSCALER_SERVICE_TYPE,
                                       self._convert_from_oid(serviceNameOid)])
            serviceType = int(self.get(serviceTypeOid,
                                       host,
                                       port,
                                       community)[serviceTypeOid].strip("\'"))

            # Filter excluded service types
            if serviceType in map(lambda v: int(v),
                                  self.config.get('exclude_service_type')):
                continue

            # Get Service State
            serviceStateOid = ".".join([self.NETSCALER_SERVICE_STATE,
                                        self._convert_from_oid(serviceNameOid)])
            serviceState = int(self.get(serviceStateOid,
                                        host,
                                        port,
                                        community)[serviceStateOid].strip("\'"))

            # Filter excluded service states
            if serviceState in map(lambda v: int(v),
                                   self.config.get('exclude_service_state')):
                continue

            for k, v in self.NETSCALER_SERVICE_GUAGES.items():
                serviceGuageOid = ".".join(
                    [v, self._convert_from_oid(serviceNameOid)])
                # Get Metric Name
                metricName = '.'.join([re.sub(r'\.|\\', '_', serviceName), k])
                # Get Metric Value
                metricValue = int(self.get(serviceGuageOid,
                                           host,
                                           port,
                                           community
                                           )[serviceGuageOid].strip("\'"))
                # Get Metric Path
                metricPath = '.'.join(['devices',
                                       device,
                                       'service',
                                       metricName])
                # Create Metric
                metric = Metric(metricPath, metricValue, timestamp, 0)
                # Publish Metric
                self.publish_metric(metric)

        # Collect Netscaler Vservers
        vserverNames = [v.strip("\'") for v in self.walk(
            self.NETSCALER_VSERVER_NAMES, host, port, community).values()]

        for vserverName in vserverNames:
            # Get Vserver Name in OID form
            vserverNameOid = self.get_string_index_oid(vserverName)

            # Get Vserver Type
            vserverTypeOid = ".".join([self.NETSCALER_VSERVER_TYPE,
                                       self._convert_from_oid(vserverNameOid)])
            vserverType = int(self.get(vserverTypeOid,
                                       host,
                                       port,
                                       community)[vserverTypeOid].strip("\'"))

            # filter excluded vserver types
            if vserverType in map(lambda v: int(v),
                                  self.config.get('exclude_vserver_type')):
                continue

            # Get Service State
            vserverStateOid = ".".join([self.NETSCALER_VSERVER_STATE,
                                        self._convert_from_oid(vserverNameOid)])
            vserverState = int(self.get(vserverStateOid,
                                        host,
                                        port,
                                        community)[vserverStateOid].strip("\'"))

            # Filter excluded vserver state
            if vserverState in map(lambda v: int(v),
                                   self.config.get('exclude_vserver_state')):
                continue

            for k, v in self.NETSCALER_VSERVER_GUAGES.items():
                vserverGuageOid = ".".join(
                    [v, self._convert_from_oid(vserverNameOid)])
                # Get Metric Name
                metricName = '.'.join([re.sub(r'\.|\\', '_', vserverName), k])
                # Get Metric Value
                metricValue = int(self.get(vserverGuageOid,
                                           host,
                                           port,
                                           community
                                           )[vserverGuageOid].strip("\'"))
                # Get Metric Path
                metricPath = '.'.join(['devices',
                                       device,
                                       'vserver',
                                       metricName])
                # Create Metric
                metric = Metric(metricPath, metricValue, timestamp, 0)
                # Publish Metric
                self.publish_metric(metric)
