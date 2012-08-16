# coding=utf-8

"""
SNMPCollector is a special collector for collecting data from using SNMP

#### Dependencies

 * pysnmp

"""

import socket

try:
    import pysnmp.entity.rfc3413.oneliner.cmdgen
    import pysnmp.debug
except ImportError:
    pysnmp = None

import diamond.collector

class SNMPCollector(diamond.collector.Collector):

    def __init__(self, config, handlers):
        """
        Create a new instance of the SNMPCollector class
        """
        # Initialize base Class
        diamond.collector.Collector.__init__(self, config, handlers)

        # Initialize SNMP Command Generator
        if pysnmp is not None:
            self.snmpCmdGen = pysnmp.entity.rfc3413.oneliner.cmdgen.CommandGenerator()

    def get_default_config_help(self):
        config_help = super(SNMPCollector, self).get_default_config_help()
        config_help.update({
            'timeout' : 'Number of seconds before timing out the snmp connection',
            'retries' : 'Number of times to retry before bailing',
        })
        return config_help

    def get_default_config(self):
        # Initialize default config
        default_config = super(SNMPCollector, self).get_default_config()
        default_config['path_suffix'] = None
        default_config['path_prefix'] = 'systems'
        default_config['timeout'] = 5
        default_config['retries'] = 3
        # Return default config
        return default_config

    def get_schedule(self):
        """
        Override SNMPCollector.get_schedule
        """
        schedule = {}
        if 'devices' in self.config:
            for device in self.config['devices']:
                # Get Device Config
                c = self.config['devices'][device]
                # Get Task Name
                task = "_".join([self.__class__.__name__, device])
                # Check if task is already in schedule
                if task in schedule:
                    raise KeyError, "Duplicate device scheduled"
                schedule[task] = (self.collect_snmp, (device, c['host'], int(c['port']), c['community']), int(self.config['splay']), int(self.config['interval']))
        return schedule

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
        snmpAuthData = pysnmp.entity.rfc3413.oneliner.cmdgen.CommunityData('agent', community)

        # Assemble SNMP Transport Data
        snmpTransportData = pysnmp.entity.rfc3413.oneliner.cmdgen.UdpTransportTarget((host, port), int(self.config['timeout']), int(self.config['retries']))

        # Assemble SNMP Next Command
        errorIndication, errorStatus, errorIndex, varBind = self.snmpCmdGen.getCmd(snmpAuthData, snmpTransportData, oid )

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
        snmpAuthData = pysnmp.entity.rfc3413.oneliner.cmdgen.CommunityData('agent', community)

        # Assemble SNMP Transport Data
        snmpTransportData = pysnmp.entity.rfc3413.oneliner.cmdgen.UdpTransportTarget((host, port), int(self.config['timeout']), int(self.config['retries']))

        # Assemble SNMP Next Command
        errorIndication, errorStatus, errorIndex, varBindTable = self.snmpCmdGen.nextCmd(snmpAuthData, snmpTransportData, oid )

        # TODO: Error Check

        for varBindTableRow in varBindTable:
            for o, v in varBindTableRow:
                ret[o.prettyPrint()] = v.prettyPrint()

        return ret
