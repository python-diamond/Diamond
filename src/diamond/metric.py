# coding=utf-8

import time
import re
import logging
from error import DiamondException


class Metric(object):

    _METRIC_TYPES = ['COUNTER', 'GAUGE']

    def __init__(self, path, value, raw_value=None, timestamp=None, precision=0,
                 host=None, metric_type='COUNTER'):
        """
        Create new instance of the Metric class

        Takes:
            path=string: string the specifies the path of the metric
            value=[float|int]: the value to be submitted
            timestamp=[float|int]: the timestamp, in seconds since the epoch
            (as from time.time()) precision=int: the precision to apply.
            Generally the default (2) should work fine.
        """

        # Validate the path, value and metric_type submitted
        if (path is None
            or value is None
            or metric_type not in self._METRIC_TYPES):
            raise DiamondException("Invalid parameter.")

        # If no timestamp was passed in, set it to the current time
        if timestamp is None:
            timestamp = int(time.time())
        else:
            # If the timestamp isn't an int, then make it one
            if not isinstance(timestamp, int):
                try:
                    timestamp = int(timestamp)
                except ValueError, e:
                    raise DiamondException("Invalid parameter: %s" % e)

        # The value needs to be a float or an int.  If it is, great.  If not,
        # try to cast it to one of those.
        if not isinstance(value, int) and not isinstance(value, float):
            try:
                if precision == 0:
                    value = round(float(value))
                else:
                    value = float(value)
            except ValueError, e:
                raise DiamondException("Invalid parameter: %s" % e)

        self.path = path
        self.value = value
        self.raw_value = raw_value
        self.timestamp = timestamp
        self.precision = precision
        self.host = host
        self.metric_type = metric_type

    def __repr__(self):
        """
        Return the Metric as a string
        """
        if not isinstance(self.precision, (int, long)):
            log = logging.getLogger('diamond')
            log.warn('Metric %s does not have a valid precision', self.path)
            self.precision = 0

        # Set the format string
        fstring = "%%s %%0.%if %%i\n" % self.precision

        # Return formated string
        return fstring % (self.path, self.value, self.timestamp)

    @classmethod
    def parse(cls, string):
        """
        Parse a string and create a metric
        """
        match = re.match(r'^(?P<name>[A-Za-z0-9\.\-_]+)\s+'
                         + '\(?P<value>[0-9\.]+)\s+'
                         + '(?P<timestamp>[0-9\.]+)(\n?)$',
                         string)
        try:
            groups = match.groupdict()
            # TODO: get precision from value string
            return Metric(groups['name'],
                          groups['value'],
                          float(groups['timestamp']))
        except:
            raise DiamondException(
                "Metric could not be parsed from string: %s." % string)

    def getPathPrefix(self):
        """
            Returns the path prefix path
            servers.host.cpu.total.idle
            return "servers"
        """
        # If we don't have a host name, assume it's just the first part of the
        # metric path
        if self.host is None:
            return self.path.split('.')[0]

        offset = self.path.index(self.host) - 1
        return self.path[0:offset]

    def getCollectorPath(self):
        """
            Returns collector path
            servers.host.cpu.total.idle
            return "cpu"
        """
        # If we don't have a host name, assume it's just the third part of the
        # metric path
        if self.host is None:
            return self.path.split('.')[2]

        offset = self.path.index(self.host)
        offset += len(self.host) + 1
        endoffset = self.path.index('.', offset)
        return self.path[offset:endoffset]

    def getMetricPath(self):
        """
            Returns the metric path after the collector name
            servers.host.cpu.total.idle
            return "total.idle"
        """
        # If we don't have a host name, assume it's just the fourth+ part of the
        # metric path
        if self.host is None:
            path = self.path.split('.')[3:]
            return '.'.join(path)

        prefix = self.getPathPrefix()
        prefix += '.'
        prefix += self.host
        prefix += '.'
        prefix += self.getCollectorPath()
        prefix += '.'

        offset = len(prefix)
        return self.path[offset:]
