# coding=utf-8

"""
Collect the monit stats and report on cpu/memory for monitored processes

#### Dependencies

 * monit serving up /_status

"""

import urllib2
import base64

from xml.dom.minidom import parseString

import diamond.collector
from diamond.collector import str_to_bool


class MonitCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(MonitCollector, self).get_default_config_help()
        config_help.update({
            'send_totals': 'Send cpu and memory totals',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MonitCollector, self).get_default_config()
        config.update({
            'host':         '127.0.0.1',
            'port':         2812,
            'user':         'monit',
            'passwd':       'monit',
            'path':         'monit',
            'byte_unit':    ['byte'],
            'send_totals':  False,
        })
        return config

    def collect(self):
        url = 'http://%s:%i/_status?format=xml' % (self.config['host'],
                                                   int(self.config['port']))
        try:
            request = urllib2.Request(url)

            #
            # shouldn't need to check this
            base64string = base64.encodestring('%s:%s' % (
                self.config['user'], self.config['passwd'])).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, err:
            self.log.error("%s: %s", err, url)
            return

        metrics = {}

        try:
            dom = parseString("".join(response.readlines()))
        except:
            self.log.error("Got an empty response from the monit server")
            return

        for svc in dom.getElementsByTagName('service'):
            if int(svc.getAttribute('type')) == 3:
                name = svc.getElementsByTagName('name')[0].firstChild.data
                status = svc.getElementsByTagName('status')[0].firstChild.data
                monitor = svc.getElementsByTagName(
                    'monitor')[0].firstChild.data
                if status == '0' and monitor == '1':
                    try:
                        uptime = svc.getElementsByTagName(
                            'uptime')[0].firstChild.data
                        metrics["%s.uptime" % name] = uptime

                        cpu = svc.getElementsByTagName(
                            'cpu')[0].getElementsByTagName(
                            'percent')[0].firstChild.data
                        metrics["%s.cpu.percent" % name] = cpu
                        if str_to_bool(self.config['send_totals']):
                            cpu_total = svc.getElementsByTagName(
                                'cpu')[0].getElementsByTagName(
                                'percenttotal')[0].firstChild.data
                            metrics["%s.cpu.percent_total" % name] = cpu_total

                        mem = int(svc.getElementsByTagName(
                            'memory')[0].getElementsByTagName(
                            'kilobyte')[0].firstChild.data)
                        for unit in self.config['byte_unit']:
                            metrics["%s.memory.%s_usage" % (name, unit)] = (
                                diamond.convertor.binary.convert(
                                    value=mem,
                                    oldUnit='kilobyte',
                                    newUnit=unit))
                        metrics["%s.uptime" % name] = uptime
                        if str_to_bool(self.config['send_totals']):
                            mem_total = int(svc.getElementsByTagName(
                                'memory')[0].getElementsByTagName(
                                'kilobytetotal')[0].firstChild.data)
                            for unit in self.config['byte_unit']:
                                metrics["%s.memory_total.%s_usage" % (
                                    name, unit)] = (
                                    diamond.convertor.binary.convert(
                                        value=mem_total,
                                        oldUnit='kilobyte',
                                        newUnit=unit))

                    except:
                        pass

        for key in metrics:
            self.publish(key, metrics[key])
