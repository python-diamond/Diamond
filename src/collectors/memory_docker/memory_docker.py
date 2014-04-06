import docker
from memory_cgroup import MemoryCgroupCollector


class MemoryDockerCollector(MemoryCgroupCollector):
    def collect(self):
        self.containers = {c['Id']: c['Names'][0][1:]
                           for c in docker.Client().containers(all=True)
                           if c['Names'] is not None}
        return super(MemoryDockerCollector, self).collect()

    def publish(self, metric_name, value, metric_type):
        for container_id, container_name in self.containers.items():
            metric_name = metric_name.replace(
                'docker.'+container_id+'.', 'docker.'+container_name+'.')
        return super(MemoryDockerCollector, self).publish(
            metric_name, value, metric_type)
