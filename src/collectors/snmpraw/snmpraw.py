# coding=utf-8

"""
The SNMPRawCollector is designed for collecting data from SNMP-enables devices,
using a set of specified OIDs

#### Configuration

Below is an example configuration for the SNMPRawCollector. The collector
can collect data any number of devices by adding configuration sections
under the *devices* header. By default the collector will collect every 60
seconds. This might be a bit excessive and put unnecessary load on the
devices being polled. You may wish to change this to every 300 seconds. However
you need modify your graphite data retentions to handle this properly.

```
    # Options for SNMPRawCollector
    enabled = True
    interval = 60

    [devices]

    # Start the device configuration
    # Note: this name will be used in the metric path.
    [[my-identification-for-this-host]]
    host = localhost
    port = 161
    community = public

    # Start the OID list for this device
    # Note: the value part will be used in the metric path.
    [[[oids]]]
    1.3.6.1.4.1.2021.10.1.3.1 = cpu.load.1min
    1.3.6.1.4.1.2021.10.1.3.2 = cpu.load.5min
    1.3.6.1.4.1.2021.10.1.3.3 = cpu.load.15min

    # If you want another host, you can. But you probably won't need it.
    [[another-identification]]
    host = router1.example.com
    port = 161
    community = public
    [[[oids]]]
    oid = metric.path
    oid = metric.path
```

Note: If you modify the SNMPRawCollector configuration, you will need to
restart diamond.

#### Dependencies

 * pysmnp (which depends on pyasn1 0.1.7 and pycrypto)

"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'snmp'))
from snmp import SNMPCollector as parent_SNMPCollector
from diamond.metric import Metric


class SNMPRawCollector(parent_SNMPCollector):

    def process_config(self):
        # list to save non-existing oid's per device, to avoid repetition of
        # errors in logging. Signal USR1 to diamond/collector to flush this
        self.skip_list = []

    def get_default_config(self):
        """
        Override SNMPCollector.get_default_config method to provide
        default_config for the SNMPInterfaceCollector
        """
        default_config = super(SNMPRawCollector,
                               self).get_default_config()
        default_config.update({
            'oids': {},
            'path_prefix': 'servers',
            'path_suffix': 'snmp',
        })
        return default_config

    def _precision(self, value):
        """
        Return the precision of the number
        """
        value = str(value)
        decimal = value.rfind('.')
        if decimal == -1:
            return 0
        return len(value) - decimal - 1

    def _skip(self, device, oid, reason=None):
        self.skip_list.append((device, oid))
        if reason is not None:
            self.log.warn('Muted \'{0}\' on \'{1}\', because: {2}'.format(
                oid, device, reason))

    def _get_value_walk(self, device, oid, host, port, community):
        data = self.walk(oid, host, port, community)

        if data is None:
            self._skip(device, oid, 'device down (#2)')
            return

        self.log.debug('Data received from WALK \'{0}\': [{1}]'.format(
            device, data))

        if len(data) != 1:
            self._skip(
                device,
                oid,
                'unexpected response, data has {0} entries'.format(
                    len(data)))
            return

        # because we only allow 1-key dicts, we can pick with absolute index
        value = data.items()[0][1]
        return value

    def _get_value(self, device, oid, host, port, community):
        data = self.get(oid, host, port, community)

        if data is None:
            self._skip(device, oid, 'device down (#1)')
            return

        self.log.debug('Data received from GET \'{0}\': [{1}]'.format(
            device, data))

        if len(data) == 0:
            self._skip(device, oid, 'empty response, device down?')
            return

        if oid not in data:
            # oid is not even in hierarchy, happens when using 9.9.9.9
            # but not when using 1.9.9.9
            self._skip(device, oid, 'no object at OID (#1)')
            return

        value = data[oid]
        if value == 'No Such Object currently exists at this OID':
            self._skip(device, oid, 'no object at OID (#2)')
            return

        if value == 'No Such Instance currently exists at this OID':
            return self._get_value_walk(device, oid, host, port, community)

        return value

    def collect_snmp(self, device, host, port, community):
        """
        Collect SNMP interface data from device
        """
        self.log.debug(
            'Collecting raw SNMP statistics from device \'{0}\''.format(device))

        dev_config = self.config['devices'][device]
        if 'oids' in dev_config:
            for oid, metricName in dev_config['oids'].items():

                if (device, oid) in self.skip_list:
                    self.log.debug(
                        'Skipping OID \'{0}\' ({1}) on device \'{2}\''.format(
                            oid, metricName, device))
                    continue

                timestamp = time.time()
                value = self._get_value(device, oid, host, port, community)
                if value is None:
                    continue

                self.log.debug(
                    '\'{0}\' ({1}) on device \'{2}\' - value=[{3}]'.format(
                        oid, metricName, device, value))

                path = '.'.join([self.config['path_prefix'], device,
                                 self.config['path_suffix'], metricName])
                metric = Metric(path=path, value=value, timestamp=timestamp,
                                precision=self._precision(value),
                                metric_type='GAUGE')
                self.publish_metric(metric)
