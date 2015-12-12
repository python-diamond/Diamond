SqsCollector
=====

The SQS collector collects metrics for one or more Amazon AWS SQS queues

#### Configuration

Below is an example configuration for the SQSCollector.
You can specify an arbitrary amount of regions

```
    enabled = True
    interval = 60

    [regions]
    [[region-code]]
    access_key_id = '...'
    secret_access_key = '''
    queues = queue_name[,queue_name2[,..]]

```

Note: If you modify the SQSCollector configuration, you will need to
restart diamond.

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

