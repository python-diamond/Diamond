# coding=utf-8

"""
Collect Memory usage and limit of LXCs

#### Dependencies
 * cgroup, I guess

"""

from diamond.collector import Collector
import diamond.convertor
import os


class MemoryLxcCollector(Collector):

    def get_default_config_help(self):
        """
        Return help text for collector configuration.
        """
        config_help = super(MemoryLxcCollector, self).get_default_config_help()
        config_help.update({
            "sys_path": "Defaults to '/sys/fs/cgroup/lxc'",
        })
        return config_help

    def get_default_config(self):
        """
        Returns default settings for collector.
        """
        config = super(MemoryLxcCollector, self).get_default_config()
        config.update({
            "path":     "lxc",
            "sys_path": "/sys/fs/cgroup/lxc",
        })
        return config

    def collect(self):
        """
        Collect memory stats of LXCs.
        """
        lxc_metrics = ["memory.usage_in_bytes", "memory.limit_in_bytes"]
        if os.path.isdir(self.config["sys_path"]) is False:
            self.log.debug("sys_path '%s' isn't directory.",
                           self.config["sys_path"])
            return {}

        collected = {}
        for item in os.listdir(self.config["sys_path"]):
            fpath = "%s/%s" % (self.config["sys_path"], item)
            if os.path.isdir(fpath) is False:
                continue

            for lxc_metric in lxc_metrics:
                filename = "%s/%s" % (fpath, lxc_metric)
                metric_name = "%s.%s" % (
                    item.replace(".", "_"),
                    lxc_metric.replace("_in_bytes", ""))
                self.log.debug("Trying to collect from %s", filename)
                collected[metric_name] = self._read_file(filename)

        for key in collected.keys():
            if collected[key] is None:
                continue

            for unit in self.config["byte_unit"]:
                value = diamond.convertor.binary.convert(
                    collected[key],
                    oldUnit="B",
                    newUnit=unit)
                new_key = "%s_in_%ss" % (key, unit)
                self.log.debug("Publishing '%s %s'", new_key, value)
                self.publish(new_key, value, metric_type="GAUGE")

    def _read_file(self, filename):
        """
        Read contents of given file.
        """
        try:
            with open(filename, "r") as fhandle:
                stats = float(fhandle.readline().rstrip("\n"))
        except Exception:
            stats = None

        return stats
