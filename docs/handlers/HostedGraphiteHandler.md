HostedGraphiteHandler
====

[Hosted Graphite](https://www.hostedgraphite.com/) is the powerful open-source
application metrics system used by hundreds of companies. We take away the
headaches of scaling, maintenance, and upgrades and let you do what you do
best - write great software.

#### Configuration

Enable this handler

 * handlers = diamond.handler.hostedgraphite.HostedGraphiteHandler,

 * apikey = API_KEY

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>apikey</td><td></td><td>Api key to use</td><td>str</td></tr>
<tr><td>batch</td><td>1</td><td>How many to store before sending to the graphite server</td><td>int</td></tr>
<tr><td>get_default_config_help</td><td></td><td>get_default_config_help</td><td></td></tr>
<tr><td>host</td><td>carbon.hostedgraphite.com</td><td>Hostname</td><td>str</td></tr>
<tr><td>max_backlog_multiplier</td><td>5</td><td>how many batches to store before trimming</td><td>int</td></tr>
<tr><td>port</td><td>2003</td><td>Port</td><td>int</td></tr>
<tr><td>proto</td><td>tcp</td><td>udp or tcp</td><td>str</td></tr>
<tr><td>server_error_interval</td><td>120</td><td>How frequently to send repeated server errors</td><td>int</td></tr>
<tr><td>timeout</td><td>15</td><td></td><td>int</td></tr>
<tr><td>trim_backlog_multiplier</td><td>4</td><td>Trim down how many batches</td><td>int</td></tr>
</table>

### This file was generated from the python source
### Please edit the source to make changes

