# coding=utf-8

"""
V. 1.0

JbossApiCollector is a collector that uses JBOSS 7 native API to collect data
Tested on jboss 7.X.X??

Much of the code was borrowed from:

http://bit.ly/XRrCWx
https://github.com/lukaf/munin-plugins/blob/master/jboss7_

References:
https://docs.jboss.org/author/display/AS7/Management+API+reference
http://middlewaremagic.com/jboss/?p=2476

TODO:
This code was made to work with the local system 'curl' command, due to
difficulties getting urllib2 or pycurl to work under the python 2.4 options
successfully doing SSL Digest Authentication.

Plan is to make this code work with newer versions of python and possibly
Requests. (http://docs.python-requests.org/en/latest/)

If possible, please make future updates backwards compatable to call the local
curl as an option.


#### Dependencies

 * java
 * jboss
 * curl
 * json

##### Configuration

# Uses local system curl until can be made to work with either urllib2, pycurl,
or requests (http://docs.python-requests.org/en/latest/)


enabled = True
path_suffix = ""
measure_collector_time = False
interface_regex = ^(.+?)\.
curl_bin = /usr/bin/curl
connect_timeout = 4
hosts = wasadmin:pass@host:9443:https, wasadmin:pass@host:9443:https
curl_options = "-s --digest -L "
ssl_options = "--sslv3 -k"
connector_stats = True | False
connector_options =  http, ajp
app_stats = True | False
jvm_memory_stats = True | False
jvm_buffer_pool_stats = True | False
jvm_memory_pool_stats = True | False
jvm_gc_stats = True | False
jvm_thread_stats = True | False


"""

import diamond.collector
import os
import re
import subprocess

try:
    import json
except ImportError:
    import simplejson as json


## Setup a set of VARs
# Set this for use in curl request
header = '"Content-Type: application/json"'

operational_type = [
    'app',
    'web',
    'jvm',
]


web_stats = [
    'errorCount',
    'requestCount',
    'bytesReceived',
    'bytesSent',
    'processingTime',
]

memory_types = [
    'init',
    'used',
    'committed',
    'max',
]

buffer_pool_types = [
    'count',
    'memory-used',
]

thread_types = [
    'thread-count',
    'daemon-thread-count'
]

memory_topics = [
    'heap-memory-usage',
    'non-heap-memory-usage',
]

gc_types = [
    'collection-count',
    'collection-time',
]


class JbossApiCollector(diamond.collector.Collector):

    def __init__(self, config, handlers):
        diamond.collector.Collector.__init__(self, config, handlers)

        if self.config['hosts'].__class__.__name__ != 'list':
            self.config['hosts'] = [self.config['hosts']]

        # get the params for each host
        if 'host' in self.config:
            hoststr = "%s:%s@%s:%s:%s" % (
                self.config['user'],
                self.config['password'],
                self.config['host'],
                self.config['port'],
                self.config['proto'],
            )
            self.config['hosts'].append(hoststr)

        self.db = None

        if type(self.config['connector_options']) is not list:
            self.config['connector_options'] = [
                self.config['connector_options']]

    def get_default_config_help(self):
        # Need to update this when done to help explain details when running
        # diamond-setup.
        config_help = super(JbossApiCollector, self).get_default_config_help()
        config_help.update({
            'curl_bin': 'Path to system curl executable',
            'hosts': 'List of hosts to collect from. Format is yourusername:yourpassword@host:port:proto',  # NOQA
            'app_stats': 'Collect application pool stats',
            'jvm_memory_pool_stats': 'Collect JVM memory-pool stats',
            'jvm_buffer_pool_stats': 'Collect JVM buffer-pool stats',
            'jvm_memory_stats': 'Collect JVM basic memory stats',
            'jvm_gc_stats': 'Collect JVM garbage-collector stats',
            'jvm_thread_stats': 'Collect JVM thread stas',
            'connector_stats': 'Collect HTTP and AJP Connector stats',
            'connector_options': 'Types of connectors to collect'
        })
        return config_help

    def get_default_config(self):

        # Initialize default config
        config = super(JbossApiCollector, self).get_default_config()
        config.update({
            'path': 'jboss',
            'method': 'Sequential',
            'curl_bin': '/usr/bin/curl',
            'connect_timeout': '4',
            'ssl_options': '--sslv3 -k',
            'curl_options': '-s --digest -L ',
            'interface_regex': '^(.+?)\.',  # matches up to first "."
            'hosts': [],
            'app_stats': 'True',
            'connector_options': ['http', 'ajp'],
            'jvm_memory_pool_stats': 'True',
            'jvm_buffer_pool_stats': 'True',
            'jvm_memory_stats': 'True',
            'jvm_gc_stats': 'True',
            'jvm_thread_stats': 'True',
            'connector_stats': 'True'
        })
        # Return default config
        return config

    def get_stats(self, current_host, current_port, current_proto, current_user,
                  current_pword):

        if not os.access(self.config['curl_bin'], os.X_OK):
            self.log.error("%s is not executable or does not exist.",
                           self.config['curl_bin'])

        # Check if there is a RegEx to perform on the interface names
        if self.config['interface_regex'] != '':
            interface = self.string_regex(self.config['interface_regex'],
                                          current_host)

        else:
            # Clean up any possible extra "."'s in the interface, keeps
            # graphite from creating directories
            interface = self.string_fix(current_host)

        for op_type in operational_type:
            output = self.get_data(op_type, current_host, current_port,
                                   current_proto, current_user, current_pword)
            if op_type == 'app' and self.config['app_stats'] == 'True':
                if output:
                # Grab the pool stats for each Instance
                    for instance in output['result']['data-source']:
                        datasource = output['result']['data-source'][instance]
                        for metric in datasource['statistics']['pool']:
                            metricName = '%s.%s.%s.statistics.pool.%s' % (
                                interface, op_type, instance, metric)
                            metricValue = datasource[
                                'statistics']['pool'][metric]
                            self.publish(metricName, float(metricValue))

            if op_type == 'web' and self.config['connector_stats'] == 'True':
                if output:
                    # Grab http and ajp info (make these options)
                    for c_type in self.config['connector_options']:
                    #for connector_type in self.config['connector_options']:
                        for metric in web_stats:
                            metricName = '%s.%s.connector.%s.%s' % (interface,
                                                                    op_type,
                                                                    c_type,
                                                                    metric)
                            connector = output['result']['connector']
                            metricValue = connector[c_type][metric]
                            self.publish(metricName, float(metricValue))

            if op_type == 'jvm':
                if output:
                    if self.config['jvm_memory_pool_stats'] == 'True':
                        # Grab JVM memory pool stats
                        mempool = output['result']['type']['memory-pool']
                        for pool_name in mempool['name']:
                            for metric in memory_types:
                                metricName = '%s.%s.%s.%s.%s.%s' % (interface,
                                                                    op_type,
                                                                    'memory-'
                                                                    + 'pool',
                                                                    pool_name,
                                                                    'usage',
                                                                    metric)
                                metricValue = mempool['name'][pool_name][
                                    'usage'][metric]
                                self.publish(metricName, float(metricValue))

                    # Grab JVM buffer-pool stats
                    if self.config['jvm_buffer_pool_stats'] == 'True':
                        bufferpool = output['result']['type']['buffer-pool']
                        for pool in bufferpool['name']:
                            for metric in buffer_pool_types:
                                metricName = '%s.%s.%s.%s.%s' % (interface,
                                                                 op_type,
                                                                 'buffer-pool',
                                                                 pool,
                                                                 metric)
                                metricValue = bufferpool['name'][pool][metric]
                                self.publish(metricName, float(metricValue))

                    # Grab basic memory stats
                    if self.config['jvm_memory_stats'] == 'True':
                        for mem_type in memory_topics:
                            for metric in memory_types:
                                metricName = '%s.%s.%s.%s.%s' % (interface,
                                                                 op_type,
                                                                 'memory',
                                                                 mem_type,
                                                                 metric)
                                memory = output['result']['type']['memory']
                                metricValue = memory[mem_type][metric]
                                self.publish(metricName, float(metricValue))

                    # Grab Garbage collection stats
                    if self.config['jvm_gc_stats'] == 'True':
                        garbage = output['result']['type']['garbage-collector']
                        for gc_name in garbage['name']:
                            for metric in gc_types:
                                metricName = '%s.%s.%s.%s.%s' % (interface,
                                                                 op_type,
                                                                 'garbage-'
                                                                 + 'collector',
                                                                 gc_name,
                                                                 metric)
                                metricValue = garbage['name'][gc_name][metric]
                                self.publish(metricName, float(metricValue))

                    # Grab threading stats
                    if self.config['jvm_thread_stats'] == 'True':
                        for metric in thread_types:
                            metricName = '%s.%s.%s.%s' % (interface, op_type,
                                                          'threading', metric)
                            threading = output['result']['type']['threading']
                            metricValue = threading[metric]
                            self.publish(metricName, float(metricValue))

        return True

    def get_data(self, op_type, current_host, current_port, current_proto,
                 current_user, current_pword):
        output = {}
        if op_type == 'app':
            data = ('{"operation":"read-resource", "include-runtime":"true", '
                    + '"recursive":"true" , "address":["subsystem",'
                    + '"datasources"]}')

        if op_type == 'web':
            data = ('{"operation":"read-resource", "include-runtime":"true", '
                    + '"recursive":"true" , "address":["subsystem","web"]}')

        if op_type == 'jvm':
            data = ('{"operation":"read-resource", "include-runtime":"true", '
                    + '"recursive":"true" , "address":["core-service",'
                    + '"platform-mbean"]}')

        the_cmd = (("%s --connect-timeout %s %s %s %s://%s:%s/management "
                   + "--header %s -d '%s' -u %s:%s") % (
            self.config['curl_bin'], self.config['connect_timeout'],
            self.config['ssl_options'], self.config['curl_options'],
            current_proto, current_host, current_port, header, data,
            current_user, current_pword))

        try:
            attributes = subprocess.Popen(the_cmd, shell=True,
                                          stdout=subprocess.PIPE
                                          ).communicate()[0]
            output = json.loads(attributes)
        except Exception, e:
            self.log.error("JbossApiCollector: There was an exception %s", e)
            output = ''
        return output

    def string_fix(self, s):
        return re.sub(r"[^a-zA-Z0-9_]", "_", s)

    def string_regex(self, pattern, s):
        tmp_result = re.match(pattern, s)
        return tmp_result.group(1)

    def collect(self):

        for host in self.config['hosts']:
            matches = re.search(
                '^([^:]*):([^@]*)@([^:]*):([^:]*):?(.*)', host)

            if not matches:
                continue

            current_host = matches.group(3)
            current_port = int(matches.group(4))
            current_proto = matches.group(5)
            current_user = matches.group(1)
            current_pword = matches.group(2)

            # Call get_stats for each instance of jboss
            self.get_stats(current_host, current_port, current_proto,
                           current_user, current_pword)

        return True
