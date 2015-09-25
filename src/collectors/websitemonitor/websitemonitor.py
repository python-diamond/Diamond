# coding=utf-8
"""
Gather HTTP Response code and Duration of HTTP request

#### Dependencies
  * urllib2

"""

import urllib2
import time
from datetime import datetime
import diamond.collector


class WebsiteMonitorCollector(diamond.collector.Collector):
    """
    Gather HTTP response code and Duration of HTTP request
    """

    def get_default_config_help(self):
        config_help = super(WebsiteMonitorCollector,
                            self).get_default_config_help()
        config_help.update({
            'URL': "FQDN of HTTP endpoint to test",

        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        default_config = super(WebsiteMonitorCollector,
                               self).get_default_config()
        default_config['URL'] = ''
        default_config['path'] = 'websitemonitor'
        return default_config

    def collect(self):
        req = urllib2.Request('%s' % (self.config['URL']))

        try:
            # time in seconds since epoch as a floating number
            start_time = time.time()
            # human-readable time e.g November 25, 2013 18:15:56
            st = datetime.fromtimestamp(start_time
                                        ).strftime('%B %d, %Y %H:%M:%S')
            self.log.debug('Start time: %s' % (st))

            resp = urllib2.urlopen(req)
            # time in seconds since epoch as a floating number
            end_time = time.time()
            # human-readable end time e.eg. November 25, 2013 18:15:56
            et = datetime.fromtimestamp(end_time).strftime('%B %d, %Y %H:%M%S')
            self.log.debug('End time: %s' % (et))
            # Response time in milliseconds
            rt = int(format((end_time - start_time) * 1000, '.0f'))
            # Publish metrics
            self.publish('response_time.%s' % (resp.code), rt,
                         metric_type='COUNTER')
        # urllib2 will puke on non HTTP 200/OK URLs
        except urllib2.URLError, e:
            if e.code != 200:
                # time in seconds since epoch as a floating number
                end_time = time.time()
                # Response time in milliseconds
                rt = int(format((end_time - start_time) * 1000, '.0f'))
                # Publish metrics -- this is recording a failure, rt will
                # likely be 0 but does capture HTTP Status Code
                self.publish('response_time.%s' % (e.code), rt,
                             metric_type='COUNTER')

        except IOError, e:
            self.log.error('Unable to open %s' % (self.config['URL']))

        except Exception, e:
            self.log.error("Unknown error opening url: %s", e)
