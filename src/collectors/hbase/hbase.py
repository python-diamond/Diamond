# coding=utf-8

"""
Diamond collector for HBase metrics, see:
"""

from diamond.metric import Metric
import diamond.collector
import glob
import re
import os


class HBaseCollector(diamond.collector.Collector):

    re_log = re.compile(r'^(?P<timestamp>\d+) (?P<name>\S+): (?P<metrics>.*)$')

    def get_default_config_help(self):
        config_help = super(HBaseCollector, self).get_default_config_help()
        config_help.update({
            'metrics': "List of paths to process metrics from",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(HBaseCollector, self).get_default_config()
        config.update({
            'path':     'hbase',
            'metrics':  ['/var/log/hbase/*.metrics'],
        })
        return config

    def collect(self):
        for pattern in self.config['metrics']:
            for filename in glob.glob(pattern):
                self.collect_from(filename)

    def collect_from(self, filename):
        if not os.access(filename, os.R_OK):
            self.log.error('HBaseCollector unable to read "%s"', filename)
            return False

        fd = open(filename, 'r+')
        for line in fd:
            match = self.re_log.match(line)
            if not match:
                continue

            metrics = {}

            data = match.groupdict()
            for metric in data['metrics'].split(','):
                metric = metric.strip()
                if '=' in metric:
                    key, value = metric.split('=', 1)
                    metrics[key] = value

            for metric in metrics.keys():
                try:

                    if data['name'] == 'jvm.metrics':
                        path = self.get_metric_path('.'.join([
                            data['name'],
                            metrics['hostName'].replace('.', '_'),
                            metrics['processName'].replace(' ', '_'),
                            metric, ]))

                    elif data['name'] == 'mapred.job':
                        path = self.get_metric_path('.'.join([
                            data['name'],
                            metrics['hostName'].replace('.', '_'),
                            metrics['group'].replace(' ', '_'),
                            metrics['counter'].replace(' ', '_'),
                            metric, ]))

                    elif data['name'] == 'rpc.metrics':

                        if metric == 'port':
                            continue

                        path = self.get_metric_path('.'.join([
                            data['name'],
                            metrics['hostName'].replace('.', '_'),
                            metrics['port'],
                            metric, ]))

                    else:
                        path = self.get_metric_path('.'.join([
                            data['name'],
                            metric, ]))

                    value = float(metrics[metric])

                    self.publish_metric(Metric(path,
                                        value,
                                        timestamp=int(data['timestamp'])/1000))

                except ValueError:
                    pass
        fd.seek(0)
        fd.truncate()
        fd.close()
