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

import diamond.collector
import psutil

class ProcessMemoryCollector(diamond.collector.Collector):
    UNIT_MAPPING = {
        'b': 0,
        'kb': 10,
        'mb': 20,
        'gb': 30,
        }

    def get_default_config_help(self):
        config_help = super(ProcessMemoryCollector,
                            self).get_default_config_help()
        config_help.update({
            'unit': ('The unit in which memory data is collected.'
                     'Can be one of b, kb, mb, gb'),
            'process': ("A subcategory of settings inside of which each "
                        "collected process has it's configuration")
        })
        return config_help

    def get_default_config(self):
        config = super(ProcessMemoryCollector, self).get_default_config()
        config.update({
            'path': 'memory.process',
            'unit': 'b',
            'process': '',
            })
        return config

    def collect(self):
        processes = {}
        for process, cfg in self.config['process'].items():
            exe = cfg.get('exe', [])
            if not isinstance(exe, list):
                exe = [exe]
            exe = [re.compile(e) for e in exe]
            name = cfg.get('name', [])
            if not isinstance(name, list):
                name = [name]
            name = [re.compile(n) for n in name]
            processes[process] = {
                'exe': exe,
                'name': name,
                'procs': []
            }

        def process_filter(proc, cfg):
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
            for procname, cfg in processes.items():
                if process_filter(proc, cfg):
                    cfg['procs'].append(proc)
                    break

        for process, cfg in processes.items():
            metric_name = process
            metric_value = (sum(p.get_memory_info().rss for p in cfg['procs'])
                            / (2 ** self.UNIT_MAPPING))
            self.publish(metric_name, metric_value)
