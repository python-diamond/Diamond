# coding=utf-8

"""
An example collector that verifies the answer to life, the universe, and
everything does not change.

#### Dependencies

 * A sane universe

#### Customizing a collector

Diamond collectors run within the diamond process and collect metrics that can
be published to a graphite server.

Collectors are subclasses of diamond.collector.Collector. In their simplest
form, they need to implement a single method called "collect".

    import diamond.collector

    class ExampleCollector(diamond.collector.Collector):

        def collect(self):
            # Set Metric Name
            metric_name = "my.example.metric"

            # Set Metric Value
            metric_value = 42

            # Publish Metric
            self.publish(metric_name, metric_value)

To run this collector in test mode you can invoke the diamond server with the
-r option and specify the collector path.

>  diamond -f -l -r path/to/ExampleCollector.py -c conf/diamond.conf.example

Diamond supports dynamic addition of collectors. Its configured to scan for new
collectors on a regular interval (configured in diamond.cfg).
If diamond detects a new collector, or that a collectors module has changed
(based on the file's mtime), it will be reloaded.

Diamond looks for collectors in /usr/lib/diamond/collectors/ (on Ubuntu). By
default diamond will invoke the *collect* method every 60 seconds.

Diamond collectors that require a separate configuration file should place a
.cfg file in /etc/diamond/collectors/.
The configuration file name should match the name of the diamond collector
class.  For example, a collector called
*examplecollector.ExampleCollector* could have its configuration file placed in
/etc/diamond/collectors/ExampleCollector.cfg.

"""

import diamond.collector


class ExampleCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(ExampleCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ExampleCollector, self).get_default_config()
        config.update({
            'path':     'example'
        })
        return config

    def collect(self):
        """
        Overrides the Collector.collect method
        """

        # Set Metric Name
        metric_name = "my.example.metric"
        # Set Metric Value
        metric_value = 42

        # Publish Metric
        self.publish(metric_name, metric_value)
