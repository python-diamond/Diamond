GraphiteHandler
====

Send metrics to a [graphite](http://graphite.wikidot.com/) using the high
performace pickle interface.

Graphite is an enterprise-scale monitoring tool that runs well on cheap
hardware. It was originally designed and written by Chris Davis at Orbitz in
2006 as side project that ultimately grew to be a foundational monitoring tool.
In 2008, Orbitz allowed Graphite to be released under the open source Apache
2.0 license. Since then Chris has continued to work on Graphite and has
deployed it at other companies including Sears, where it serves as a pillar of
the e-commerce monitoring system. Today many
[large companies](http://graphite.readthedocs.org/en/latest/who-is-using.html)
use it.

- enable it in `diamond.conf` :

`    handlers = diamond.handler.graphitepickle.GraphitePickleHandler
`

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>batch</td><td>1</td><td>How many to store before sending to the graphite server</td><td>int</td></tr>
<tr><td>flow_info</td><td>0</td><td>IPv6 Flow Info</td><td>int</td></tr>
<tr><td>get_default_config_help</td><td></td><td>get_default_config_help</td><td></td></tr>
<tr><td>host</td><td>localhost</td><td>Hostname</td><td>str</td></tr>
<tr><td>keepalive</td><td>0</td><td>Enable keepalives for tcp streams</td><td>int</td></tr>
<tr><td>keepaliveinterval</td><td>10</td><td>How frequently to send keepalives</td><td>int</td></tr>
<tr><td>max_backlog_multiplier</td><td>5</td><td>how many batches to store before trimming</td><td>int</td></tr>
<tr><td>port</td><td>2003</td><td>Port</td><td>int</td></tr>
<tr><td>proto</td><td>tcp</td><td>udp, udp4, udp6, tcp, tcp4, or tcp6</td><td>str</td></tr>
<tr><td>scope_id</td><td>0</td><td>IPv6 Scope ID</td><td>int</td></tr>
<tr><td>server_error_interval</td><td>120</td><td>How frequently to send repeated server errors</td><td>int</td></tr>
<tr><td>timeout</td><td>15</td><td></td><td>int</td></tr>
<tr><td>trim_backlog_multiplier</td><td>4</td><td>Trim down how many batches</td><td>int</td></tr>
</table>

### This file was generated from the python source
### Please edit the source to make changes

