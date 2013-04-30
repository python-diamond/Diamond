# coding=utf-8

"""
Send metrics to an MQTT broker.

### Dependencies

* [mosquitto](http://mosquitto.org/documentation/python/)

In order for this to do something useful, you'll need an
MQTT broker (e.g. [mosquitto](http://mosquitto.org) and
a diamond.conf containing something along these lines:

        [server]
        handlers = diamond.handler.mqtt.MQTTHandler
        ...
        [handlers]

        [[MQTTHandler]]
        host = address-of-mqtt-broker
        port = 1883

Test by launching an MQTT subscribe, e.g.:

        mosquitto_sub  -v -t 'servers/#'

### Notes

* This handler sets a last will and testament, so that the broker
  publishes its death at a topic called clients/diamond/<hostname>

"""

__author__ = 'Jan-Piet Mens'
__email__ = 'jpmens@gmail.com'

from Handler import Handler
import mosquitto
from diamond.collector import get_hostname
import os


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
        self.host = self.config['host']
        self.port = int(self.config['port'])

        # Initialize
        self.mqttc = mqttc = mosquitto.Mosquitto(self.client_id, clean_session=True)
        self.mqttc.will_set("clients/diamond/%s" % (self.hostname),
                payload="Adios!", qos=0, retain=False)
        self.mqttc.connect(self.host, self.port, 60)

    def process(self, metric):
        """
        Process a metric by converting metric name to MQTT topic name;
        the payload is metric and timestamp.
        """

        line = str(metric)
        topic, value, timestamp = line.split()
        topic = topic.replace('.', '/')
        topic = topic.replace('#', '&')     # Topic must not contain wildcards

        self.mqttc.publish(topic, "%s %s" % (value, timestamp), 0)
