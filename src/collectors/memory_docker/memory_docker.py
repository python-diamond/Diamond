# coding=utf-8

"""
The MemoryDockerCollector collects memory statistics from docker containers. It
collects identical information as ``MemoryCgroupCollector``. The only
difference is that it replaces the container ids within the ``docker`` path
with container names resolved through the Docker client.

#### Dependencies

 * docker

"""

import os
import sys
from diamond.utils.config import str_to_bool

try:
    import docker
except ImportError:
    docker = None

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'memory_cgroup'))
from memory_cgroup import MemoryCgroupCollector


DOCKER_SUB_STR = 'docker.'
DOCKER_SUB_LEN = len(DOCKER_SUB_STR)


class MemoryDockerCollector(MemoryCgroupCollector):
    def process_config(self):
        super(MemoryDockerCollector, self).process_config()
        self.filter_existing = str_to_bool(self.config['filter_existing'])

    def get_default_config_help(self):
        config_help = super(MemoryDockerCollector, self).get_default_config_help()
        config_help.update(
            filter_existing="If set to 'true', skips publishing information on "
                            "cgroups without an existing container."
        )
        return config_help

    def get_default_config(self):
        config = super(MemoryDockerCollector, self).get_default_config()
        config.update(filter_existing=False)
        return config

    def collect(self):
        if docker is None:
            self.log.error('Unable to import docker')
            return

        self.containers = dict(
            (c['Id'], c['Names'][0][1:])
            for c in docker.Client().containers(all=True)
            if c['Names'] is not None)
        return super(MemoryDockerCollector, self).collect()

    def publish(self, metric_name, *args, **kwargs):
        docker_idx = metric_name.find(DOCKER_SUB_STR)
        if docker_idx >= 0:
            start_idx = docker_idx + DOCKER_SUB_LEN
            dot_idx = metric_name.find('.', start_idx)
            if dot_idx >= start_idx:
                container_id = metric_name[start_idx:dot_idx]
                container_name = self.containers.get(container_id)
                if container_name:
                    new_metric_name = ''.join((metric_name[:start_idx], container_name, metric_name[dot_idx:]))
                    return super(MemoryDockerCollector, self).publish(new_metric_name, *args, **kwargs)
                elif self.filter_existing:
                    return
        return super(MemoryDockerCollector, self).publish(metric_name, *args, **kwargs)
