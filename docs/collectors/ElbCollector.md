ElbCollector
=====

The ELB collector collects metrics for one or more Amazon AWS ELBs

#### Configuration

Below is an example configuration for the ELBCollector.
You can specify an arbitrary amount of regions

```
    enabled = true
    interval = 60

    # Optional
    access_key_id = ...
    secret_access_key = ...

    # Optional - Available keys: region, zone, elb_name, metric_name
    format = $elb_name.$zone.$metric_name

    # Optional - list of regular expressions used to ignore ELBs
    elbs_ignored = ^elb-a$, .*-test$, $test-.*

    [regions]

    [[us-west-1]]
    # Optional - queries all elbs if omitted
    elb_names = elb1, elb2, ...

    [[us-west-2]]
    ...

```

#### Dependencies

 * boto


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

