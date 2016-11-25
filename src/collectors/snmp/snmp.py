# coding=utf-8

"""
The SNMPCollector is designed for collecting data from SNMP-enables devices,
using a set of specified OIDs

#### Configuration

Below is an example configuration for the SNMPCollector. The collector
can collect data any number of devices by adding configuration sections
under the *devices* header. By default the collector will collect every 60
seconds. This might be a bit excessive and put unnecessary load on the
devices being polled. You may wish to change this to every 300 seconds. However
you need modify your graphite data retentions to handle this properly.

```
    [[SNMPCollector]]
    enabled = True
    interval = 60

    [[[devices]]]

    # Start the device configuration
    # Note: this name will be used in the metric path.
    [[[[my-identification-for-this-host]]]]
    host = localhost
    port = 161
    community = public

    # Start the OID list for this device
    # Note: the value part will be used in the metric path.
    [[[[[oids]]]]]
    1.3.6.1.4.1.2021.10.1.3.1 = cpu.load.1min
    1.3.6.1.4.1.2021.10.1.3.2 = cpu.load.5min
    1.3.6.1.4.1.2021.10.1.3.3 = cpu.load.15min

    # If you want another host, you can. But you probably won't need it.
    [[[[another-identification]]]]
    host = router1.example.com
    port = 161
    community = public
    [[[[[oids]]]]]
    oid = metric.path
    oid = metric.path
```

Note: If you modify the SNMPRawCollector configuration, you will need to
restart diamond.

#### Dependencies

 * pysmnp (which depends on pyasn1 0.1.7 and pycrypto)

"""

import re
import socket
import warnings

# pysnmp packages on debian 6.0 use sha and md5 which are deprecated
# packages. there is nothing to be done about it until pysnmp
# updates to use new hashlib module -- ignoring warning for now
old_showwarning = warnings.showwarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

cmdgen = None
IntegerType = None

try:
    # Note only here for safety. The collector will log if this fails to load
    import pysnmp.entity.rfc3413.oneliner.cmdgen as cmdgen
    from pyasn1.type.univ import Integer as IntegerType
except ImportError:
    pass

warnings.showwarning = old_showwarning

import diamond.collector


class SNMPCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(SNMPCollector, self).get_default_config_help()
        config_help.update({
            'timeout': 'Seconds before timing out the snmp connection',
            'retries': 'Number of times to retry before bailing',
        })
        return config_help

    def get_default_config(self):
        # Initialize default config
        default_config = super(SNMPCollector, self).get_default_config()
        default_config.update({
            'path': 'snmp',
            'timeout': 5,
            'retries': 3,
            'devices': {},
        })
        return default_config

    def _to_oid_tuple(self, s):
        """
        Convert an OID string into a tuple of integers

        :param s: an OID string
        :returns: A tuple of integers
        """
        if not isinstance(s, (tuple, list)):
            s = s.split('.')
        return tuple(map(int, s))

    def _from_oid_tuple(self, oid):
        """
        Convert a tuple of integers into an OID string

        :param oid: a tuple of integers
        :returns: a period delimited string of integers
        """
        if not isinstance(oid, (tuple, list)):
            return oid
        return '.'.join(map(str, oid))

    def _precision(self, value):
        """
        Return the precision of the number
        """
        value = str(value)
        decimal = value.rfind('.')
        if decimal == -1:
            return 0
        return len(value) - decimal - 1

    def _publish(self, device, oid, basename, name, value):
        """
        Publishes a metric as a GAUGE with a given value. Non-integer
        datatyps are attempted to be converted to a float value, and
        ignored if they cannot be. This will also replace a root OID
        with a basename. For example, if given a root oid '1.2',
        basename 'foo.bar', and name '1.2.3.4.5', the result would be
        'foo.bar.3.4.5'.

        :param device: the device name string
        :param oid: Root OID string
        :param basename: The replacement string of the OID root string
        :param name: An instance of pysnmp.proto.rfc1902.ObjectName
        :param value: Some form of subclass instance of
                      pyasn1.type.base.AbstractSimpleAsn1Item
        """
        # If metric value is 'empty'
        if not value:
            self.log.debug("Metric '{0}' has no value".format(name))
            return None

        # Simple integer types need no special work
        if isinstance(value, IntegerType):
            value = value.prettyPrint()
        else:
            # Otherwise attempt to convert to a float
            try:
                value = float(value.prettyPrint())
            except ValueError:
                self.log.debug(
                    "Metric '{0}' is not an Integer type".format(name)
                )
                return

        # Convert to a simple readable format
        name = name.prettyPrint()
        name = re.sub(r'^{0}'.format(oid), basename, name)

        self.log.debug(
            "'{0}' on device '{1}' - value=[{2}]".format(
                name, device, value
            )
        )

        path = '.'.join([
            'devices',
            device,
            name,
        ])

        self.publish_gauge(path, value)

    def get(self, oid, host, port, community):
        """
        Backwards compatible snmp_get
        """
        auth = self.create_auth(community)
        transport = self.create_transport(host, port)
        rows = self.snmp_get(oid, auth, transport)
        return dict((k.prettyPrint(), v.prettyPrint()) for k, v in rows)

    def walk(self, oid, host, port, community):
        """
        Backwards compatible snmp_walk
        """
        auth = self.create_auth(community)
        transport = self.create_transport(host, port)
        rows = self.snmp_walk(oid, auth, transport)
        return dict((k.prettyPrint(), v.prettyPrint()) for k, v in rows)

    def snmp_get(self, oid, auth, transport):
        """
        Perform SNMP get for a given OID

        :param oid: An OID string or tuple to query
        :param auth: a CommunityData instance for authentication
        :param transport: an SNMP transport target (UdpTransportTarget)
        :returns: list of SNMP (name, value) tuples
        """
        # Run the SNMP GET query
        result = self.cmdgen.getCmd(auth, transport, self._to_oid_tuple(oid))

        try:
            return result[3]
        except (ValueError, IndexError):
            self.log.debug(
                "SNMP GET '{0}' on host '{1}' returned no data".format(
                    oid, transport.transportAddr[0]
                )
            )
        return []

    def snmp_walk(self, oid, auth, transport):
        """
        Perform an SNMP walk on a given OID

        :param oid: An OID string or tuple to query
        :param auth: a CommunityData instance for authentication
        :param transport: an SNMP transport target (UdpTransportTarget)
        :returns: list of SNMP (name, value) tuples
        """
        # Run the SNMP WALK query
        result = self.cmdgen.nextCmd(auth, transport, self._to_oid_tuple(oid))

        try:
            return [item[0] for item in result[3]]
        except IndexError:
            self.log.debug(
                "SNMP WALK '{0}' on host '{1}' returned no data".format(
                    oid, transport.transportAddr[0]
                )
            )
        return []

    def create_transport(self, host, port):
        """
        Create a pysnmp UDP transport target with the given host and port

        :param host: hostname string
        :param port: integer port number
        :return: pysnmp UdpTransportTarget
        """
        # Get the IP addr of the host
        host = socket.gethostbyname(host)

        timeout = int(self.config['timeout'])
        retries = int(self.config['retries'])

        return cmdgen.UdpTransportTarget((host, port), timeout, retries)

    def create_auth(self, community):
        """
        Create a pysnmp CommunityData object

        :param community: community auth string
        :returns: pysnmp CommunityData
        """
        return cmdgen.CommunityData('agent', community)

    def collect_snmp(self, device, host, port, community):
        """
        Collect SNMP interface data from a device. Devices should
        be configured with an [oids] section that includes name-value
        pairs for data to gather. For example:

            [oids]
            1.3.6.1.4.1.1111 = my.metric.name

        There are special circumstances where one could obtain large
        swaths of data using an SNMP walk. In this situation, metrics
        aren't named, but namespaced by OID value in graphite:

            [oids]
            1.2.6.1.4.1.1111.* = my.metric.name

        Note, this will replace anything preceding .* with the name on
        the right hand side. Anything obtained from this walk will be
        namespaced according to the remaining portion of the OID.
        For example:

            my.metric.name.1
            my.metric.name.2.1
            my.metric.name.2.2
            my.metric.name.2.3
        """
        self.log.debug("Collecting SNMP data from device '{0}'".format(device))

        auth = self.create_auth(community)
        transport = self.create_transport(host, port)
        oids = self.config['devices'][device]['oids']

        for oid, basename in oids.items():
            if oid.endswith('.*'):  # Walk
                oid = oid[:-2]
                fn = self.snmp_walk
            else:
                fn = self.snmp_get

            for metric_name, metric_value in fn(oid, auth, transport):
                self._publish(device.replace('.', '_'),
                              oid,
                              basename,
                              metric_name,
                              metric_value)

    def collect(self):
        """
        Collect stats via SNMP
        """
        if not cmdgen:
            self.log.error(
                'pysnmp.entity.rfc3413.oneliner.cmdgen failed to load'
            )
            return

        # If there are no devices, nothing can be collected
        if 'devices' not in self.config:
            self.log.error('No devices configured for this collector')
            return

        # Initialize SNMP Command Generator
        self.cmdgen = cmdgen.CommandGenerator()

        # Collect SNMP data from each device
        for device, config in self.config['devices'].items():
            host = config['host']
            port = int(config.get('port', 161))
            community = config.get('community', 'public')
            self.collect_snmp(device, host, port, community)
