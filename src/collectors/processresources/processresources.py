# coding=utf-8

"""
A Diamond collector that collects memory usage of each process defined in it's
config file by matching them with their executable filepath or the process name.
This collector can also be used to collect memory usage for the Diamond process.

Example config file ProcessResourcesCollector.conf

```
enabled=True
unit=B
cpu_interval=0.1
[process]
[[postgres]]
exe=^\/usr\/lib\/postgresql\/+d.+d\/bin\/postgres$
name=^postgres,^pg

[[diamond]]
selfmon=True
```

exe and name are both lists of comma-separated regexps.

count_workers defined under [process] will determine whether to count how many
workers are there of processes which match this [process],
for example: cgi workers.

cpu_interval is the interval in seconds used to calculate cpu usage percentage.
From psutil's docs:

'''get_cpu_percent(interval=0.1)'''
Return a float representing the process CPU utilization as a percentage.
* When interval is > 0.0 compares process times to system CPU times elapsed
    before and after the interval (blocking).
* When interval is 0.0 compares process times to system CPU times
    elapsed since last call, returning immediately. In this case is recommended
    for accuracy that this function be called with at least 0.1 seconds between
    calls.
"""

import os
import re

import diamond.collector
import diamond.convertor

try:
    import psutil
    psutil
except ImportError:
    psutil = None


def process_filter(proc, cfg):
    """
    Decides whether a process matches with a given process descriptor

    :param proc: a psutil.Process instance
    :param cfg: the dictionary from processes that describes with the
        process group we're testing for
    :return: True if it matches
    :rtype: bool
    """
    if cfg['selfmon'] and proc.pid == os.getpid():
        return True
    for exe in cfg['exe']:
        try:
            if exe.search(proc.exe):
                return True
        except psutil.AccessDenied:
            break
    for name in cfg['name']:
        if name.search(proc.name):
            return True
    for cmdline in cfg['cmdline']:
        if cmdline.search(' '.join(proc.cmdline)):
            return True
    return False


class ProcessResourcesCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(ProcessResourcesCollector,
                            self).get_default_config_help()
        config_help.update({
            'unit': 'The unit in which memory data is collected.',
            'process': ("A subcategory of settings inside of which each "
                        "collected process has it's configuration"),
            'cpu_interval': (
                """The time interval used to calculate cpu percentage
* When interval is > 0.0 compares process times to system CPU times elapsed
before and after the interval (blocking).
* When interval is 0.0 compares process times to system CPU times
elapsed since last call, returning immediately. In this case is recommended
for accuracy that this function be called with at least 0.1 seconds between
calls."""),
        })
        return config_help

    def get_default_config(self):
        """
        Default settings are:
            path: 'memory.process'
            unit: 'B'
        """
        config = super(ProcessResourcesCollector, self).get_default_config()
        config.update({
            'path': 'memory.process',
            'unit': 'B',
            'process': '',
            'cpu_interval': 0.0
        })
        return config

    def setup_config(self):
        """
        prepare self.processes, which is a descriptor dictionary in
        processgroup --> {
            exe: [regex],
            name: [regex],
            cmdline: [regex],
            selfmon: [boolean],
            procs: [psutil.Process],
            count_workers: [boolean]
        }
        """
        self.processes = {}
        for process, cfg in self.config['process'].items():
            # first we build a dictionary with the process aliases and the
            #  matching regexps
            proc = {'procs': []}
            for key in ('exe', 'name', 'cmdline'):
                proc[key] = cfg.get(key, [])
                if not isinstance(proc[key], list):
                    proc[key] = [proc[key]]
                proc[key] = [re.compile(e) for e in proc[key]]
            proc['selfmon'] = cfg.get('selfmon', '').lower() == 'true'
            proc['count_workers'] = cfg.get(
                'count_workers', '').lower() == 'true'
            self.processes[process] = proc

    def filter_processes(self):
        """
        Populates self.processes[processname]['procs'] with the corresponding
        list of psutil.Process instances
        """
        class ProcessResources(object):
            def __init__(self, **kwargs):
                for name, val in kwargs.items():
                    setattr(self, name, val)
        # requires setup_config to be run before this
        interval = float(self.config['cpu_interval'])
        for proc in psutil.process_iter():
            # get process data
            loaded = None
            try:
                proc_dummy = ProcessResources(
                    rss=proc.get_memory_info().rss,
                    vms=proc.get_memory_info().vms,
                    cpu_percent=proc.get_cpu_percent(interval=interval)
                )
                loaded = True
            except psutil.NoSuchProcess:
                loaded = False

            if loaded:
                # filter and divide the system processes amongst the different
                #  process groups defined in the config file
                for procname, cfg in self.processes.items():
                    if process_filter(proc, cfg):
                        cfg['procs'].append(proc_dummy)
                        break

    def collect(self):
        """
        Collects the RSS memory usage of each process defined under the
        `process` subsection of the config file
        """
        if not psutil:
            self.log.error('Unable to import psutil')
            self.log.error('No process resource metrics retrieved')
            return None

        try:
            self.setup_config()
            self.filter_processes()
            unit = self.config['unit']
            for process, cfg in self.processes.items():
                # finally publish the results for each process group
                metric_name = "%s.rss" % process
                metric_value = diamond.convertor.binary.convert(
                    sum(p.rss for p in cfg['procs']),
                    oldUnit='byte', newUnit=unit)
                # Publish Metric
                self.publish(metric_name, metric_value)

                metric_name = "%s.vms" % process
                metric_value = diamond.convertor.binary.convert(
                    sum(p.vms for p in cfg['procs']),
                    oldUnit='byte', newUnit=unit)
                # Publish Metric
                self.publish(metric_name, metric_value)

                # CPU percent
                metric_name = "%s.cpu_percent" % process
                metric_value = sum(p.cpu_percent for p in cfg['procs'])
                # Publish Metric
                self.publish(metric_name, metric_value)

                if cfg['count_workers']:
                    metric_name = '%s.workers' % process
                    metric_value = len(cfg['procs'])
                    self.publish(metric_name, metric_value)
        except Exception, e:
            self.log.error(str(e))
