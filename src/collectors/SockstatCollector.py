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

from diamond import *
import diamond.collector

_RE = re.compile('|'.join([
    r'sockets: used (?P<used>\d+)',
    r'TCP: inuse (?P<tcp_inuse>\d+) orphan (?P<tcp_orphan>\d+) tw (?P<tcp_tw>\d+) alloc (?P<tcp_alloc>\d+) mem (?P<tcp_mem>\d+)',
    r'UDP: inuse (?P<udp_inuse>\d+) mem (?P<udp_mem>\d+)'
]))

class SockstatCollector(diamond.collector.Collector):
    """
    Uses /proc/net/sockstat to collect data on number of open sockets
    """

    PROC = '/proc/net/sockstat'

    def collect(self):
        if not os.access(self.PROC, os.R_OK):
            return None

        result = {}

        file = open(self.PROC)
        for line in file:
            match = _RE.match(line)
            if match:
                for key, value in match.groupdict().items():
                    if value:
                        result[key] = int(value)
        file.close()

        for key, value in result.items():
            self.publish(key, value)
