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
from diamond.metric import Metric

# Detect the architecture of the system and set the counters for MAX_VALUES
# appropriately. Otherwise, rolling over counters will cause incorrect or
# negative values.

if platform.architecture()[0] == '64bit':
    MAX_COUNTER = (2 ** 64) - 1
else:
    MAX_COUNTER = (2 ** 32) - 1

from diamond.metric import Metric

class Collector(object):
    """
    The Collector class is a base class for all metric collectors.
    """

    def __init__(self, config, handlers):
        """
        Create a new instance of the Collector class
        """
        # Initialize Logger
        self.log = logging.getLogger('diamond')
        # Initialize Members
        self.name = self.__class__.__name__
        self.handlers = handlers
        self.last_values = {}

        # Get Collector class
        cls = self.__class__

        # Initialize config
        self.config = configobj.ConfigObj()
        # Merge default Collector config
        self.config.merge(config['collectors']['default'])
        # Check if default config is defined
        if self.get_default_config() is not None:
            # Merge default config
            self.config.merge(self.get_default_config())
        # Check if Collector config section exists
        if cls.__name__ in config['collectors']:
            # Merge Collector config section
            self.config.merge(config['collectors'][cls.__name__])

        # Check for config file in config directory
        configfile = os.path.join(config['server']['collectors_config_path'], cls.__name__) + '.conf'
        if os.path.exists(configfile):
            # Merge Collector config file
            self.config.merge(configobj.ConfigObj(configfile))

    def get_default_config(self):
        """
        Return the default config for the collector
        """
        return {}

    def get_schedule(self):
        """
        Return schedule for the collector
        """
        # Return a dict of tuples containing (collector function, collector function args, splay, interval)
        return {self.__class__.__name__: (self._run, None, int(self.config['splay']), int(self.config['interval']))}

    def get_metric_path(self, name):
        """
        Get metric path
        """
        if 'path_prefix' in self.config:
            prefix = self.config['path_prefix']
        else:
            prefix = 'systems'

        if 'hostname' in self.config:
            hostname = self.config['hostname']
        else:
            hostname = socket.getfqdn().split('.')[0]

        if 'path' in self.config:
            path = self.config['path']
        else:
            path = self.__class__.__name__

        if path == '.':
            return '.'.join([prefix, hostname, name])
        else:
            return '.'.join([prefix, hostname, path, name])

    def collect(self):
        """
        Default collector method
        """
        raise NotImplementedError()

    def publish(self, name, value, precision=0):
        """
        Publish a metric with the given name
        """
        # Get metric Path
        path = self.get_metric_path(name)

        # Create Metric
        metric = Metric(path, value, None, precision)

        # Publish Metric
        self.publish_metric(metric)

    def publish_metric(self, metric):
        """
        Publish a Metric object
        """
        # Process Metric
        for h in self.handlers:
            h.process(metric)

    def derivative(self, name, new, max_value=0):
        """
        Calculate the derivative of the metric.
        """
        # Format Metric Path
        path = self.get_metric_path(name)

        if path in self.last_values:
            old = self.last_values[path]
            # Check for rollover
            if new < old:
                old = old - max_value
            # Get Change in X (value)
            dx = new - old
            # Get Change in Y (time)
            dy = int(self.config['interval'])
            result =  float(dx) / float(dy)
        else:
            result = 0

        # Store Old Value
        self.last_values[path] = new

        # Return result
        return result

    def _run(self):
        """
        Run the collector
        """
        # Log
        self.log.debug("Collecting data from: %s" % (self.__class__.__name__))
        try:
            # Collect Data
            self.collect()
        except Exception, e:
            # Log Error
            self.log.error(traceback.format_exc())
