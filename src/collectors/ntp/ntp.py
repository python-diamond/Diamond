# coding=utf-8

"""
Collect out of band stats from ntp

Uses output from ntpdate:

```
$ ntpdate -q pool.ntp.org
server 12.34.56.1, stratum 2, offset -0.000277, delay 0.02878
server 12.34.56.2, stratum 1, offset -0.000128, delay 0.02896
server 12.34.56.3, stratum 2, offset 0.000613, delay 0.02870
server 12.34.56.4, stratum 2, offset -0.000351, delay 0.02864
31 Apr 12:00:00 ntpdate[12]: adjust time server 12.34.56.2 offset -0.000128 sec
$
```

#### Dependencies

    * /usr/sbin/ntpdate
    * subprocess

"""

import diamond.collector
from diamond import convertor


class NtpCollector(diamond.collector.ProcessCollector):

    def get_default_config_help(self):
        config_help = super(NtpCollector, self).get_default_config_help()
        config_help.update({
            'bin':      'Path to ntpdate binary',
            'ntp_pool': 'NTP Pool address',
            'precision': 'Number of decimal places to report to',
            'time_scale': 'Time unit to report offset in',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(NtpCollector, self).get_default_config()
        config.update({
            'bin':      self.find_binary('/usr/sbin/ntpdate'),
            'ntp_pool': 'pool.ntp.org',
            'path':     'ntp',
            'precision': 0,
            'time_scale': 'milliseconds',
        })
        return config

    def get_ntpdate_stats(self):
        output = self.run_command(['-q', self.config['ntp_pool']])

        data = {'server.count': {'val': 0, 'precision': 0}}

        for line in output[0].splitlines():
            # Only care about best choice not all servers
            if line.startswith('server'):
                data['server.count']['val'] += 1
                continue

            parts = line.split()

            # Make sure we have the correct output
            # Sample of line: 31 Apr 12:00:00 ntpdate[12345]: adjust time \
            #   server 123.456.789.2 offset -0.000123 sec
            if len(parts) != 11:
                self.log.error('NtpCollector: Output of ntpdate was %s words '
                               'long but was expected to be 11' % len(parts))
                self.log.debug('NtpCollector: ntpdate output was %s' % parts)
                continue

            # offset is in seconds, convert is to nanoseconds and miliseconds
            offset_in_s = float(parts[9])

            # Convert to the requested time unit
            offset = convertor.time.convert(offset_in_s,
                                            's',
                                            self.config['time_scale'])

            # Determine metric namespace based on given time unit
            metric_name = 'offset.%s' % self.config['time_scale']

            data[metric_name] = {'val': offset,
                                 'precision': self.config['precision']}

        return data.items()

    def collect(self):
        for stat, v in self.get_ntpdate_stats():
            self.publish(stat, v['val'], precision=v['precision'])
