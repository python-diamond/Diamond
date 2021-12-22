# coding=utf-8

"""
The DockerCollector uses the docker stats api to
collect data about docker and the containers.

#### Dependencies

* docker -- Install via `pip install docker-py`
  Source https://github.com/docker/docker-py
"""

import json
import diamond.collector

try:
    import docker
except ImportError:
    docker = None
else:
    DockerClient = docker.Client if docker.version < "2" else docker.APIClient


class DockerCollector(diamond.collector.Collector):

    METRICS = {
        # memory stats
        "memory_stats.stats.total_rss": "RSS_byte",
        "memory_stats.stats.total_cache": "cache_byte",
        "memory_stats.stats.total_swap": "swap_byte",
        "memory_stats.stats.total_pgpgin": "pagein_count",
        "memory_stats.stats.total_pgpgout": "pageout_count",

        # cpu stats
        "cpu_stats.cpu_usage.total_usage": "cpu.total",
        "cpu_stats.cpu_usage.usage_in_kernelmode": "cpu.kernelmode",
        "cpu_stats.cpu_usage.usage_in_usermode": "cpu.usermode",
        "cpu_stats.system_cpu_usage": "cpu.system",
    }

    def get_default_config_help(self):
        return super(DockerCollector, self).get_default_config_help()

    def get_default_config(self):
        config = super(DockerCollector, self).get_default_config()
        config.update({
            'path': 'docker'
        })
        return config

    def get_value(self, path, dictionary):
        keys = path.split(".")
        cur = dictionary
        for key in keys:
            if not isinstance(cur, dict):
                raise Exception("metric '{}' does not exist".format(path))
            cur = cur.get(key)
            if cur is None:
                break
        return cur

    def collect(self):
        if docker is None:
            self.log.error('Unable to import docker')

        # Collect info
        results = {}
        client = DockerClient(version='auto')

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

        # Collect memory and cpu stats
        for container in running_containers:
            name = "containers." + "".join(container['Names'][0][1:])
            s = client.stats(container["Id"])
            stat = json.loads(s.next())
            for path in self.METRICS:
                val = self.get_value(path, stat)
                if val is not None:
                    metric_key = ".".join([name, self.METRICS.get(path)])
                    results[metric_key] = (val, 'GAUGE')
            s.close()

        for name in sorted(results.keys()):
            (value, metric_type) = results[name]
            self.publish(name, value, metric_type=metric_type)
