# coding=utf-8

"""
The MemoryDockerCollector collects memory statistics from docker containers

#### Dependencies

 * docker

"""

import os
import sys

try:
    import docker
except ImportError:
    docker = None

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'memory_cgroup'))
from memory_cgroup import MemoryCgroupCollector


class MemoryDockerCollector(MemoryCgroupCollector):

    def collect(self):
        if docker is None:
            self.log.error('Unable to import docker')
            return

        self.containers = dict(
            (c['Id'], c['Names'][0][1:])
            for c in docker.Client().containers(all=True)
            if c['Names'] is not None)
        return super(MemoryDockerCollector, self).collect()

    def publish(self, metric_name, value, metric_type):
        for container_id, container_name in self.containers.items():
            metric_name = metric_name.replace(
                'docker.' + container_id + '.',
                'docker.' + container_name + '.')
        return super(MemoryDockerCollector, self).publish(
            metric_name, value, metric_type)
