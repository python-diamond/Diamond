ExampleCollector
=====

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

For testing collectors, create a directory (example below for /tmp/diamond)
containing your new collector(s), their .conf files, and a copy of diamond.conf
with the following options in diamond.conf:

    [server]

    user = ecuser
    group = ecuser

    handlers = diamond.handler.archive.ArchiveHandler
    handlers_config_path = /tmp/diamond/handlers/
    collectors_path = /tmp/diamond/collectors/
    collectors_config_path = /tmp/diamond/collectors/

    collectors_reload_interval = 3600

    [handlers]

    [[default]]

    [[ArchiveHandler]]
    log_file = /dev/stdout

    [collectors]
    [[default]]

and then run diamond in foreground mode:

    # diamond -f -l --skip-pidfile -c /tmp/diamond/diamond.conf

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


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

