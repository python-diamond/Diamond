RiemannHandler
====

Send metrics to [Riemann](http://aphyr.github.com/riemann/).

#### Dependencies

 * [Bernhard](https://github.com/banjiewen/bernhard).

#### Configuration

Add `diamond.handler.riemann.RiemannHandler` to your handlers.
It has these options:

 * `host` - The Riemann host to connect to.
 * `port` - The port it's on.
 * `transport` - Either `tcp` or `udp`. (default: `tcp`)

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>get_default_config_help</td><td></td><td>get_default_config_help</td><td></td></tr>
<tr><td>host</td><td></td><td></td><td>str</td></tr>
<tr><td>port</td><td>123</td><td></td><td>int</td></tr>
<tr><td>server_error_interval</td><td>120</td><td>How frequently to send repeated server errors</td><td>int</td></tr>
<tr><td>transport</td><td>tcp</td><td>tcp or udp</td><td>str</td></tr>
</table>

### This file was generated from the python source
### Please edit the source to make changes

