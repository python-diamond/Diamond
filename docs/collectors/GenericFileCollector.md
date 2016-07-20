<!--This file was generated from the python source
Please edit the source to make changes
-->
GenericFileCollector
=====

This class collects data in key / value form from generic files.

The collector operates on each line of a file, expecting the line to match the
format provided by a configurable regular expression. It behaves similarly
to awk.

By default, the regular expression represents a common file pattern of key
values pairs separated by either space, colon or equals (with optional
surrounding space). The key value pairs can be any alphanumeric character.

If customization is required, you can provide a different regex. Furthermore,
you can override the match method if you need to do any further processing.

#### Dependencies

* re




#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
file |  | The file from which to collect the data. | 
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
regex | ^\s*(?P<key>\w+)\s*[\s|:|=]\s*(?P<value>\w+)\s*$ | Defines the line format of the file. | str

#### Example Output

```
__EXAMPLESHERE__
```

