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
import re
import httplib
import urlparse

import diamond.collector 

class HttpdCollector(diamond.collector.Collector):
    """
    Collect stats from Apache HTTPD server using mod_status
    """
 
    def collect(self):
        # Parse Url
        parts = urlparse.urlparse(self.config['url'])

        # Parse host and port
        endpoint = parts[1].split(':') 
        if len(endpoint) > 1:
            service_host = endpoint[0]
            service_port = int(endpoint[1])
        else:
            service_host = endpoint[0]
            service_port = 80

        # Parse path
        service_path = parts[2]

        metrics = ['ReqPerSec', 'BytesPerSec', 'BytesPerReq', 'BusyWorkers', 'IdleWorkers'] 
        
        # Setup Connection 
        connection = httplib.HTTPConnection(service_host, service_port)
        
        try:
            connection.request("GET", "%s?%s" % (parts[2], parts[4]))
        except Exception, e:
            self.log.error("Error retrieving HTTPD stats. %s" % e)
            return

        response = connection.getresponse()
        data = response.read()
        exp = re.compile('^([A-Za-z]+):\s+(.+)$');
        for line in data.split('\n'):
            if line:
                m = exp.match(line)
                if m:
                    k = m.group(1)
                    v = m.group(2)
                    if k in metrics:
                        # Get Metric Name
                        metric_name = "%s" % (k)
                        # Get Metric Value
                        metric_value = "%d" % float(v)
                        # Publish Metric
                        self.publish(metric_name, metric_value)
