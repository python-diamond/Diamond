# coding=utf-8

"""
Collects Mesos Task cgroup statistics. Because Mesos Tasks
only tangentially relate to the host they are running on,
this collector uses task 'source' information to build the
naming path. The prefix is overridden in the collector to
place metrics in the graphite tree at the root under
`mesos.tasks`. The container ID contained within the
source string will serve as the container uniqueifier.

If your scheduler (this was written against a Mesos cluster
    being scheduled by Aurora) does not include uniqueifing
information in the task data under `frameworks.executors.source`,
you're going to have a bad time.

#### Example Configuration

```
    host = localhost
    port = 5051
```
"""

import diamond.collector
import json
import urllib2
import os


class MesosCGroupCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(MesosCGroupCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': 'Hostname',
            'port': 'Port'
        })
        return config_help

    def get_default_config(self):
        # https://github.com/BrightcoveOS/Diamond/blob/master/src/diamond/collector.py#L312-L358
        config = super(MesosCGroupCollector, self).get_default_config()
        config.update({
            'mesos_state_path': 'state.json',
            'cgroup_fs_path': '/sys/fs/cgroup',
            'host': 'localhost',
            'port': 5051,
            'path_prefix': 'mesos',
            'path': 'tasks',
            'hostname': None
        })
        return config

    def __init__(self, *args, **kwargs):
        super(MesosCGroupCollector, self).__init__(*args, **kwargs)

    def collect(self):
        containers = self.get_containers()

        sysfs = containers['flags']['cgroups_hierarchy']
        cgroup_root = containers['flags']['cgroups_root']

        for aspect in ['cpuacct', 'cpu', 'memory']:
            aspect_path = os.path.join(sysfs, aspect, cgroup_root)

            contents = os.listdir(aspect_path)
            for task_id in [entry for entry in contents if
                            os.path.isdir(os.path.join(aspect_path, entry))]:

                if task_id not in containers:
                    continue

                key_parts = [containers[task_id]['environment'],
                             containers[task_id]['role'],
                             containers[task_id]['task'],
                             containers[task_id]['id'],
                             aspect]

                # list task_id items
                task_id = os.path.join(aspect_path, task_id)

                with open(os.path.join(task_id, "%s.stat" % aspect)) as f:
                    data = f.readlines()

                    for kv_pair in data:
                        key, value = kv_pair.split()
                        self.publish(
                            self.clean_up(
                                '.'.join(key_parts + [key])), value)

    def get_containers(self):
        state = self.get_mesos_state()

        containers = {
            'flags': state['flags']
        }

        if 'frameworks' in state:
            for framework in state['frameworks']:
                for executor in framework['executors']:
                    container = executor['container']
                    source = executor['source']
                    role, environment, task, number = source.split('.')

                    containers[container] = {'role': role,
                                             'environment': environment,
                                             'task': task,
                                             'id': number
                                             }

        return containers

    def get_mesos_state(self):
        try:
            url = "http://%s:%s/%s" % (self.config['host'],
                                       self.config['port'],
                                       self.config['mesos_state_path'])

            return json.load(urllib2.urlopen(url))
        except (urllib2.HTTPError, ValueError), err:
            self.log.error('Unable to read JSON response: %s' % err)
            return {}

    def clean_up(self, text):
        return text.replace('/', '.')
