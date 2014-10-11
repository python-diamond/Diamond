# coding=utf-8

"""
The GridEngineCollector parses qstat statistics from Sun Grid Engine,
Univa Grid Engine and Open Grid Scheduler.

#### Dependencies

 * Grid Engine qstat

"""

import os
import re
import subprocess
import sys
import xml.dom.minidom

import diamond.collector


class GridEngineCollector(diamond.collector.Collector):
    """Diamond collector for Grid Engine performance data
    """

    class QueueStatsEntry:
        def __init__(self, name=None, load=None, used=None, resv=None,
                     available=None, total=None, temp_disabled=None,
                     manual_intervention=None):
            self.name = name
            self.load = load
            self.used = used
            self.resv = resv
            self.available = available
            self.total = total
            self.temp_disabled = temp_disabled
            self.manual_intervention = manual_intervention

    class StatsParser(object):
        def __init__(self, document):
            self.dom = xml.dom.minidom.parseString(document.strip())

        def get_tag_text(self, node, tag_name):
            el = node.getElementsByTagName(tag_name)[0]
            return self.get_text(el)

        def get_text(self, node):
            rc = []
            for node in node.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    rc.append(node.data)
            return ''.join(rc)

    class QueueStatsParser(StatsParser):
        def __init__(self, document):
            self.dom = xml.dom.minidom.parseString(document.strip())

        def parse(self):
            cluster_queue_summaries = self.dom.getElementsByTagName(
                "cluster_queue_summary")
            return [
                self._parse_cluster_stats_entry(node)
                for node in cluster_queue_summaries]

        def _parse_cluster_stats_entry(self, node):
            name = self.get_tag_text(node, "name")
            load = float(self.get_tag_text(node, "load"))
            used = int(self.get_tag_text(node, "used"))
            resv = int(self.get_tag_text(node, "resv"))
            available = int(self.get_tag_text(node, "available"))
            total = int(self.get_tag_text(node, "total"))
            temp_disabled = int(self.get_tag_text(node, "temp_disabled"))
            manual_intervention = int(self.get_tag_text(
                node,
                "manual_intervention"))

            return GridEngineCollector.QueueStatsEntry(
                name=name,
                load=load,
                used=used,
                resv=resv,
                available=available,
                total=total,
                temp_disabled=temp_disabled,
                manual_intervention=manual_intervention)

    def process_config(self):
        os.environ['SGE_ROOT'] = self.config['sge_root']

    def get_default_config_help(self):
        config_help = super(GridEngineCollector,
                            self).get_default_config_help()
        config_help.update({
            'bin_path': "The path to Grid Engine's qstat",
            'sge_root': "The SGE_ROOT value to provide to qstat"
        })
        return config_help

    def get_default_config(self):
        config = super(GridEngineCollector, self).get_default_config()
        config.update({
            'bin_path': '/opt/gridengine/bin/lx-amd64/qstat',
            'method': 'Threaded',
            'path': 'gridengine',
            'sge_root': self._sge_root(),
        })
        return config

    def collect(self):
        """Collect statistics from Grid Engine via qstat.
        """
        self._collect_queue_stats()

    def _capture_output(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        bytestr = p.communicate()[0]
        output = bytestr.decode(sys.getdefaultencoding())
        return output

    def _collect_queue_stats(self):
        output = self._queue_stats_xml()
        parser = self.QueueStatsParser(output)
        for cq in parser.parse():
            name = self._sanitize(cq.name)
            prefix = 'queues.%s' % (name)
            metrics = ['load', 'used', 'resv', 'available', 'total',
                       'temp_disabled', 'manual_intervention']
            for metric in metrics:
                path = '%s.%s' % (prefix, metric)
                value = getattr(cq, metric)
                self.publish(path, value)

    def _queue_stats_xml(self):
        bin_path = self.config['bin_path']
        return self._capture_output([bin_path, '-g', 'c', '-xml'])

    def _sanitize(self, s):
        """Sanitize the name of a metric to remove unwanted chars
        """
        return re.sub("[^\w-]", "_", s)

    def _sge_root(self):
        sge_root = os.environ.get('SGE_ROOT')
        if sge_root:
            return sge_root
        else:
            return '/opt/gridengine'
