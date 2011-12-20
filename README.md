About
=====

Diamond is a python daemon that collects system metrics and publishes them to Graphite. It is
capable of collecting cpu, memory, network, i/o, load and disk metrics.  Additionally,
it features an API for implementing custom collectors for gathering metrics from almost any source.

Installation
=====

** Core Dependencies**

-   CentOS or Ubuntu
-   Python 2.4+
-   python-configobj
-   pyasn1

** Optional Dependencies**
-   pysnmp

Usage
=====

To install diamond:

    make install

For testing, diamond can also be started directly via ant without installing:

    cp conf/diamond.conf.example conf/diamond.conf
    edit conf/diamond.conf
    make run

The *run* task will invoke diamond in debug mode for testing.

Ant can also build packages for CentOS/RHEL, Ubuntu/Debian, or generate a tar ball.

    make buildrpm
    sudo yum localinstall --nogpgcheck dist/diamond-0.2.0-1.noarch.rpm

    make builddeb
    sudo dpkg -i dist/diamond-0.2.0-1.deb

    make tar
    tar -xzvf dist/diamond-0.2.0.tar.gz

Configuration
=====

If you've installed diamond via a package, the configuration file is /etc/diamond/diamond.cfg. By default, diamond
will push to a graphite server host "graphite". You should probably change this to point to your own graphite server.

Other configuration should not be necessary.

By default diamond publishes metrics using the following form:

    systems.<hostname>.<metrics>.<metric>

You can override the "systems" portion of the metric path by changing the "path_prefix" setting in the configuration file.

Built-In Collectors
======

-   CPUCollector
-   DiskSpaceCollector
-   DiskUsageCollector
-   FilestatCollector
-   LoadAverageCollector
-   MemoryCollector
-   NetworkCollector
-   SockstatCollector
-   TCPCollector
-   UserScriptsCollector
-   VMStatCollector

Custom Collectors
======

Diamond collectors run within the diamond process and collect metrics that can be published to a graphite server.

Collectors are subclasses of diamond.collector.Collector. In their simplest form, they need to implement a single method called "collect".

    import diamond.collector

    class ExampleCollector(diamond.collector.Collector):

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

To run this collector in test mode you can invoke the diamond server with the -r option and specify the collector path.

> python src/diamond/server.py -f -v -r examples/examplecollector.py

Diamond supports dynamic addition of collectors. Its configured to scan for new collectors on a regular interval (configured in diamond.cfg).
If diamond detects a new collector, or that a collectors module has changed (based on the file's mtime), it will be reloaded.

Diamond looks for collectors in /usr/lib/diamond/collectors/ (on Ubuntu). By default diamond will invoke the *collect* method every 60 seconds.

Diamond collectors that require a separate configuration file should place a .cfg file in /etc/diamond/.
The configuration file name should match the name of the diamond collector class.  For example, a collector called
*examplecollector.ExampleCollector* could have its configuration file placed in /etc/diamond/ExampleCollector.cfg.


Contacts
=====

**Maintainer:** [Andy Kipp](mailto:akipp@brightove.com "Andy Kipp")

Contributors
=====

[Ivan Pouzyrevsky](https://github.com/sandello)
[ooshlablu](https://github.com/ooshlablu)
[oxcd8o](https://github.com/oxcd8o)
[Rob Smith](https://github.com/kormoc)
