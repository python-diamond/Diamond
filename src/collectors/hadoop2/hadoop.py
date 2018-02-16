# coding=utf-8

"""
Diamond collector for Hadoop metrics2, see:

 * [http://blog.cloudera.com/blog/2012/10/what-is-hadoop-metrics2/](Metrics2)

#### Dependencies

 * hadoop

"""

import glob
import os
import re
import time
import uuid

from diamond.metric import Metric
from diamond.collector import Collector, str_to_bool


RESERVED_NAME = 'TEMP_DIAMOND_METRICS_FILE'

NEW_CONFIGS = {
    'metric_files': {
        'default': ['/var/log/hadoop/*-metrics.out'],
        'help': "List of paths to process metrics from."
    },
    'truncate': {
        'default': False,
        'help': "Truncate the metrics files after reading them."
    }
}


class HadoopMetrics2Collector(Collector):

    re_log = re.compile(r'^(?P<timestamp>\d+) (?P<name>\S+): (?P<metrics>.*)$')

    def __generate_unique_filename(self, base):
        formatted_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime())
        return '{}_{}_{}'.format(base, formatted_time, uuid.uuid4())

    def __get_new_configs(self, val):
        return dict(map(lambda (a, b): (a, b[val]), NEW_CONFIGS.items()))

    def get_default_config_help(self):
        config_help = super(HadoopMetrics2Collector, self).get_default_config_help()
        config_help.update(self.__get_new_configs('help'))
        return config_help

    def get_default_config(self):
        config = super(HadoopMetrics2Collector, self).get_default_config()
        config.update(self.__get_new_configs('default'))
        return config

    def collect(self):
        metrics = self.config['metric_files']
        if not isinstance(metrics, list):
            metrics = [str(metrics)]

        for pattern in metrics:
            for filename in glob.glob(pattern):
                self._collect_from(filename)

    def _collect_from(self, filename):
        """Loops through each line in the file, parses the logged data into
        metrics, and publishes the metrics."""
        if not os.access(filename, os.R_OK):
            self.log.error('HadoopMetrics2Collector unable to read "%s"', filename)
            return

        self.config['hostname_method'] = 'uname_short'

        if str_to_bool(self.config['truncate']):
            # It is too dangerous to truncate a file that may be in the process
            # of being appended to; especially since most file systems do not
            # provide functionality for removing data from the start of a file.
            # As such we simply rename the file and delete the entire file when
            # we are finished.
            original_filename = filename
            filename = os.path.join(os.path.dirname(original_filename),
                                    self.__generate_unique_filename(RESERVED_NAME))
            os.rename(original_filename, filename)

        _file = open(filename, 'r')

        for line in _file:
            match = self.re_log.match(line)
            if not match:
                continue
            raw_data = match.groupdict()

            metrics = {}
            extra_data = {}
            for metric in raw_data['metrics'].split(','):
                metric = metric.strip()
                if '=' in metric:
                    key, value = metric.split('=', 1)
                    try:
                        metrics[key] = round(float(value))
                    except ValueError:
                        extra_data[key] = value

            host = extra_data.get('Hostname', None) or self.get_hostname()
            partial_path = 'hadoop.{}.'.format(raw_data['name'])

            for key, val in metrics.items():
                full_path = partial_path + key
                self._publish(key, val, full_path, host, raw_data['timestamp'])

        _file.close()

        if str_to_bool(self.config['truncate']):
            os.remove(filename)

    def _publish(self, name, value, path, host, timestamp):
        """Copied from the diamond.collector.Collector publish method; modified
        to handle custom hosts, paths, and timestamps."""
        if self.config['metrics_whitelist']:
            if not self.config['metrics_whitelist'].match(name):
                return
        elif self.config['metrics_blacklist']:
            if self.config['metrics_blacklist'].match(name):
                return
        ttl = float(self.config['interval']) * float(self.config['ttl_multiplier'])
        metric = Metric(path, value, timestamp=timestamp, host=host, metric_type='GAUGE', ttl=ttl)
        self.publish_metric(metric)
