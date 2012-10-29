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
