# coding=utf-8

"""
A Diamond collector that collects memory usage of each process defined in it's
config file by matching them with their executable filepath or the process name.

Example config file ProcessMemoryCollector.conf

```
enabled=True
unit=kB
[process]
[[postgres]]
exe=^\/usr\/lib\/postgresql\/+d.+d\/bin\/postgres$
name=^postgres,^pg
```

exe and name are both lists of comma-separated regexps.
"""

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


class ProcessMemoryCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(ProcessMemoryCollector,
                            self).get_default_config_help()
        config_help.update({
            'unit': 'The unit in which memory data is collected.',
            'process': ("A subcategory of settings inside of which each "
                        "collected process has it's configuration")
        })
        return config_help

    def get_default_config(self):
        """
        Default settings are:
            path: 'memory.process'
            unit: 'B'
        """
        config = super(ProcessMemoryCollector, self).get_default_config()
        config.update({
            'path': 'memory.process',
            'unit': 'B',
            'process': '',
        })
        return config

    def setup_config(self):
        """
        prepare self.processes, which is a descriptor dictionary in
        processgroup --> {
            exe: [regex],
            name: [regex],
            cmdline: [regex],
            procs: [psutil.Process]
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
            self.processes[process] = proc

    def filter_processes(self):
        """
        Populates self.processes[processname]['procs'] with the corresponding
        list of psutil.Process instances
        """

        for proc in psutil.process_iter():
            # filter and divide the system processes amongst the different
            #  process groups defined in the config file
            for procname, cfg in self.processes.items():
                if process_filter(proc, cfg):
                    cfg['procs'].append(proc)
                    break

    def collect(self):
        """
        Collects the RSS memory usage of each process defined under the
        `process` subsection of the config file
        """
        self.setup_config()
        self.filter_processes()
        unit = self.config['unit']
        for process, cfg in self.processes.items():
            # finally publish the results for each process group
            metric_name = "%s.rss" % process
            metric_value = diamond.convertor.binary.convert(
                sum(p.get_memory_info().rss for p in cfg['procs']),
                oldUnit='byte', newUnit=unit)
            # Publish Metric
            self.publish(metric_name, metric_value)

            metric_name = "%s.vms" % process
            metric_value = diamond.convertor.binary.convert(
                sum(p.get_memory_info().vms for p in cfg['procs']),
                oldUnit='byte', newUnit=unit)
            # Publish Metric
            self.publish(metric_name, metric_value)
