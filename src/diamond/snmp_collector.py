# Copyright (C) 2011-2012 by Ivan Pouzyrevsky.
# Copyright (C) 2010-2011 by Brightcove Inc. 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sys
import string
import logging
import time
import traceback
import configobj
import socket
import re 

import pysnmp.entity.rfc3413.oneliner.cmdgen 
import pysnmp.debug

from metric import Metric

class SNMPCollector(Collector):
    """
    SNMPCollector is a special collector for collecting data from using SNMP
    """
   
    def __init__(self, config, handlers):
        """
        Create a new instance of the SNMPCollector class
        """
        # Initialize base Class
        Collector.__init__(self, config, handlers)

        # Initialize SNMP Command Generator
        self.snmpCmdGen = pysnmp.entity.rfc3413.oneliner.cmdgen.CommandGenerator()

    def get_default_config(self):
        # Initialize default config
        default_config = {}
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
        snmpTransportData = pysnmp.entity.rfc3413.oneliner.cmdgen.UdpTransportTarget((host, port), self.config['timeout'], self.config['retries'])

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
        snmpTransportData = pysnmp.entity.rfc3413.oneliner.cmdgen.UdpTransportTarget((host, port), self.config['timeout'], self.config['retries'])

        # Assemble SNMP Next Command
        errorIndication, errorStatus, errorIndex, varBindTable = self.snmpCmdGen.nextCmd(snmpAuthData, snmpTransportData, oid )

        # TODO: Error Check

        for varBindTableRow in varBindTable:
            for o, v in varBindTableRow:
                ret[o.prettyPrint()] = v.prettyPrint()                

        return ret
