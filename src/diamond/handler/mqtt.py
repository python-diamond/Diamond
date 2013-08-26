# coding=utf-8

"""
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

"""

__author__ = 'Jan-Piet Mens'
__email__ = 'jpmens@gmail.com'

from Handler import Handler
import mosquitto
from diamond.collector import get_hostname
import os
HAVE_SSL = True
try:
    import ssl
except ImportError:
    HAVE_SSL = False


class MQTTHandler(Handler):
    """
    """

    def __init__(self, config=None):
        """
        Create a new instance of the MQTTHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)

        # Initialize Data
        self.mqttc = None
        self.hostname = get_hostname(self.config)
        self.client_id = "%s_%s" % (self.hostname, os.getpid())

        # Initialize Options
        self.host = self.config.get('host', 'localhost')
        self.port = 0
        self.qos = int(self.config.get('qos', 0))
        self.prefix = self.config.get('prefix', "")
        self.tls = self.config.get('tls', False)
        self.timestamp = 0
        try:
            self.timestamp = self.config['timestamp']
            if not self.timestamp:
                self.timestamp = 1
            else:
                self.timestamp = 0
        except:
            self.timestamp = 1

        # Initialize
        self.mqttc = mosquitto.Mosquitto(self.client_id, clean_session=True)

        if not self.tls:
            self.port = int(self.config.get('port', 1883))
        else:
            # Set up TLS if requested

            self.port = int(self.config.get('port', 8883))

            self.cafile = self.config.get('cafile', None)
            self.certfile = self.config.get('certfile', None)
            self.keyfile = self.config.get('keyfile', None)

            if (self.cafile is None
                or self.certfile is None
                or self.keyfile is None):
                self.log.error("MQTTHandler: TLS configuration missing.")
                return

            try:
                self.mqttc.tls_set(
                    self.cafile,
                    certfile=self.certfile,
                    keyfile=self.keyfile,
                    cert_reqs=ssl.CERT_REQUIRED,
                    tls_version=3,
                    ciphers=None)
            except:
                self.log.error("MQTTHandler: Cannot set up TLS "
                               + "configuration. Files missing?")

        self.mqttc.will_set("clients/diamond/%s" % (self.hostname),
                payload="Adios!", qos=0, retain=False)
        self.mqttc.connect(self.host, self.port, 60)

        self.mqttc.on_disconnect = self._disconnect

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(MQTTHandler, self).get_default_config_help()

        config.update({
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(MQTTHandler, self).get_default_config()

        config.update({
        })

        return config

    def process(self, metric):
        """
        Process a metric by converting metric name to MQTT topic name;
        the payload is metric and timestamp.
        """

        line = str(metric)
        topic, value, timestamp = line.split()
        if len(self.prefix):
            topic = "%s/%s" % (self.prefix, topic)
        topic = topic.replace('.', '/')
        topic = topic.replace('#', '&')     # Topic must not contain wildcards

        if self.timestamp == 0:
            self.mqttc.publish(topic, "%s" % (value), self.qos)
        else:
            self.mqttc.publish(topic, "%s %s" % (value, timestamp), self.qos)

    def _disconnect(self, mosq, obj, rc):

        self.log.debug("MQTTHandler: reconnecting to broker...")
        mosq.reconnect()
