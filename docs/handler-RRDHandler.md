RRDHandler
====

Save stats in RRD files using rrdtool.
#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>basedir</td><td>/var/lib/collectd/rrd</td><td>The base directory for all RRD files.</td><td>str</td></tr>
<tr><td>batch</td><td>1</td><td>Wait for this many updates before saving to the RRD file</td><td>int</td></tr>
<tr><td>get_default_config_help</td><td></td><td>get_default_config_help</td><td></td></tr>
<tr><td>server_error_interval</td><td>120</td><td>How frequently to send repeated server errors</td><td>int</td></tr>
<tr><td>step</td><td>10</td><td>The minimum interval represented in generated RRD files.</td><td>int</td></tr>
</table>

### This file was generated from the python source
### Please edit the source to make changes

