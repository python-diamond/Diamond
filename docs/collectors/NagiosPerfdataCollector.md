NagiosPerfdataCollector
=====

The NagiosPerfdataCollector parses Nagios performance data in the
PNP4Nagios/Graphios/Metricinga key-value format.

#### Dependencies

 * Nagios configured to periodically dump performance data files in
   PNP4Nagios format

Configuring Nagios/Icinga
-------------------------
If you're already using Graphios, you're already set up to send metrics through
Metricinga, and you can skip to the next section! If not, read on.

### Modifying the daemon configuration

The default performance data output format used by Nagios and Icinga can't be
easily extended to contain new attributes, so we're going to replace it with
one that prints key-value pairs instead. This will allow us to add in whatever
kind of bookkeeping attributes we want! We need these to do things like override
the display name of a service with a metric name more meaningful to Graphite.

We'll need to edit one of the following files:

* **For Nagios:** /etc/nagios/nagios.cfg
* **For Icinga:** /etc/icinga/icinga.cfg

Make sure that the following configuration keys are set to something like the
values below:

    process_performance_data=1
    host_perfdata_file=/var/spool/nagios/host-perfdata
    host_perfdata_file_mode=a
    host_perfdata_file_processing_command=process-host-perfdata-file
    host_perfdata_file_processing_interval=60
    host_perfdata_file_template=DATATYPE::HOSTPERFDATA	TIMET::$TIMET$	HOSTNAME::$HOSTNAME$	HOSTPERFDATA::$HOSTPERFDATA$	HOSTCHECKCOMMAND::$HOSTCHECKCOMMAND$	HOSTSTATE::$HOSTSTATE$	HOSTSTATETYPE::$HOSTSTATETYPE$	GRAPHITEPREFIX::$_HOSTGRAPHITEPREFIX$	GRAPHITEPOSTFIX::$_HOSTGRAPHITEPOSTFIX$  # NOQA
    service_perfdata_file=/var/spool/nagios/service-perfdata
    service_perfdata_file_mode=a
    service_perfdata_file_processing_command=process-service-perfdata-file
    service_perfdata_file_processing_interval=60
    service_perfdata_file_template=DATATYPE::SERVICEPERFDATA	TIMET::$TIMET$	HOSTNAME::$HOSTNAME$	SERVICEDESC::$SERVICEDESC$	SERVICEPERFDATA::$SERVICEPERFDATA$	SERVICECHECKCOMMAND::$SERVICECHECKCOMMAND$	HOSTSTATE::$HOSTSTATE$	HOSTSTATETYPE::$HOSTSTATETYPE$	SERVICESTATE::$SERVICESTATE$	SERVICESTATETYPE::$SERVICESTATETYPE$	GRAPHITEPREFIX::$_SERVICEGRAPHITEPREFIX$	GRAPHITEPOSTFIX::$_SERVICEGRAPHITEPOSTFIX$  # NOQA

Note that you most likely will wish to change $_SERVICEGRAPHITEPREFIX$,
$_HOSTGRAPHITEPREFIX$, $_SERVICEGRAPHITEPOSTFIX$, and $_HOSTGRAPHITEPOSTFIX$

### Configuring file rotation

Next, the rotation commands need to be configured so the performance data files
are periodically moved into the Metrnagios spool directory. Depending on your
system configuration, these commands may be located in
`/etc/nagios/objects/commands.d`:

    define command {
        command_name    process-host-perfdata-file
        command_line    /bin/mv /var/spool/nagios/host-perfdata /var/spool/diamond/host-perfdata.$TIMET$  # NOQA
    }

    define command {
        command_name    process-service-perfdata-file
        command_line    /bin/mv /var/spool/nagios/service-perfdata /var/spool/diamond/service-perfdata.$TIMET$  # NOQA
    }

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>perfdata_dir</td><td>/var/spool/diamond/nagiosperfdata</td><td>The directory containing Nagios perfdata files</td><td>str</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

