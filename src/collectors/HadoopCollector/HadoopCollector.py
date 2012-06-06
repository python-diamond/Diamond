#
# Diamond collector for Hadoop metrics, see:
#
#  * http://www.cloudera.com/blog/2009/03/hadoop-metrics/
#
# (c) 2012 Wijnand Modderman-Lenstra <maze@pyth0n.org>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

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
            continue

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
                            self.log.debug('publishing[%s] %s=%s' % (path, key, value))

                        except (ValueError):
                            pass
