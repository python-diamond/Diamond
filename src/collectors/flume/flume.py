# coding=utf-8

"""
Collect statistics from Flume

#### Dependencies

 * urllib2
 * json or simplejson

"""

import urllib2
import diamond.collector

try:
    import simplejson as json
except ImportError:
    import json


class FlumeCollector(diamond.collector.Collector):

    # items to collect
    _metrics_collect = {
        'CHANNEL': [
            'ChannelFillPercentage',
            'EventPutAttemptCount',
            'EventPutSuccessCount',
            'EventTakeAttemptCount',
            'EventTakeSuccessCount'
        ],
        'SINK': [
            'BatchCompleteCount',
            'BatchEmptyCount',
            'BatchUnderflowCount',
            'ConnectionClosedCount',
            'ConnectionCreatedCount',
            'ConnectionFailedCount',
            'EventDrainAttemptCount',
            'EventDrainSuccessCount'
        ],
        'SOURCE': [
            'AppendAcceptedCount',
            'AppendBatchAcceptedCount',
            'AppendBatchReceivedCount',
            'AppendReceivedCount',
            'EventAcceptedCount',
            'EventReceivedCount',
            'OpenConnectionCount'
        ]
    }

    def get_default_config_help(self):
        config_help = super(FlumeCollector, self).get_default_config_help()
        config_help.update({
            'req_host': 'Hostname',
            'req_port': 'Port',
            'req_path': 'Path',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        default_config = super(FlumeCollector, self).get_default_config()
        default_config['path'] = 'flume'
        default_config['req_host'] = 'localhost'
        default_config['req_port'] = 41414
        default_config['req_path'] = '/metrics'
        return default_config

    def collect(self):
        url = 'http://{0}:{1}{2}'.format(
            self.config['req_host'],
            self.config['req_port'],
            self.config['req_path']
        )

        try:
            resp = urllib2.urlopen(url)
            try:
                j = json.loads(resp.read())
                resp.close()
            except Exception, e:
                resp.close()
                self.log.error('Cannot load json data: %s', e)
                return None
        except urllib2.URLError, e:
            self.log.error('Failed to open url: %s', e)
            return None
        except Exception, e:
            self.log.error('Unknown error opening url: %s', e)
            return None

        for comp in j.iteritems():
            comp_name = comp[0]
            comp_items = comp[1]
            comp_type = comp_items['Type']

            for item in self._metrics_collect[comp_type]:
                if item.endswith('Count'):
                    metric_name = '{0}.{1}'.format(comp_name, item[:-5])
                    metric_value = int(comp_items[item])
                    self.publish_counter(metric_name, metric_value)
                elif item.endswith('Percentage'):
                    metric_name = '{0}.{1}'.format(comp_name, item)
                    metric_value = float(comp_items[item])
                    self.publish_gauge(metric_name, metric_value)
                else:
                    metric_name = item
                    metric_value = int(comp_items[item])
                    self.publish_gauge(metric_name, metric_value)
