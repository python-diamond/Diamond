# coding=utf-8

"""
The TrendEmicCollector is designed for collecting data from Trend Ethernet
Metering Interface Controllers (EMIC), such as the ones at:
https://partners.trendcontrols.com/trendproducts/cd/en/ecatdata/pg_allemic.html

#### Configuration

Below is an example configuration for the TrendEmicCollector. The collector
can collect data any number of devices by adding configuration sections
under the *devices* header. By default the collector will collect every 1
second.

```
    # Options for TrendEmicCollector
    enabled = True
    interval = 4

    [devices]

    # Start the device configuration
    # Note: this name will be used in the metric path.
    [[my-identification-for-this-emic]]
    host = X.X.X.X
```

Note: If you modify the TrendEmicCollector configuration, you will need to
restart diamond.

#### Dependencies

"""

import urllib
import httplib
import diamond.collector


class TrendEmicCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(TrendEmicCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(TrendEmicCollector, self).get_default_config()
        config.update({
            'path':     'trend_emic'
        })
        return config

    def strip_emic(self, data):
        i = data.index('=')
        while isinstance(i, int):
            data = data[i+1:]
            try:
                i = data.index('=')
            except:
                i = None
        return data[:-1]

    def parse_emic(self, data):
        raw = self.strip_emic(data)
        rows = []
        for row in raw.split('|'):
            fields = row.split('~')
            rows.append(fields)
        return rows

    def parse_metrics(self, rows):
        metrics = []
        for row in rows:
            if row[0] is not '':
                parsed_row = {}
                parsed_row['name'] = urllib.unquote(row[0]).decode('utf-8')
                parsed_row['value'] = row[1]
                parsed_row['units'] = row[2]
                metrics.append(parsed_row)
        return metrics

    def connection(self, host):
        return httplib.HTTPConnection(host)

    def build_params(self, cmd, iq_id):
        if iq_id is None:
            return "CMD={0}".format(cmd)
        else:
            return "CMD={0}&IQ={1}".format(cmd, iq_id)

    def get_data(self, host, cmd, iq_id=None):
        headers = {"Content-type": "application/x-www-form-urlencoded",
                                   "Accept": "*/*"}
        conn = self.connection(host)
        conn.request("POST", "/cgi-bin/virtualiq.cgi",
                     self.build_params(cmd, iq_id), headers)

        response = conn.getresponse()
        data = None
        if response.status == 200:
            data = response.read()
        conn.close()
        return data

    def meters(self, host):
        rows = self.parse_emic(self.get_data(host, 1))
        iq_ids = []
        for row in rows:
            if row[0] is not '':
                iq_id = {}
                iq_id['id'] = row[0]
                iq_id['name'] = urllib.unquote(row[2]).decode('utf-8')
                iq_ids.append(iq_id)
        return iq_ids

    def get_emic(self, host, cmd, iq_id=None):
        return self.parse_emic(self.get_data(host, cmd, iq_id))

    def get_metrics(self, host, meter_id):
        return self.parse_metrics(self.get_emic(host, 20, meter_id))

    def format_path(self, device, meter, metric_name, metric_unit):
        return "{0}.{1}.{2}.{3}".format(
            device, meter, metric_name, metric_unit)

    def collect(self):
        """
        Collect Emic data
        """
        devices = self.config['devices']
        for name, device in devices.iteritems():
            host = device['host']
            self.log.debug(
                'Collecting Trend EMIC data from device \'{0}\' at {1}'
                    .format(name, host))
            meters = self.meters(host)
            for meter in meters:
                metrics = self.get_metrics(host, meter['id'])
                for metric in metrics:
                    metric_path = self.format_path(
                        name,
                        meter['name'],
                        metric['name'],
                        metric['units']).replace(" ", "_").lower()
                    metric_value = float(metric['value'])
                    self.publish(metric_path,
                                 metric_value,
                                 precision=1,
                                 metric_type='GAUGE')
