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


def match_process(pid, name, cmdline, exe, cfg):
    """
    Decides whether a process matches with a given process descriptor

    :param pid: process pid
    :param exe: process executable
    :param name: process name
    :param cmdline: process cmdline
    :param cfg: the dictionary from processes that describes with the
        process group we're testing for
    :return: True if it matches
    :rtype: bool
    """
    if cfg['selfmon'] and pid == os.getpid():
        return True
    for exe_re in cfg['exe']:
        if exe_re.search(exe):
            return True
    for name_re in cfg['name']:
        if name_re.search(name):
            return True
    for cmdline_re in cfg['cmdline']:
        if cmdline_re.search(' '.join(cmdline)):
            return True
    return False


def process_info(process, info_keys):
    results = {}
    process_info = process.as_dict()
    metrics = ((key, process_info.get(key, None)) for key in info_keys)
    for key, value in metrics:
        if type(value) in [float, int]:
            results.update({key: value})
        elif hasattr(value, '_asdict'):
            for subkey, subvalue in value._asdict().iteritems():
                results.update({"%s.%s" % (key, subkey): subvalue})
    return results


def get_value(process, name):
    result = getattr(process, name)
    try:
        return result()
    except TypeError:
        return result


class ProcessResourcesCollector(diamond.collector.Collector):
    def process_config(self):
        """
        prepare self.processes, which is a descriptor dictionary in
        pg_name: {
            exe: [regex],
            name: [regex],
            cmdline: [regex],
            selfmon: [boolean],
            procs: [psutil.Process],
            count_workers: [boolean]
        }
        """
        self.processes = {}
        self.processes_info = {}
        for pg_name, cfg in self.config['process'].items():
            pg_cfg = {}
            for key in ('exe', 'name', 'cmdline'):
                pg_cfg[key] = cfg.get(key, [])
                if not isinstance(pg_cfg[key], list):
                    pg_cfg[key] = [pg_cfg[key]]
                pg_cfg[key] = [re.compile(e) for e in pg_cfg[key]]
            pg_cfg['selfmon'] = cfg.get('selfmon', '').lower() == 'true'
            pg_cfg['count_workers'] = cfg.get(
                'count_workers', '').lower() == 'true'
            self.processes[pg_name] = pg_cfg
            self.processes_info[pg_name] = {}

    def get_default_config_help(self):
        config_help = super(ProcessResourcesCollector,
                            self).get_default_config_help()
        config_help.update({
            'unit': 'The unit in which memory data is collected.',
            'process': ("A subcategory of settings inside of which each "
                        "collected process has it's configuration"),
        })
        return config_help

    def get_default_config(self):
        """
        Default settings are:
            path: 'process'
            unit: 'B'
        """
        config = super(ProcessResourcesCollector, self).get_default_config()
        config.update({
            'path': 'process',
            'unit': 'B',
            'process': {},
        })
        return config

    default_info_keys = [
        'num_ctx_switches',
        'cpu_percent',
        'cpu_times',
        'io_counters',
        'num_threads',
        'memory_percent',
        'ext_memory_info',
    ]

    def save_process_info(self, pg_name, process_info):
        for key, value in process_info.iteritems():
            if key in self.processes_info[pg_name]:
                self.processes_info[pg_name][key] += value
            else:
                self.processes_info[pg_name][key] = value

    def collect_process_info(self, process):
        try:
            pid = get_value(process, 'pid')
            name = get_value(process, 'name')
            cmdline = get_value(process, 'cmdline')
            try:
                exe = get_value(process, 'exe')
            except psutil.AccessDenied:
                exe = ""
            for pg_name, cfg in self.processes.items():
                if match_process(pid, name, cmdline, exe, cfg):
                    pi = process_info(process, self.default_info_keys)
                    if cfg['count_workers']:
                        pi.update({'workers_count': 1})
                    self.save_process_info(pg_name, pi)
        except psutil.NoSuchProcess, e:
            self.log.info("Process exited while trying to get info: %s", e)

    def collect(self):
        """
        Collects resources usage of each process defined under the
        `process` subsection of the config file
        """
        if not psutil:
            self.log.error('Unable to import psutil')
            self.log.error('No process resource metrics retrieved')
            return None

        for process in psutil.process_iter():
            self.collect_process_info(process)

        # publish results
        for pg_name, counters in self.processes_info.iteritems():
            metrics = (
                ("%s.%s" % (pg_name, key), value)
                for key, value in counters.iteritems())
            [self.publish(*metric) for metric in metrics]
            # reinitialize process info
            self.processes_info[pg_name] = {}
