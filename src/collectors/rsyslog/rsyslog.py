# coding=utf-8

"""
Collects stats from rsyslog server with impstats module loaded
Impstats formats are json/json-elasticsearch/cee/legacy, but
only json and legacy formats are supported

#### Dependencies
 * Rsyslog Plugin – impstats (rsyslog 7.5.3+)
   (http://www.rsyslog.com/rsyslog-statistic-counter-plugin-impstats/)
   (http://www.rsyslog.com/doc/v8-stable/configuration/modules/impstats.html)

#### Metrics
 * [Rsyslog statistic counter ]
   (http://www.rsyslog.com/rsyslog-statistic-counter/)
"""

from collections import deque
import re
import diamond.collector
import socket
import time
import json


class RsyslogCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(RsyslogCollector, self).get_default_config_help()
        config_help.update({
            'pstats_path': "Path to get syslog stats.",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the RsyslogCollector settings
        """
        config = super(RsyslogCollector, self).get_default_config()
        config.update({
            'pstats_path':     '/var/log/rsyslog_stats.log',
            'path':           'rsyslog'
        })
        return config

    def _get_summary(self):
        count = 0
        with open(self.config['pstats_path']) as f:
            for line in reversed(f.readlines()):
                if "global" in line.rstrip():
                    if count > 1:
                        break
                    count += 1
                elif count > 0:
                    count += 1
            f.seek(0)
            summary_fp = deque(f, count)
        return summary_fp

    def legacyformat(self, stat_lines):
        self.rsyslog_stats = []
        for line in stat_lines:
            metrics = {}
            parsed = line.split(': ', 2)
            if parsed[1].count("(") > 0:
                name = re.sub(r"(^im[ut][dc]p)\(\*?\:?(\d?[\d|\w]?\d)\)",
                              r'\1_\2', parsed[1])
            else:
                name = parsed[1].replace(' ', '_')
            _metrics = parsed[2].split(' ', -1)
            metrics.update({"name": name})
            for m in _metrics:
                if "\n" not in m:
                    metrics.update({m.split('=', 1)[0]: m.split('=', 1)[1]})
            self.rsyslog_stats.append(metrics)
        return self.rsyslog_stats

    def jsonformat(self, stat_lines):
        self.rsyslog_stats = []
        for line in stat_lines:
            parsed = line.split('rsyslogd-pstats: ', 2)
            parsed = json.loads(parsed[1])
            if parsed['name'].count("(") > 0:
                parsed['name'] = re.sub(
                    r"(^im[ut][dc]p)\(\*?\:?(\d?[\d|\w]?\d)\)",
                    r'\1_\2', parsed['name']
                )
            else:
                parsed['name'] = parsed['name'].replace(' ', '_')
            self.rsyslog_stats.append(parsed)
        return self.rsyslog_stats

    def is_json(self, str):
        try:
            json_object = json.loads(str)
        except ValueError, e:
            return False
        return True

    def collect(self):
        legacy_format = False
        stats = self._get_summary()
        for line in stats:
            parsed = line.split('rsyslogd-pstats: ', 2)
            if self.is_json(parsed[1]):
                rsyslog_stats = self.jsonformat(stats)
            else:
                rsyslog_stats = self.legacyformat(stats)
                legacy_format = True
            break
        for metrics in self.rsyslog_stats:
            metric_prefix = metrics['name']
            for k in metrics:
                if k != 'origin' and k != 'name':
                    metric_name = metric_prefix + '.' + k
                    metric_value = metrics[k]
                    if legacy_format is True:
                        self.publish(metric_name, metric_value)
                    else:
                        if isinstance(metric_value, int):
                            self.publish(metric_name, metric_value)
