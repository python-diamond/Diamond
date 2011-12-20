# Copyright (C) 2011 by Rob Smith
# http://www.kormoc.com
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

import subprocess

import diamond.collector

class PingCollector(diamond.collector.Collector):
    """
    Collect icmp round trip times
    Only valid for ipv4 hosts currently
    """

    def collect(self):
        for key in self.config.keys():
            if key[:7] == "target_":
                host = self.config[key]
                metric_name = "ping."+host.replace('.','_');

                ping = subprocess.Popen(["ping", '-nq', '-c 1', host], stdout=subprocess.PIPE).communicate()[0].strip().split("\n")[-1]
                if ping[0:3] != 'rtt':
                    metric_value = 10000
                else :
                    ping = ping.split()[3].split('/')[0]
                    metric_value = int(round(float(ping)))
                self.publish(metric_name, metric_value)
