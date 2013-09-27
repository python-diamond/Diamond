# coding=utf-8

"""
The NagiosPerfdataCollector parses Nagios performance data in the
PNP4Nagios/Graphios/Metricinga key-value format.

#### Dependencies

 * Nagios configured to periodically dump performance data files in
   PNP4Nagios format

"""

import os
import re

import diamond.collector


class NagiosPerfdataCollector(diamond.collector.Collector):
    """Diamond collector for Nagios performance data
    """

    GENERIC_FIELDS = ['DATATYPE', 'HOSTNAME', 'TIMET']
    HOST_FIELDS = ['HOSTPERFDATA']
    SERVICE_FIELDS = ['SERVICEDESC', 'SERVICEPERFDATA']
    TOKENIZER_RE = (r"([^\s]+|'[^']+')=([-.\d]+)(c|s|ms|us|B|KB|MB|GB|TB|%)?"
    + r"(?:;([-.\d]+))?(?:;([-.\d]+))?(?:;([-.\d]+))?(?:;([-.\d]+))?")

    def __init__(self, config, handlers):
        super(NagiosPerfdataCollector, self).__init__(config, handlers)

    def get_default_config_help(self):
        config_help = super(NagiosPerfdataCollector,
                            self).get_default_config_help()
        config_help.update({
            'perfdata_dir': 'The directory containing Nagios perfdata files'
        })
        return config_help

    def get_default_config(self):
        config = super(NagiosPerfdataCollector, self).get_default_config()
        config.update({
            'enabled': 'False',
            'path': 'nagiosperfdata',
            'perfdata_dir': '/var/spool/diamond/nagiosperfdata',
            'method': 'Threaded'
        })
        return config

    def collect(self):
        """Collect statistics from a Nagios perfdata directory.
        """
        perfdata_dir = self.config['perfdata_dir']

        try:
            filenames = os.listdir(perfdata_dir)
        except OSError:
            self.log.error("Cannot read directory `{dir}'".format(
                    dir=perfdata_dir))
            return

        for filename in filenames:
            self._process_file(os.path.join(perfdata_dir, filename))

    def _extract_fields(self, line):
        """Extract the key/value fields from a line of performance data
        """
        acc = {}
        field_tokens = line.split("\t")
        for field_token in field_tokens:
            kv_tokens = field_token.split('::')
            if len(kv_tokens) == 2:
                (key, value) = kv_tokens
                acc[key] = value

        return acc

    def _fields_valid(self, d):
        """Verify that all necessary fields are present

        Determine whether the fields parsed represent a host or
        service perfdata. If the perfdata is unknown, return False.
        If the perfdata does not contain all fields required for that
        type, return False. Otherwise, return True.
        """
        if 'DATATYPE' not in d:
            return False

        datatype = d['DATATYPE']
        if datatype == 'HOSTPERFDATA':
            fields = self.GENERIC_FIELDS + self.HOST_FIELDS
        elif datatype == 'SERVICEPERFDATA':
            fields = self.GENERIC_FIELDS + self.SERVICE_FIELDS
        else:
            return False

        for field in fields:
            if field not in d:
                return False

        return True

    def _normalize_to_unit(self, value, unit):
        """Normalize the value to the unit returned.

        We use base-1000 for second-based units, and base-1024 for
        byte-based units. Sadly, the Nagios-Plugins specification doesn't
        disambiguate base-1000 (KB) and base-1024 (KiB).
        """
        if unit == 'ms':
            return value / 1000.0
        if unit == 'us':
            return value / 1000000.0
        if unit == 'KB':
            return value * 1024.0
        if unit == 'MB':
            return value * 1024768.0
        if unit == 'GB':
            return value * 1073741824.0
        if unit == 'TB':
            return value * 1099511627776.0

        return value

    def _parse_perfdata(self, s):
        """Parse performance data from a perfdata string
        """
        metrics = []
        counters = re.findall(self.TOKENIZER_RE, s)
        if counters is None:
            self.log.warning("Failed to parse performance data: {s}".format(
                    s=s))
            return metrics

        for (key, value, uom, warn, crit, min, max) in counters:
            try:
                norm_value = self._normalize_to_unit(float(value), uom)
                metrics.append((key, norm_value))
            except ValueError:
                self.log.warning("Couldn't convert value '{value}' to float" \
                        .format(value=value))

        return metrics

    def _process_file(self, path):
        """Parse and submit the metrics from a file
        """
        try:
            f = open(path)
            for line in f:
                self._process_line(line)

            os.remove(path)
        except IOError, ex:
            self.log.error("Could not open file `{path}': {error}".format(
                    path=path, error=ex.strerror))

    def _process_line(self, line):
        """Parse and submit the metrics from a line of perfdata output
        """
        fields = self._extract_fields(line)
        if not self._fields_valid(fields):
            self.log.warning("Missing required fields for line: {line}".format(
                    line=line))

        metric_path_base = []
        graphite_prefix = fields.get('GRAPHITEPREFIX')
        graphite_postfix = fields.get('GRAPHITEPOSTFIX')

        if graphite_prefix:
            metric_path_base.append(graphite_prefix)

        hostname = fields['HOSTNAME'].lower()
        metric_path_base.append(hostname)

        datatype = fields['DATATYPE']
        if datatype == 'HOSTPERFDATA':
            metric_path_base.append('host')
        elif datatype == 'SERVICEPERFDATA':
            service_desc = fields.get('SERVICEDESC')
            graphite_postfix = fields.get('GRAPHITEPOSTFIX')
            if graphite_postfix:
                metric_path_base.append(graphite_postfix)
            else:
                metric_path_base.append(service_desc)

        perfdata = fields[datatype]
        counters = self._parse_perfdata(perfdata)

        for (counter, value) in counters:
            metric_path = metric_path_base + [counter]
            metric_path = [self._sanitize(x) for x in metric_path]
            metric_name = '.'.join(metric_path)
            self.publish(metric_name, value)

    def _sanitize(self, s):
        """Sanitize the name of a metric to remove unwanted chars
        """
        return re.sub("[^\w-]", "_", s)
