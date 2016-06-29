# coding=utf-8

"""
Collect status codes from a HTTP or HTTPS connections

#### Dependencies

 * urllib2

#### Usage
Add the collector config as :

enabled = True
req_url = https://www.my_server.com/, https://www.my_server.com/assets/jquery.js

Metrics are collected as :
    - servers.<hostname>.http.<url>.response_code_<code> (response code)

    special chars are replaced by _, url looking like
       http://www.site.com/admin/page.html are replaced by
       http:__www_site_com_admin_page_html

#### Note
Since this is only about response codes, this does not valid SSL certificates.

"""

import urllib2
import diamond.collector
import re
import ssl


class HttpCodeCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(HttpCodeCollector, self).get_default_config_help()
        config_help.update({
            'req_url':
            'array of full URL to get (ex : https://www.ici.net/mypage.html)'
        })
        return config_help

    def get_default_config(self):
        default_config = super(HttpCodeCollector, self).get_default_config()
        default_config['path'] = 'http'
        default_config['req_url'] = ['http://localhost/']

        default_config['headers'] = {
            'User-Agent': 'Diamond HTTP collector', }
        return default_config

    def collect(self):
        # create urllib2 vars

        if type(self.config['req_url']) is list:
            req_urls = self.config['req_url']

        else:
            req_urls = [self.config['req_url']]

        # do the request
        for url in req_urls:
            response_code = None
            self.log.debug("collecting %s", str(url))
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = urllib2.Request(url, headers=self.config['headers'])
            try:
                try:
                    handle = urllib2.urlopen(req, context=ctx)

                except urllib2.HTTPError as e:
                    response_code = e.code

                else:
                    response_code = handle.getcode()

                self.log.debug("response code was %s", str(response_code))

                # build a compatible name : no '.' and no'/' in the name
                u = ''.join(url.split("://", 1)[1:]).rstrip('/')
                m_prefix = re.sub('[^0-9a-zA-Z]+', '_', u)

                self.publish_gauge(m_prefix +
                                   ".response_code." +
                                   str(response_code), 1)
                self.publish_gauge(m_prefix +
                                   ".response_code",
                                   response_code)

            except IOError as e:
                self.log.error("Unable to open %s : %s", url, e)

            except Exception as e:
                self.log.error("Unknown error opening url: %s - %s", url, e)
