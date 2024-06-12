# coding=utf-8

"""
A simple collector to gather hypervisor resource usage stats

#### Dependencies

 * python-novaclient

"""

import diamond.collector
from novaclient import client


class NovaHypervisorStatsCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(NovaHypervisorStatsCollector,
                            self).get_default_config_help()
        config_help.update({
            'username':   'User to auth with',
            'password':   'Password to auth with',
            'tenant':     'Tenancy to use',
            'auth_url':   'Keystone ip or hostname',
            'auth_proto': 'HTTP protocol to use',
            'cpu_allocation_ratio': 'As per nova.conf, '
                                    'the allocation ratio of '
                                    'real to virtual cores',
            'ram_allocation_ratio': 'As per nova.conf, '
                                    'the allocation ratio '
                                    'of real to virtual ram',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(NovaHypervisorStatsCollector, self).get_default_config()
        config.update({
            'path':           'nova.hypervisorstats',
            'username':   'admin',
            'password':   'admin',
            'tenant':     'admin',
            'auth_url':   '127.0.0.1',
            'auth_proto': 'http',
            'cpu_allocation_ratio': '16',
            'ram_allocation_ratio': '1.5',
        })
        return config

    def collect(self):
        url = self.config['auth_proto'] + '://' + \
            self.config['auth_url'] + ':5000/v2.0/'

        nova = client.Client('2', self.config['username'],
                             self.config['password'],
                             self.config['tenant'],
                             url, timeout=120,
                             service_type="compute",
                             no_cache=True)

        s = []

        rollup = nova.hypervisors.statistics()._info
        s.append({rollup + '.disk.local_gb': rollup['local_gb']})
        s.append({rollup + '.disk.local_gb_used': rollup['local_gb_used']})
        s.append({rollup + '.disk.free_disk_gb': rollup['free_disk_gb']})
        s.append({rollup + '.disk.disk_available_least':
                  rollup['disk_available_least']})
        s.append({rollup + '.memory.total':
                  rollup['memory_mb'] * ram_allocation_ratio})
        s.append({rollup + '.memory.real': rollup['memory_mb']})
        s.append({rollup + '.memory.used': rollup['memory_mb_used']})
        s.append({rollup + '.memory.free_real': rollup['free_ram_mb']})
        s.append({rollup + '.memory.free':
                  rollup['memory_mb'] * ram_allocation_ratio -
                  rollup['memory_mb_used']})
        s.append({rollup + '.running_vms': rollup['running_vms']})
        s.append({rollup + '.vcpus.total':
                  rollup['vcpus'] * cpu_allocation_ratio})
        s.append({rollup + '.vcpus.used':
                  rollup['vcpus_used'] * cpu_allocation_ratio})
        s.append({rollup + '.vcpus.real':
                  rollup['vcpus'] * cpu_allocation_ratio})
        hypervisors = nova.hypervisors.list()
        if hypervisors:
            for h in hypervisors:
                hv = nova.hypervisors.get(h.id)
                stats = hv._info.copy()
                hostname = stats['hypervisor_hostname'].split('.')

                max_vcpus = (int(stats['vcpus']) *
                             float(self.config['cpu_allocation_ratio']))
                vcpus_percent_used = ((stats['vcpus_used']/max_vcpus) * 100)

                s.append({hostname[0] + '.max_vcpus': max_vcpus})
                s.append({hostname[0] + '.vcpus_percent_used':
                          vcpus_percent_used})

                max_ram = (int(stats['memory_mb']) *
                           float(self.config['ram_allocation_ratio']))
                ram_percent_used = ((stats['memory_mb_used']/max_ram) * 100)
                s.append({hostname[0] + '.max_ram': max_ram})
                s.append({hostname[0] + '.ram_percent_used':
                          ram_percent_used})

                for k, v in sorted(stats.items()):
                    hostname = h.hypervisor_hostname.split('.')
                    metric_name = ("%s.%s") % (hostname[0], k)
                    s.append({metric_name: v})

        for metric in s:
            for key, val in metric.items():
                self.publish(key, val)
