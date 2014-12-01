# coding=utf-8

"""
SNMPCollector is a special collector for collecting data from using SNMP

#### Dependencies

 * pysnmp

"""

import socket

import warnings

# pysnmp packages on debian 6.0 use sha and md5 which are deprecated
# packages. there is nothing to be done about it until pysnmp
# updates to use new hashlib module -- ignoring warning for now
old_showwarning = warnings.showwarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

cmdgen = None

try:
    import pysnmp.entity.rfc3413.oneliner.cmdgen as cmdgen
    import pysnmp.debug
except ImportError:
    pysnmp = None
    cmdgen = None

warnings.showwarning = old_showwarning

import diamond.collector


class SNMPCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(SNMPCollector, self).get_default_config_help()
        config_help.update({
            'timeout': 'Seconds before timing out the snmp connection',
            'retries': 'Number of times to retry before bailing',
        })
        return config_help

    def get_default_config(self):
        # Initialize default config
        default_config = super(SNMPCollector, self).get_default_config()
        default_config['path_suffix'] = ''
        default_config['path_prefix'] = 'systems'
        default_config['timeout'] = 5
        default_config['retries'] = 3
        # Return default config
        return default_config

    def _convert_to_oid(self, s):
        d = s.split(".")
        return tuple([int(x) for x in d])

    def _convert_from_oid(self, oid):
        return ".".join([str(x) for x in oid])

    def get(self, oid, host, port, community):
        """
        Perform SNMP get for a given OID
        """
        # Initialize return value
        ret = {}

        # Convert OID to tuple if necessary
        if not isinstance(oid, tuple):
            oid = self._convert_to_oid(oid)

        # Convert Host to IP if necessary
        host = socket.gethostbyname(host)

        # Assemble SNMP Auth Data
        snmpAuthData = cmdgen.CommunityData('agent', community)

        # Assemble SNMP Transport Data
        snmpTransportData = cmdgen.UdpTransportTarget(
            (host, port),
            int(self.config['timeout']),
            int(self.config['retries']))

        # Assemble SNMP Next Command
        result = self.snmpCmdGen.getCmd(snmpAuthData, snmpTransportData, oid)
        varBind = result[3]

        # TODO: Error check

        for o, v in varBind:
            ret[o.prettyPrint()] = v.prettyPrint()

        return ret

    def walk(self, oid, host, port, community):
        """
        Perform an SNMP walk on a given OID
        """
        # Initialize return value
        ret = {}

        # Convert OID to tuple if necessary
        if not isinstance(oid, tuple):
            oid = self._convert_to_oid(oid)

        # Convert Host to IP if necessary
        host = socket.gethostbyname(host)

        # Assemble SNMP Auth Data
        snmpAuthData = cmdgen.CommunityData('agent', community)

        # Assemble SNMP Transport Data
        snmpTransportData = cmdgen.UdpTransportTarget(
            (host, port),
            int(self.config['timeout']),
            int(self.config['retries']))

        # Assemble SNMP Next Command
        resultTable = self.snmpCmdGen.nextCmd(snmpAuthData,
                                              snmpTransportData,
                                              oid)
        varBindTable = resultTable[3]

        # TODO: Error Check

        for varBindTableRow in varBindTable:
            for o, v in varBindTableRow:
                ret[o.prettyPrint()] = v.prettyPrint()

        return ret
