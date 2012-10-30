# coding=utf-8

"""
A Diamond collector that collects memory usage of each process defined in it's
config file by matching them with their executable filepath or the process name.

Example config file ProcessMemoryCollector.conf

```
enabled=True
[process]
[[postgres]]
exe=^\/usr\/lib\/postgresql\/+d.+d\/bin\/postgres$
name=^postgres,^pg
```

exe and name are both lists of comma-separated regexps.
"""
import re

import diamond.collector, diamond.convertor
import psutil

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
            procs: [psutil.Process]
            }
        """
        self.processes = {}
        for process, cfg in self.config['process'].items():
            # first we build a dictionary with the process aliases and the
            #  matching regexps
            exe = cfg.get('exe', [])
            if not isinstance(exe, list):
                exe = [exe]
            exe = [re.compile(e) for e in exe]
            name = cfg.get('name', [])
            if not isinstance(name, list):
                name = [name]
            name = [re.compile(n) for n in name]
            self.processes[process] = {
                'exe': exe,
                'name': name,
                'procs': []
            }

    def filter_processes(self):
        def process_filter(proc, cfg):
            """
            Decides whether a process matches with a given process descriptor

            @param proc: a psutil.Process instance
            @param cfg: the dictionary from processes that describes with the
                process group we're testing for
            @return: True|False
            """
            for exe in cfg['exe']:
                try:
                    if exe.match(proc.exe):
                        return True
                except psutil.AccessDenied:
                    break
            for name in cfg['name']:
                if name.match(proc.name):
                    return True
            return False

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
            metric_name = process
            metric_value = diamond.convertor.binary.convert(
                sum(p.get_memory_info().rss for p in cfg['procs']),
                oldUnit='byte', newUnit=unit)
            # Publish Metric
            self.publish(metric_name, metric_value)
