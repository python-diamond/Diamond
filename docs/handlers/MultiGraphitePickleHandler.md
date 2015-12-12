MultiGraphitePickleHandler
====

Send metrics to a [graphite](http://graphite.wikidot.com/) using the pickle
interface. Unlike GraphitePickleHandler, this one supports multiple graphite
servers. Specify them as a list of hosts divided by comma.
#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>batch</td><td>1</td><td>How many to store before sending to the graphite server</td><td>int</td></tr>
<tr><td>get_default_config_help</td><td></td><td>get_default_config_help</td><td></td></tr>
<tr><td>host</td><td>localhost,</td><td>Hostname, Hostname, Hostname</td><td>list</td></tr>
<tr><td>max_backlog_multiplier</td><td>5</td><td>how many batches to store before trimming</td><td>int</td></tr>
<tr><td>port</td><td>2003</td><td>Port</td><td>int</td></tr>
<tr><td>proto</td><td>tcp</td><td>udp or tcp</td><td>str</td></tr>
<tr><td>server_error_interval</td><td>120</td><td>How frequently to send repeated server errors</td><td>int</td></tr>
<tr><td>timeout</td><td>15</td><td></td><td>int</td></tr>
<tr><td>trim_backlog_multiplier</td><td>4</td><td>Trim down how many batches</td><td>int</td></tr>
</table>

### This file was generated from the python source
### Please edit the source to make changes

