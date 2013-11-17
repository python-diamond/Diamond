# coding=utf-8

"""
DRBD metric collector

  Read and publish metrics from all available resources in /proc/drbd
"""

import diamond.collector
import re


class DRBDCollector(diamond.collector.Collector):
    """
    DRBD Simple metric collector
    """
    def get_default_config_help(self):
        config_help = super(DRBDCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(DRBDCollector, self).get_default_config()
        config.update({
            'path': 'drbd'
        })
        return config

    def collect(self):
        """
        Overrides the Collector.collect method
        """
        performance_indicators = {
            'ns': 'network_send',
            'nr': 'network_receive',
            'dw': 'disk_write',
            'dr': 'disk_read',
            'al': 'activity_log',
            'bm': 'bit_map',
            'lo': 'local_count',
            'pe': 'pending',
            'ua': 'unacknowledged',
            'ap': 'application_pending',
            'ep': 'epochs',
            'wo': 'write_order',
            'oos': 'out_of_sync',
            'cs': 'connection_state',
            'ro': 'roles',
            'ds': 'disk_states'
             }

        results = dict()
        try:
            with open('/proc/drbd', 'r') as statusfile:
                current_resource = ''
                for line in statusfile:
                    if re.search('version', line) is None:
                        if re.search(r' \d: cs', line):
                            matches = re.match(r' (\d): (cs:\w+) (ro:\w+/\w+) '
                                               '(ds:\w+/\w+) (\w{1}) .*', line)
                            current_resource = matches.group(1)
                            results[current_resource] = dict()
                        elif re.search(r'\sns:', line):
                            metrics = line.strip().split(" ")
                            for metric in metrics:
                                item, value = metric.split(":")
                                results[current_resource][
                                    performance_indicators[item]] = value

                    else:
                        continue
        except IOError as errormsg:
            self.log.error("Can't read DRBD status file: {0}".format(errormsg))
            return

        for resource in results.keys():
            for metric_name, metric_value in results[resource].items():
                if metric_value.isdigit():
                    self.publish(resource + "." + metric_name, metric_value)
                else:
                    continue
