<!--This file was generated from the python source
Please edit the source to make changes
-->
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

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
get_default_config_help |  | get_default_config_help | 
host |  |  | str
port | 123 |  | int
server_error_interval | 120 | How frequently to send repeated server errors | int
transport | tcp | tcp or udp | str
