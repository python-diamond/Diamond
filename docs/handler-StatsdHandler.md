StatsdHandler
====

Implements the abstract Handler class, sending data to statsd.
This is a UDP service, sending datagrams.  They may be lost.
It's OK.

#### Dependencies

 * [python-statsd](http://pypi.python.org/pypi/python-statsd/)
 * [statsd](https://github.com/etsy/statsd) v0.1.1 or newer.

#### Configuration

Enable this handler

 * handlers = diamond.handler.stats_d.StatsdHandler


#### Notes


The handler file is named an odd stats_d.py because of an import issue with
having the python library called statsd and this handler's module being called
statsd, so we use an odd name for this handler. This doesn't affect the usage
of this handler.

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>batch</td><td>1</td><td></td><td>int</td></tr>
<tr><td>get_default_config_help</td><td></td><td>get_default_config_help</td><td></td></tr>
<tr><td>host</td><td></td><td></td><td>str</td></tr>
<tr><td>port</td><td>1234</td><td></td><td>int</td></tr>
<tr><td>server_error_interval</td><td>120</td><td>How frequently to send repeated server errors</td><td>int</td></tr>
</table>

### This file was generated from the python source
### Please edit the source to make changes

