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

class TCPCollector(diamond.collector.Collector):
    """
    The TCPCollector class collects metrics on TCP stats from
    /proc/net/netstat
    """

    PROC='/proc/net/netstat'

    def collect(self):
        if not os.access(self.PROC, os.R_OK):
            return None

        lines = []

        file = open(self.PROC)
        for line in file:
            if line.startswith("TcpExt:"):
                lines.append(line[7:].split())
        file.close()

        if len(lines) == 0:
            return

        if len(lines) != 2:
            return

        # There are two lines in lines: names and values, space-separated.
        names, values = lines
        allowed_names = self.config['allowed_names']

        for key, value in zip(names, values):
            if key in allowed_names:
                self.publish(key, value, 0)
