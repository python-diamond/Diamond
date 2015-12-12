<!--This file was generated from the python source
Please edit the source to make changes
-->
JbossApiCollector
=====

V. 1.0

JbossApiCollector is a collector that uses JBOSS 7 native API to collect data
Tested on jboss 7.X.X??

Much of the code was borrowed from:

http://bit.ly/XRrCWx
https://github.com/lukaf/munin-plugins/blob/master/jboss7_

References:
https://docs.jboss.org/author/display/AS7/Management+API+reference
http://middlewaremagic.com/jboss/?p=2476

TODO:
This code was made to work with the local system 'curl' command, due to
difficulties getting urllib2 or pycurl to work under the python 2.4 options
successfully doing SSL Digest Authentication.

Plan is to make this code work with newer versions of python and possibly
Requests. (http://docs.python-requests.org/en/latest/)

If possible, please make future updates backwards compatible to call the local
curl as an option.


#### Dependencies

 * java
 * jboss
 * curl
 * json

##### Configuration

# Uses local system curl until can be made to work with either urllib2, pycurl,
or requests (http://docs.python-requests.org/en/latest/)


enabled = True
path_suffix = ""
measure_collector_time = False
interface_regex = ^(.+?)\.
curl_bin = /usr/bin/curl
connect_timeout = 4
hosts = wasadmin:pass@host:9443:https, wasadmin:pass@host:9443:https
curl_options = "-s --digest -L "
ssl_options = "--sslv3 -k"
connector_stats = True | False
connector_options =  http, ajp
app_stats = True | False
jvm_memory_stats = True | False
jvm_buffer_pool_stats = True | False
jvm_memory_pool_stats = True | False
jvm_gc_stats = True | False
jvm_thread_stats = True | False



#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
app_stats | True | Collect application pool stats | str
byte_unit | byte | Default numeric output(s) | str
connector_options | http, ajp, | Types of connectors to collect | list
connector_stats | True | Collect HTTP and AJP Connector stats | str
curl_bin | /usr/bin/curl | Path to system curl executable | str
enabled | False | Enable collecting these metrics | bool
hosts | , | List of hosts to collect from. Format is yourusername:yourpassword@host:port:proto | list
jvm_buffer_pool_stats | True | Collect JVM buffer-pool stats | str
jvm_gc_stats | True | Collect JVM garbage-collector stats | str
jvm_memory_pool_stats | True | Collect JVM memory-pool stats | str
jvm_memory_stats | True | Collect JVM basic memory stats | str
jvm_thread_stats | True | Collect JVM thread stas | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
__EXAMPLESHERE__
```

