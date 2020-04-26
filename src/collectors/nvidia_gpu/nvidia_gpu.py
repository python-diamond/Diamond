# coding=utf-8

"""
The NvidiaGPUCollector collects GPU utilization metric using nvidia-smi.

See https://developer.nvidia.com/nvidia-system-management-interface

#### Dependencies

 * nvidia-smi
 * nvidia-ml-py (Optional)
"""

from itertools import izip
try:
    import pynvml
    USE_PYTHON_BINDING = True
except ImportError:
    USE_PYTHON_BINDING = False

import diamond.collector


class NvidiaGPUCollector(diamond.collector.ProcessCollector):

    def get_default_config_help(self):
        config_help = super(NvidiaGPUCollector, self).get_default_config_help()
        config_help.update({
            'bin': 'The path to the nvidia-smi binary',
            'stats': 'A list of Nvidia GPU stats to collect. '
                     'Use `nvidia-smi --help-query-gpu` for more information'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(NvidiaGPUCollector, self).get_default_config()
        config.update({
            'path': 'nvidia',
            'bin': '/usr/bin/nvidia-smi',
            'stats': [
                'index',
                'memory.total',
                'memory.used',
                'memory.free',
                'utilization.gpu',
                'utilization.memory',
                'temperature.gpu'
            ]
        })
        return config

    def collect_via_nvidia_smi(self, stats_config):
        """
        Use nvidia smi command line tool to collect metrics
        :param stats_config:
        :return:
        """
        raw_output = self.run_command([
            '--query-gpu={query_gpu}'.format(query_gpu=','.join(stats_config)),
            '--format=csv,nounits,noheader'
        ])

        if raw_output is None:
            return

        results = raw_output[0].strip().split("\n")
        for result in results:
            stats = result.strip().split(',')
            assert len(stats) == len(stats_config)
            index = stats[0]
            for stat_name, metric in izip(stats_config[1:], stats[1:]):
                metric_name = 'gpu_{index}.{stat_name}'.format(
                    index=str(index),
                    stat_name=stat_name
                )
                self.publish(metric_name, metric)

    def collect_via_pynvml(self, stats_config):
        """
        Use pynvml python binding to collect metrics
        :param stats_config:
        :return:
        """
        try:
            NVML_TEMPERATURE_GPU = 0
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()

            for device_index in xrange(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(device_index)
                memoryInfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
                utilizationRates = pynvml.nvmlDeviceGetUtilizationRates(handle)

                metrics = {
                    'memory.total': memoryInfo.total / 1024 / 1024,
                    'memory.used': memoryInfo.total / 1024 / 1024,
                    'memory.free': memoryInfo.free / 1024 / 1024,
                    'utilization.gpu': utilizationRates.gpu,
                    'utilization.memory': utilizationRates.memory,
                    'temperature.gpu':
                        pynvml.nvmlDeviceGetTemperature(handle,
                                                        NVML_TEMPERATURE_GPU)
                }

                for stat_name in stats_config[1:]:
                    metric = metrics.get(stat_name)
                    if metric:
                        metric_name = 'gpu_{index}.{stat_name}'.format(
                            index=str(device_index),
                            stat_name=stat_name
                        )
                        self.publish(metric_name, metric)
        finally:
            pynvml.nvmlShutdown()

    def collect(self):
        """
        Collector GPU stats
        """
        stats_config = self.config['stats']
        if USE_PYTHON_BINDING:
            collect_metrics = self.collect_via_pynvml
        else:
            collect_metrics = self.collect_via_nvidia_smi

        collect_metrics(stats_config)
