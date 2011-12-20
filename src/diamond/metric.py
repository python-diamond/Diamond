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

import time
import re

from error import *

class Metric(object):

    def __init__(self, path, value, timestamp = None, precision = 0):
        """
        Create new instance of the Metric class

        Takes:
            path=string: string the specifies the path of the metric
            value=[float|int]: the value to be submitted
            timestamp=[float|int]: the timestamp, in seconds since the epoch (as from time.time())
            precision=int: the precision to apply.  Generally the default (2) should work fine.
        """

        # Validate the path and value submitted
        if path is None or value is None:
            raise DiamondException, "Invalid parameter."

        # If no timestamp was passed in, set it to the current time
        if timestamp is None:
            timestamp = int(time.time())
        else:
            # If the timestamp isn't an int, then make it one
            if not isinstance(timestamp, int):
                try:
                    timestamp = int(timestamp)
                except ValueError, e:
                    raise DiamondException, "Invalid parameter: %s" % e

        # The value needs to be a float or an int.  If it is, great.  If not, try to cast it to one of those.
        if not isinstance(value, int) and not isinstance(value, float):
            try:
                if precision == 0:
                    value = round(float(value))
                else:
                    value = float(value)
            except ValueError, e:
                    raise DiamondException, "Invalid parameter: %s" % e

        self.path = path
        self.value = value
        self.timestamp = timestamp
        self.precision = precision

    def __repr__(self):
        """
        Return the Metric as a string
        """
        # Set the format string
        fstring = "%%s %%0.%if %%i\n" % (self.precision)

        # Return formated string
        return fstring % (self.path, self.value, self.timestamp)

    @classmethod
    def parse(cls, string):
        """
        Parse a string and create a metric
        """
        match = re.match(r'^(?P<name>[A-Za-z0-9\.\-_]+)\s+(?P<value>[0-9\.]+)\s+(?P<timestamp>[0-9\.]+)(\n?)$', string)
        try:
            groups = match.groupdict()
            # TODO: get precision from value string
            return Metric(groups['name'], groups['value'], float(groups['timestamp']))
        except:
            raise DiamondException, "Metric could not be parsed from string: %s." % (string)
