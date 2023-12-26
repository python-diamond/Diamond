# coding=utf-8

"""
Collect dhcp stats from kea
```

#### Dependencies

    * Kea with control-socket enabled
    * It currently supports kea ipv4

Example config file kea.conf
```
enabled=True
control_socket_v4=/var/run/kea/kea-dhcp4.socket
```

"""

import json
import socket
import diamond.collector
from diamond.collector import str_to_bool
from diamond import convertor
from string import Template

class KeaCollector(diamond.collector.Collector):

    __metrics__ = [
        'pkt4-received', 'pkt4-discover-received', 'pkt4-offer-received',
        'pkt4-request-received', 'pkt4-ack-received', 'pkt4-nak-received',
        'pkt4-receive-drop', 'pkt4-release-received', 'pkt4-decline-received',
        'pkt4-inform-received', 'pkt4-unknown-received', 'pkt4-sent',
        'pkt4-offer-sent', 'pkt4-ack-sent', 'pkt4-nak-sent',
        'pkt4-parse-failed', 'pkt4-receive-drop', 'reclaimed-leases',
        'declined-addresses', 'reclaimed-declined-addresses'
    ]

    __query__ = Template('{ "command": "statistic-get", "arguments": {"name": "$name"} }')



    def get_default_config_help(self):
        config_help = super(KeaCollector, self).get_default_config_help()
        config_help.update({
            'control_socket': 'Path to kea control socket',
        })
        return config_help

    def get_default_config(self):
        """Return default config

        :rtype: dict
        """
        config = super(KeaCollector, self).get_default_config()
        config.update({
            'control_socket': '/var/run/kea/kea-dhcp4.socket',
        })
        return config

    def get_kea_stats(self):
        """Yield data from kea after reading it from the control socket
        """
        for item in self.__metrics__:
            try:
                conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                conn.connect(self.config['control_socket'])
                conn.sendall(self.__query__.substitute(name=item))
                ### At the moment the payload has a maximum size of 8192
                #   so I am limiting it to this size
                data = json.loads(conn.recv(8192))
                if 'arguments' in data and item in data['arguments']:
                    yield (item, data['arguments'][item][0][0])
                else:
                    yield (item, 0)
            finally:
                conn.close()

    def collect(self):
        """Collect metrics from kea running locally 
        """
        for name, value in self.get_kea_stats():
            self.publish(name, value)

