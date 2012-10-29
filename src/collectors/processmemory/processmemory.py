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

