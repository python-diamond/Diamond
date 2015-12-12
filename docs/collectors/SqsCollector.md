<!--This file was generated from the python source
Please edit the source to make changes
-->
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


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
__EXAMPLESHERE__
```

