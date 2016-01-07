<!--This file was generated from the python source
Please edit the source to make changes
-->
StatsdHandler
====

Implements the abstract Handler class, sending data to statsd.
This is a UDP service, sending datagrams.  They may be lost.
It's OK.

#### Dependencies

 * [statsd](https://pypi.python.org/pypi/statsd/) v2.0.0 or newer.
 * A compatible implementation of [statsd](https://github.com/etsy/statsd)

#### Configuration

Enable this handler

 * handlers = diamond.handler.stats_d.StatsdHandler


#### Notes


The handler file is named an odd stats_d.py because of an import issue with
having the python library called statsd and this handler's module being called
statsd, so we use an odd name for this handler. This doesn't affect the usage
of this handler.

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
