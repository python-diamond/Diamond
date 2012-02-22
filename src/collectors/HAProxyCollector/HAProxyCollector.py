
import re
import sys
import urllib2
import base64
import csv
import logging
from urlparse import urlparse

import diamond.collector

class HAProxyCollector(diamond.collector.Collector):
    """
    Collect HAProxy Stats
    """

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'enabled':  'False',
            'path':     'haproxy',
            'url':      'http://localhost/haproxy?stats;csv',
            'user':     'admin',
            'pass':     'password',
        }

    def get_csv_data(self):
        """
        Request stats from HAProxy Server
        """
        metrics = []
        req  = urllib2.Request(self.config['url'])
        try:
            handle = urllib2.urlopen(req)
            return handle.readlines()
        except Exception, e:
            if not hasattr(e, 'code') or e.code != 401:
                self.log.error("Error retrieving HAProxy stats. %s", e)
                return metrics

        # get the www-authenticate line from the headers
        # which has the authentication scheme and realm in it
        authline = e.headers['www-authenticate']

        # this regular expression is used to extract scheme and realm
        authobj = re.compile(r'''(?:\s*www-authenticate\s*:)?\s*(\w*)\s+realm=['"]([^'"]+)['"]''',re.IGNORECASE)
        matchobj = authobj.match(authline)
        if not matchobj:
            # if the authline isn't matched by the regular expression
            # then something is wrong
            self.log.error('The authentication header is malformed.')
            return metrics

        scheme = matchobj.group(1)
        realm  = matchobj.group(2)
        # here we've extracted the scheme
        # and the realm from the header
        if scheme.lower() != 'basic':
            self.log.error('Invalid authentication scheme.')
            return metrics

        base64string = base64.encodestring('%s:%s' % (self.config['user'], self.config['pass']))[:-1]
        authheader = 'Basic %s' % base64string
        req.add_header("Authorization", authheader)
        try:
            handle    = urllib2.urlopen(req)
            metrics   = handle.readlines()
            print metrics
            return metrics
        except IOError, e:
            # here we shouldn't fail if the USER/PASS is right
            self.log.error("Error retrieving HAProxy stats. (Invalid username or password?) %s", e)
            return metrics

    def collect(self):
        """
        Collect HAProxy Stats
        """
        csv_data = self.get_csv_data()
        data = csv.reader(csv_data)
        rownum = 0

        for row in data:
            if rownum == 0:
                pass
            else:
                metric_name =  '%s.%s' % (row[0].lower(), row[1].lower())
                #create dictionary
                haproxy_stats = {
                    'qcur': row[2],
                    'qmax': row[3],
                    'scur': row[4],
                    'smax': row[5],
                    'slim': row[6],
                    'stot': row[7],
                    'bin':  row[8],
                    'bout': row[9],
                    'dreq': row[10],
                    'dresp': row[11],
                    'ereq': row[12],
                    'econ': row[13],
                    'eresp': row[14],
                    'wretr': row[15],
                    'wredis': row[16],
                    'weight': row[18],
                    'act': row[19],
                    'bck': row[20],
                    'lastchg': row[21],
                    'downtime': row[22],
                    'qlimit': row[23],
                    'iid': row[25],
                    'sid': row[26],
                    'throttle': row[27],
                    'lbtot': row[28],
                    'tracked': row[29],
                    'type': row[30],
                    'rate': row[31],
                    'rate_lim': row[32],
                    'rate_max': row[33]
                }
                for metric in haproxy_stats.keys():
                    stat_name =  '%s.%s' % (metric_name,metric.lower())
                    if haproxy_stats[metric] == '':
                        haproxy_stats[metric] = 0
                    self.log.debug('Publishing Metric: %s Value[%s]' % (stat_name,haproxy_stats[metric]))
                    self.publish(stat_name, long(haproxy_stats[metric]))
            #increment the row number and move on to the next set of stats
            rownum += 1

