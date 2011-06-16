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

from diamond.metric import Metric

class Collector(object):
    """
    The Collector class is a base class for all metric collectors.
    """

    def __init__(self, config, handlers):
        """
        Create a new instance of the Collector class
        """
        # Initialize Logger
        self.log = logging.getLogger('diamond')
        # Initialize Members
        self.name = self.__class__.__name__
        self.handlers = handlers 
        self.last_values = {}
        
        # Get Collector class
        cls = self.__class__

        # Initialize config
        self.config = configobj.ConfigObj()
        # Merge default Collector config
        self.config.merge(config['collectors']['default'])
        # Check if default config is defined
        if self.get_default_config() is not None:
            # Merge default config
            self.config.merge(self.get_default_config())
        # Check if Collector config section exists 
        if cls.__name__ in config['collectors']:
            # Merge Collector config section
            self.config.merge(config['collectors'][cls.__name__])

        # Check for config file in config directory 
        configfile = os.path.join(config['server']['collectors_config_path'], cls.__name__) + '.cfg'            
        if os.path.exists(configfile):
            # Merge Collector config file
            self.config.merge(configobj.ConfigObj(configfile))
 
    def get_default_config(self):
        """
        Return the default config for the collector
        """
        return {}

    def get_schedule(self):
        """
        Return schedule for the collector
        """
        # Return a dict of tuples containing (collector function, collector function args, splay, interval) 
        return {self.__class__.__name__: (self._run, None, int(self.config['splay']), int(self.config['interval']))}

    def get_metric_path(self, name):
        """
        Get metric path  
        """ 
        if 'path_prefix' in self.config:
            prefix = self.config['path_prefix']
        else:
            prefix = 'systems'
        if 'hostname' in self.config:
            hostname = self.config['hostname']
        else:
            hostname = os.uname()[1].split('.')[0]
        if 'path' in self.config:
            path = self.config['path']
        else:
            path = self.__class__.__name__
        return '.'.join([prefix, hostname, path, name])

    def collect(self):
        """
        Default collector method
        """
        pass 
 
    def publish(self, name, value, precision=0):
        """
        Publish a metric with the given name
        """
        # Get metric Path
        path = self.get_metric_path(name) 
        
        # Create Metric
        metric = Metric(path, value, None, precision)
        
        # Publish Metric
        self.publish_metric(metric)

    def publish_metric(self, metric): 
        """
        Publish a Metric object
        """
        # Process Metric
        for h in self.handlers:
            h.process(metric)

    def derivative(self, name, new, max_value=0):
        """
        Calculate the derivative of the metric.
        """ 
        # Format Metric Path
        path = self.get_metric_path(name)

        if path in self.last_values:
            old = self.last_values[path]
            # Check for rollover
            if new < old:
                old = old + max_value
            # Get Change in X (value)
            dy = new - old
            # Get Change in Y (time)
            dx = int(self.config['interval'])
            result =  float(dy) / float(dx)
        else:
            result = 0

        # Store Old Value 
        self.last_values[path] = new
        
        # Return result
        return result

    def _run(self):
        """
        Run the collector
        """
        # Log
        self.log.debug("Collecting data from: %s" % (self.__class__.__name__))
        try:
            # Collect Data 
            self.collect()  
        except Exception, e:
            # Log Error 
            self.log.error(traceback.format_exc())
    
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

