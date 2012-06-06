#
# Diamond collector for Hadoop metrics, see:
#
#  * http://www.cloudera.com/blog/2009/03/hadoop-metrics/

from diamond import *
from diamond.metric import Metric
import diamond.collector
import glob
import re

class HadoopCollector(diamond.collector.Collector):
    """
    Processes Hadoop metrics.
    """

    re_log = re.compile(r'^(?P<timestamp>\d+) (?P<name>\S+): (?P<metrics>.*)$')

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'enabled':  'True',
            'path':     'hadoop',
            'method':   'Threaded',
            'metrics':  ['/var/log/hadoop/*-metrics.out'],
        }

    def collect(self):
        for pattern in self.config['metrics']:
            for filename in glob.glob(pattern):
                self.collect_from(filename)

    def collect_from(self, filename):
        if not os.access(filename, os.R_OK):
            return False

        with open(filename, 'r') as fd:
            for line in fd:
                match = self.re_log.match(line)
                if not match:
                    continue

                data = match.groupdict()
                for metric in data['metrics'].split(','):
                    metric = metric.strip()
                    if '=' in metric:
                        key, value = metric.split('=', 1)
                        try:
                            value = float(value)
                            path = self.get_metric_path('.'.join([
                                data['name'],
                                key,
                            ]))
                            self.publish_metric(Metric(path,
                                value,
                                timestamp=int(data['timestamp'])))

                        except (ValueError):
                            pass
