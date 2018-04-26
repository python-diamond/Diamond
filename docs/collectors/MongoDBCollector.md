<!--This file was generated from the python source
Please edit the source to make changes
-->
MongoDBCollector
=====

Collects all number values from the db.serverStatus() command, other
values are ignored.

**Note:** this collector expects pymongo 2.4 and onward. See the pymongo
changelog for more details:
http://api.mongodb.org/python/current/changelog.html#changes-in-version-2-4

#### Dependencies

 * pymongo

#### Example Configuration

MongoDBCollector.conf

```
    enabled = True
    hosts = localhost:27017, alias1@localhost:27018, etc
```

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
collection_sample_rate | 1 | Only send stats for a consistent subset of collections. This is applied after collections are ignored via ignore_collections Sampling uses crc32 so it is consistent across replicas. Value between 0 and 1. Default is 1 | int
databases | .* | A regex of which databases to gather metrics for. Defaults to all databases. | str
enabled | False | Enable collecting these metrics | bool
host |  | A single hostname(:port) to get metrics from (can be used instead of hosts and overrides it) | 
hosts | localhost, | Array of hostname(:port) elements to get metrics fromSet an alias by prefixing host:port with alias@ | list
ignore_collections | ^tmp\.mr\. | A regex of which collections to ignore. MapReduce temporary collections (tmp.mr.*) are ignored by default. | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
network_timeout | None | Timeout for mongodb connection (in milliseconds). There is no timeout by default. | NoneType
passwd | None | Password for authenticated login (optional) | NoneType
replica | False | True to enable replica set logging. Reports health of individual nodes as well as basic aggregate stats. Default is False | bool
replset_node_name | _id | Identifier for reporting replset metrics. Default is _id | str
simple | False | Only collect the same metrics as mongostat. | str
ssl | False | True to enable SSL connections to the MongoDB server. Default is False | bool
translate_collections | False | Translate dot (.) to underscores (_) in collection names. | str
replace_dashes_in_metric_keys | True | Replace dashes (-) to dots (.) in database object names and metrics | str
user | None | Username for authenticated login (optional) | NoneType

#### Example Output

```
servers.hostname.mongo.db_keys.db_nested_key 1
servers.hostname.mongo.dbkey 2
```

