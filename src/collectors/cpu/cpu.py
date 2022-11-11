# coding=utf-8

"""
The CPUCollector collects CPU utilization metric using /proc/stat.

#### Dependencies

 * /proc/stat

"""

import diamond.collector
import os
import time
from diamond.collector import str_to_bool

try:
    import psutil
except ImportError:
    psutil = None


class CPUCollector(diamond.collector.Collector):

    PROC = '/proc/stat'
    INTERVAL = 1

    MAX_VALUES = {
        'user': diamond.collector.MAX_COUNTER,
        'nice': diamond.collector.MAX_COUNTER,
        'system': diamond.collector.MAX_COUNTER,
        'idle': diamond.collector.MAX_COUNTER,
        'iowait': diamond.collector.MAX_COUNTER,
        'irq': diamond.collector.MAX_COUNTER,
        'softirq': diamond.collector.MAX_COUNTER,
        'steal': diamond.collector.MAX_COUNTER,
        'guest': diamond.collector.MAX_COUNTER,
        'guest_nice': diamond.collector.MAX_COUNTER,
    }

    def get_default_config_help(self):
        config_help = super(CPUCollector, self).get_default_config_help()
        config_help.update({
            'percore':  'Collect metrics per cpu core or just total',
            'simple':   'only return aggregate CPU% metric',
            'extended':  'return aggregate CPU% metric and complex CPU metrics',
            'normalize': 'for cpu totals, divide by the number of CPUs',
            'derivative': 'use derivative values for metrics',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(CPUCollector, self).get_default_config()
        config.update({
            'path':     'cpu',
            'percore':  'True',
            'xenfix':   None,
            'simple':   'False',
            'extended':  'False',
            'normalize': 'False',
            'derivative': 'True',
        })
        return config

    def collect(self):
        """
        Collector cpu stats
        """

        def cpu_time_list():
            """
            get cpu time list
            """

            statFile = open(self.PROC, "r")
            timeList = statFile.readline().split(" ")[2:6]
            for i in range(len(timeList)):
                timeList[i] = int(timeList[i])
            statFile.close()
            return timeList

        def cpu_delta_time(interval):
            """
            Get before and after cpu times for usage calc
            """
            pre_check = cpu_time_list()
            time.sleep(interval)
            post_check = cpu_time_list()
            for i in range(len(pre_check)):
                post_check[i] -= pre_check[i]
            return post_check

        use_derivative = str_to_bool(self.config['derivative'])
        use_normalization = str_to_bool(self.config['normalize'])
        metrics = {}

        if os.access(self.PROC, os.R_OK):

            # If simple only return aggregate CPU% metric, unless extended is
            # set (in which case return both)
            if str_to_bool(self.config['simple']) or \
                    str_to_bool(self.config['extended']):
                dt = cpu_delta_time(self.INTERVAL)
                cpuPct = 100 - (dt[len(dt) - 1] * 100.00 / sum(dt))
                self.publish('percent', str('%.4f' % cpuPct))
                # Only return simple metrics, unless the `extended` flag is set
                if not str_to_bool(self.config['extended']):
                    return True

            results = {}
            # Open file
            file = open(self.PROC)

            ncpus = -1  # dont want to count the 'cpu'(total) cpu.
            for line in file:
                if not line.startswith('cpu'):
                    continue

                ncpus += 1
                elements = line.split()

                cpu = elements[0]

                if cpu == 'cpu':
                    cpu = 'total'
                elif not str_to_bool(self.config['percore']):
                    continue

                results[cpu] = {}

                if len(elements) >= 2:
                    results[cpu]['user'] = elements[1]
                if len(elements) >= 3:
                    results[cpu]['nice'] = elements[2]
                if len(elements) >= 4:
                    results[cpu]['system'] = elements[3]
                if len(elements) >= 5:
                    results[cpu]['idle'] = elements[4]
                if len(elements) >= 6:
                    results[cpu]['iowait'] = elements[5]
                if len(elements) >= 7:
                    results[cpu]['irq'] = elements[6]
                if len(elements) >= 8:
                    results[cpu]['softirq'] = elements[7]
                if len(elements) >= 9:
                    results[cpu]['steal'] = elements[8]
                if len(elements) >= 10:
                    results[cpu]['guest'] = elements[9]
                if len(elements) >= 11:
                    results[cpu]['guest_nice'] = elements[10]

            # Close File
            file.close()

            metrics['cpu_count'] = ncpus

            for cpu in results.keys():
                stats = results[cpu]
                for s in stats.keys():
                    # Get Metric Name
                    metric_name = '.'.join([cpu, s])
                    # Get actual data
                    div = 1
                    if use_normalization and cpu == 'total' and ncpus > 0:
                        div = ncpus
                    if use_derivative:
                        metrics[metric_name] = self.derivative(
                            metric_name,
                            long(stats[s]),
                            self.MAX_VALUES[s]) / div
                    else:
                        metrics[metric_name] = long(stats[s]) / div

            # Check for a bug in xen where the idle time is doubled for guest
            # See https://bugzilla.redhat.com/show_bug.cgi?id=624756
            if self.config['xenfix'] is None or self.config['xenfix'] is True:
                if os.path.isdir('/proc/xen'):
                    total = 0
                    for metric_name in metrics.keys():
                        if 'cpu0.' in metric_name:
                            total += int(metrics[metric_name])
                    if total > 110:
                        self.config['xenfix'] = True
                        for mname in metrics.keys():
                            if '.idle' in mname:
                                metrics[mname] = float(metrics[mname]) / 2
                    elif total > 0:
                        self.config['xenfix'] = False
                else:
                    self.config['xenfix'] = False

        else:
            if not psutil:
                self.log.error('Unable to import psutil')
                self.log.error('No cpu metrics retrieved')
                return None

            cpu_time = psutil.cpu_times(True)
            cpu_count = len(cpu_time)
            total_time = psutil.cpu_times()

            metrics['cpu_count'] = cpu_count

            if str_to_bool(self.config['percore']):
                for i in range(0, len(cpu_time)):
                    cpu = 'cpu' + str(i)
                    if use_derivative:
                        metrics[cpu + '.user'] = self.derivative(
                            cpu + '.user',
                            long(cpu_time[i].user),
                            self.MAX_VALUES['user'])
                        metrics[cpu + '.system'] = self.derivative(
                            cpu + '.system',
                            long(cpu_time[i].system),
                            self.MAX_VALUES['system'])
                        metrics[cpu + '.idle'] = self.derivative(
                            cpu + '.idle',
                            long(cpu_time[i].idle),
                            self.MAX_VALUES['idle'])
                        if hasattr(cpu_time[i], 'nice'):
                            metrics[cpu + '.nice'] = self.derivative(
                                cpu + '.nice',
                                long(cpu_time[i].nice),
                                self.MAX_VALUES['nice'])

                    else:
                        metrics[cpu + '.user'] = long(cpu_time[i].user)
                        metrics[cpu + '.system'] = long(cpu_time[i].system)
                        metrics[cpu + '.idle'] = long(cpu_time[i].idle)
                        if hasattr(cpu_time[i], 'nice'):
                            metrics[cpu + '.nice'] = long(cpu_time[i].nice)

            div = 1
            if use_normalization and cpu_count > 0:
                div = cpu_count

            if use_derivative:
                metrics['total.user'] = self.derivative(
                    'total.user',
                    long(total_time.user),
                    self.MAX_VALUES['user']) / div
                metrics['total.system'] = self.derivative(
                    'total.system',
                    long(total_time.system),
                    self.MAX_VALUES['system']) / div
                metrics['total.idle'] = self.derivative(
                    'total.idle',
                    long(total_time.idle),
                    self.MAX_VALUES['idle']) / div
                if hasattr(total_time, 'nice'):
                    metrics['total.nice'] = self.derivative(
                        'total.nice',
                        long(total_time.nice),
                        self.MAX_VALUES['nice']) / div
            else:
                metrics['total.user'] = long(total_time.user) / div
                metrics['total.system'] = long(total_time.system) / div
                metrics['total.idle'] = long(total_time.idle) / div
                if hasattr(total_time, 'nice'):
                    metrics['total.nice'] = long(total_time.nice) / div

        # Publish Metric
        for metric_name in metrics.keys():
            self.publish(metric_name,
                         metrics[metric_name],
                         precision=2)
        return True
