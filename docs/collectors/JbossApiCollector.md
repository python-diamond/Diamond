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



#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>app_stats</td><td>True</td><td>Collect application pool stats</td><td>str</td></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>connector_options</td><td>http, ajp,</td><td>Types of connectors to collect</td><td>list</td></tr>
<tr><td>connector_stats</td><td>True</td><td>Collect HTTP and AJP Connector stats</td><td>str</td></tr>
<tr><td>curl_bin</td><td>/usr/bin/curl</td><td>Path to system curl executable</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>hosts</td><td>,</td><td>List of hosts to collect from. Format is yourusername:yourpassword@host:port:proto</td><td>list</td></tr>
<tr><td>jvm_buffer_pool_stats</td><td>True</td><td>Collect JVM buffer-pool stats</td><td>str</td></tr>
<tr><td>jvm_gc_stats</td><td>True</td><td>Collect JVM garbage-collector stats</td><td>str</td></tr>
<tr><td>jvm_memory_pool_stats</td><td>True</td><td>Collect JVM memory-pool stats</td><td>str</td></tr>
<tr><td>jvm_memory_stats</td><td>True</td><td>Collect JVM basic memory stats</td><td>str</td></tr>
<tr><td>jvm_thread_stats</td><td>True</td><td>Collect JVM thread stas</td><td>str</td></tr>
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

