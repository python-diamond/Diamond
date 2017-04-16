# coding=utf-8

"""
Collect data from nvidia-smi
"""

import diamond.collector
from subprocess import Popen, PIPE
import xml.etree.ElementTree as etree

from diamond.collector import str_to_bool


class NvidiaCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = (
            super(NvidiaCollector, self).get_default_config_help())
        config_help.update({
            'bin': 'The path to the nvidaia-smi',
            'use_sudo': 'Use sudo?',
            'sudo_cmd': 'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        """
        Returns default configuration options.
        """
        config = super(NvidiaCollector, self).get_default_config()
        config.update({
            'bin': 'nvidia-smi',
            'use_sudo': False,
            'sudo_cmd': '/usr/bin/sudo',
        })
        return config

    def collect(self):
        """
        Collect and publish nvidia-smi stats
        """
        cmd = [self.config['bin'], "list"]

        if str_to_bool(self.config['use_sudo']):
            cmd.insert(0, self.config['sudo_cmd'])

        nvidia_smi_data = Popen(cmd, stdout=PIPE).communicate()[0]
        root = etree.fromstring(nvidia_smi_data)

        prefix = 'nvidia-smi'
        for x in root.findall('gpu'):
            product_name = x.find('product_name').text
            product_id = x.attrib['id'].replace('.', ':')
            metric = '%s.%s.%s' % \
                     (prefix, sanitize_metric_name(product_name), product_id)
            for metric in get_metrics(x, metric):
                self.publish(metric[0], metric[1])


def get_metrics(root, metric):
    metrics = []
    for x in list(root):
        name = sanitize_metric_name(x.tag)
        if not list(x) and x.text != 'N/A' and x.text.strip() != '':
            value = parse_value(x.text)
            if value is not None:
                metrics.append((metric + '.' + name, value))
        metrics.extend(get_metrics(x, metric + '.' + name))
    return metrics


def parse_value(value):
    v = value.split(' ')[0].replace('x', '')
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def sanitize_metric_name(name):
    return name.replace(' ', '_').replace('.', '_').replace('/', '_')
