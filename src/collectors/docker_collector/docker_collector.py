# coding=utf-8

"""
The DockerCollector gathers some metrics about docker containers and images.

#### Dependencies

* docker -- Install via `pip install docker-py`.
  Source https://github.com/docker/docker-py

#### Config

Options:

* `memory_path` -- The path to the kernel's CGroups memory filesystem.
  The auto-detected default is probably correct.

Example config:

```
enabled=True
```

#### Stats

* `containers_running_count` -- Number of running containers.
* `containers_stopped_count` -- Number of stopped containers.
* `<container-name>/RSS` -- Resident Set Size memory.
* `<container-name>/cache` -- Memory used for caching.
* `<container-name>/swap` -- Swapped memory.
* `<container-name>/pagein_count` -- Number of page faults that bring a
  page into memory.
* `<container-name>/pageout_count` -- Number of page faults that push a
  page out of memory.

"""

from diamond.collector import Collector
import diamond.convertor
import os

try:
    import docker
except ImportError:
    docker = None

# <memory.stat name>: (<metric_name>, <oldUnit if needs converting>)
_KEY_MAPPING = {
    'total_rss':     ('RSS',           'B'),
    'total_cache':   ('cache',         'B'),
    'total_swap':    ('swap',          'B'),
    'total_pgpgin':  ('pagein_count',  None),
    'total_pgpgout': ('pageout_count', None)
}


class DockerCollector(Collector):

    def process_config(self):
        super(DockerCollector, self).process_config()
        self.memory_path = self.config['memory_path']

    def get_default_config_help(self):
        config_help = super(DockerCollector, self).get_default_config_help()
        config_help.update({
            'memory_path': "The path to the kernel's CGroups memory"
            "filesystem. The auto-detected default is probably correct."
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(DockerCollector, self).get_default_config()
        config.update({
            'path':     'docker',
            'memory_path': self._default_memory_path(),
        })
        return config

    def collect(self):
        if docker is None:
            self.log.error('Unable to import docker')
            return False

        try:
            # Collect info
            results = {}
            client = docker.Client(version='auto')

            # Top level stats
            running_containers = client.containers()
            results['containers_running_count'] = (
                len(running_containers), 'GAUGE')

            all_containers = client.containers(all=True)
            results['containers_stopped_count'] = (
                len(all_containers) - len(running_containers), 'GAUGE')

            images_count = len(set(client.images(quiet=True)))
            results['images_count'] = (images_count, 'GAUGE')

            dangling_images_count = len(set(client.images(
                quiet=True, all=True, filters={'dangling': True})))
            results['images_dangling_count'] = (dangling_images_count, 'GAUGE')

            # Collect information
            self._collect_running_containers(running_containers, results)

            # Publish it
            for name in sorted(results.keys()):
                (value, metric_type) = results[name]
                self.publish(name, value, metric_type=metric_type)

            return True
        except Exception, e:
            print e
            self.log.error(e, exc_info=True)
            return False

    def _collect_running_containers(self, containers, results):
        # Per container stats
        for container in containers:
            name = container['Names'][0][1:]
            memory_stats = self._get_memory_stats(container['Id'])
            if memory_stats is None:
                continue

            for (key, value) in memory_stats:
                if key not in _KEY_MAPPING:
                    continue
                (new_key, from_unit) = _KEY_MAPPING[key]

                if from_unit is None:
                    results['.'.join(['containers', name, new_key])] = (
                        value, 'COUNTER')
                else:
                    for unit in self.config['byte_unit']:
                        new_value = diamond.convertor.binary.convert(
                            value=value, oldUnit=from_unit, newUnit=unit)
                        result_key = "containers.%s.%s_%s" % (
                            name, new_key, unit)
                        results[result_key] = (new_value, 'GAUGE')

    def _default_memory_path(self):
        if os.path.exists('/proc/mounts'):
            with open('/proc/mounts') as f:
                split_lines = [l.split() for l in f.read().split("\n")]

            mount_and_options = [
                (p[1], p[3].split(','))
                for p in split_lines
                if len(p) >= 4 and p[0] == 'cgroup'
            ]

            for mount, options in mount_and_options:
                if 'memory' in options:
                    return mount
        return '/sys/fs/cgroup/memory'

    def _memory_stat_path(self, docker_id):
        vars = {
            'mount': self.memory_path,
            'id': docker_id
        }
        candidates = [
            "%(mount)s/system.slice/docker-%(id)s.scope/memory.stat" % vars,
            "%(mount)s/docker/%(id)s/memory.stat" % vars,
        ]
        result = [path for path in candidates if os.path.exists(path)]
        if len(result) > 0:
            return result[0]
        else:
            return None

    def _get_memory_stats(self, docker_id):
        path = self._memory_stat_path(docker_id)
        if not path:
            return None

        stat_file = open(path, 'r')
        elements = [line.split() for line in stat_file]
        stat_file.close()

        return [(n, v) for (n, v) in elements if n in _KEY_MAPPING]

# EOF
