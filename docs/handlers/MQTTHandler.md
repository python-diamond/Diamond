<!--This file was generated from the python source
Please edit the source to make changes
-->
MQTTHandler
====

Send metrics to an MQTT broker.

### Dependencies

* [mosquitto](http://mosquitto.org/documentation/python/)
* Python `ssl` module (and Python >= 2.7)

In order for this to do something useful, you'll need an
MQTT broker (e.g. [mosquitto](http://mosquitto.org) and
a `diamond.conf` containing something along these lines:

        [server]
        handlers = diamond.handler.mqtt.MQTTHandler
        ...
        [handlers]

        [[MQTTHandler]]
        host = address-of-mqtt-broker  (default: localhost)
        port = 1883         (default: 1883; with tls, default: 8883)
        qos = 0             (default: 0)

        # If False, do not include timestamp in the MQTT payload
        # i.e. just the metric number
        timestamp = True

        # Optional topic-prefix to prepend to metrics en-route to
        # MQTT broker
        prefix = some/pre/fix       (default: "")

        # If you want to connect to your MQTT broker with TLS, you'll have
        # to set the following four parameters
        tls = True          (default: False)
        cafile =        /path/to/ca/cert.pem
        certfile =      /path/to/certificate.pem
        keyfile =       /path/to/key.pem

Test by launching an MQTT subscribe, e.g.:

        mosquitto_sub  -v -t 'servers/#'

or
        mosquitto_sub -v -t 'some/pre/fix/#'

### To Graphite

You may be interested in
[mqtt2graphite](https://github.com/jpmens/mqtt2graphite)
which subscribes to an MQTT broker and sends metrics off to Graphite.

### Notes

* This handler sets a last will and testament, so that the broker
  publishes its death at a topic called clients/diamond/<hostname>
* Support for reconnecting to a broker is implemented and ought to
  work.

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
