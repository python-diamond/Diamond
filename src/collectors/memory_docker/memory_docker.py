# coding=utf-8

"""
The MemoryDockerCollector collects memory statistics from docker containers.
It collects identical information as ``MemoryCgroupCollector``. The only
difference is that it replaces container ids within ``docker`` paths
with container names resolved through the Docker client.

Docker metrics with ids that do not exist can be filtered out. Ids of
containers that exist but have no name are always published.

More recent versions of Docker create cgroups starting with ``docker-``.
In that case the metrics are renamed to start with ``docker.``

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


DOCKER_SUB_STR = 'docker'
DOCKER_SUB_LEN = len(DOCKER_SUB_STR)


def _parse_metric_name(metric_name):
    docker_idx = metric_name.find(DOCKER_SUB_STR)
    if 0 <= docker_idx < len(metric_name):
        start_idx = docker_idx + DOCKER_SUB_LEN + 1
        sep = metric_name[start_idx - 1]
        if sep in ('.', '-'):
            dot_idx = metric_name.find('.', start_idx)
            if dot_idx >= start_idx:
                container_id = metric_name[start_idx:dot_idx]
                if container_id != 'service':
                    return container_id, sep, start_idx, dot_idx
    return None


def _get_container_name(container_names):
    if container_names:
        for c_name in container_names:
            if c_name.find('/', 1) == -1:
                return c_name[1:]
        return container_names[0][1:]
    return ''


class MemoryDockerCollector(MemoryCgroupCollector):
    def process_config(self):
        super(MemoryDockerCollector, self).process_config()
        self.filter_existing = str_to_bool(self.config['filter_existing'])
        trunc = self.config['truncate_ids']
        try:
            self.truncate_ids = int(trunc)
        except (TypeError, ValueError):
            self.truncate_ids = 0
        self.docker_url = self.config['docker_base_url']
        self.docker_version = self.config['docker_version']

    def get_default_config_help(self):
        config_help = super(
            MemoryDockerCollector, self).get_default_config_help()
        config_help.update(
            filter_existing="If set to 'true', skips publishing information "
                            "on cgroups without an existing container.",
            truncate_ids="Length to truncate ids of non-existing containers "
                         "and containers without a name. If set to equal to "
                         "or lower than zero, metric names are not changed "
                         "in length.",
            docker_url="URL to the Docker service. Not required, if Docker "
                       "is running with its default configuration.",
            docker_version="Docker service API version. The default, 'auto', "
                           "will sets the required version automatically."
        )
        return config_help

    def get_default_config(self):
        config = super(MemoryDockerCollector, self).get_default_config()
        config.update(filter_existing=False)
        config.update(truncate_ids=0)
        config.update(docker_base_url=None)
        config.update(docker_version='auto')
        return config

    def collect(self):
        if docker is None:
            self.log.error('Unable to import docker')
            return
        if not hasattr(self, 'docker_client'):
            self.docker_client = docker.Client(base_url=self.docker_url, version=self.docker_version)

        self.containers = {
            c['Id']: _get_container_name(c['Names'])
            for c in self.docker_client.containers(all=True)
        }
        return super(MemoryDockerCollector, self).collect()

    def publish(self, metric_name, *args, **kwargs):
        docker_metric = _parse_metric_name(metric_name)
        if docker_metric:
            container_id, sep, start_idx, end_idx = docker_metric
            container_name = self.containers.get(container_id)
            if container_name:
                new_metric_name = '{0}.{1}{2}'.format(
                    metric_name[:start_idx - 1],
                    container_name,
                    metric_name[end_idx:])
            elif container_name is None and self.filter_existing:
                self.log.debug(
                    "Skipping id '%s' (not an existing Docker container)."
                    % container_id)
                return
            elif self.truncate_ids > 0:
                new_metric_name = '{0}.{1}{2}'.format(
                    metric_name[:start_idx - 1],
                    container_id[:self.truncate_ids],
                    metric_name[end_idx:])
            elif sep != '.':
                new_metric_name = '{0}.{1}'.format(
                    metric_name[:start_idx - 1],
                    metric_name[start_idx:])
            else:
                new_metric_name = metric_name
        else:
            new_metric_name = metric_name
        return super(MemoryDockerCollector, self).publish(new_metric_name,
                                                          *args,
                                                          **kwargs)
