# coding=utf-8

"""
Collect stats from postfix-stats. postfix-stats is a simple threaded stats
aggregator for Postfix. When running as a syslog destination, it can be used to
get realtime cumulative stats.

#### Dependencies

 * socket
 * json (or simeplejson)
 * [postfix-stats](https://github.com/disqus/postfix-stats)

"""

import socket
import sys

try:
    import json
except ImportError:
    import simplejson as json

import diamond.collector

from diamond.collector import str_to_bool

if sys.version_info < (2, 6):
    from string import maketrans
    DOTS_TO_UNDERS = maketrans('.', '_')
else:
    DOTS_TO_UNDERS = {ord(u'.'): u'_'}


class PostfixCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(PostfixCollector,
                            self).get_default_config_help()
        config_help.update({
            'host':             'Hostname to coonect to',
            'port':             'Port to connect to',
            'include_clients':  'Include client connection stats',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(PostfixCollector, self).get_default_config()
        config.update({
            'path':             'postfix',
            'host':             'localhost',
            'port':             7777,
            'include_clients':  True,
        })
        return config

    def get_json(self):
        json_string = ''

        address = (self.config['host'], int(self.config['port']))

        s = None
        try:
            try:
                s = socket.create_connection(address, timeout=1)

                s.sendall('stats\n')

                while 1:
                    data = s.recv(4096)
                    if not data:
                        break
                    json_string += data
            except socket.error:
                self.log.exception("Error talking to postfix-stats")
                return '{}'
        finally:
            if s:
                s.close()

        return json_string or '{}'

    def get_data(self):
        json_string = self.get_json()

        try:
            data = json.loads(json_string)
        except (ValueError, TypeError):
            self.log.exception("Error parsing json from postfix-stats")
            return None

        return data

    def collect(self):
        data = self.get_data()

        if not data:
            return

        if str_to_bool(self.config['include_clients']) and u'clients' in data:
            for client, value in data['clients'].iteritems():
                # translate dots to underscores in client names
                metric = u'.'.join(['clients',
                                    client.translate(DOTS_TO_UNDERS)])

                dvalue = self.derivative(metric, value)

                self.publish(metric, dvalue)

        for action in (u'in', u'recv', u'send'):
            if action not in data:
                continue

            for sect, stats in data[action].iteritems():
                for status, value in stats.iteritems():
                    metric = '.'.join([action,
                                       sect,
                                       status.translate(DOTS_TO_UNDERS)])

                    dvalue = self.derivative(metric, value)

                    self.publish(metric, dvalue)

        if u'local' in data:
            for key, value in data[u'local'].iteritems():
                metric = '.'.join(['local', key])

                dvalue = self.derivative(metric, value)

                self.publish(metric, dvalue)
