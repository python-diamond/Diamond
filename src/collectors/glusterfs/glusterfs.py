# coding=utf-8

"""
The GlusterFSCollector currently only collects latency percentages
from the GlusterFS storage system.

version 0.3 beta

Documentation for GlusterFS profiling:
http://gluster.readthedocs.org/en/latest/Administrator%20Guide/Monitoring%20Workload/

#### Dependencies

 * glusterfs [https://www.gluster.org/]
 * Profiling enabled: gluster volume profile <VOLNAME> start

"""

import diamond.collector
import subprocess
import sys
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

metric_base = "glusterfs."
target_volume = ''
target_brick = ''


class GlusterFSCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(GlusterFSCollector, self).get_default_config_help()
        config_help.update({
            'gluster_path': 'complete path to gluster binary.' +
            ' Defaults to /usr/sbin/gluster',
            'target_volume': 'which brick to send info on.' +
            ' Defaults to all',
            'target_brick': 'which node/server to send metrics for.' +
            ' Defaults to all',
        })
        return config_help

    def get_default_config(self):
        config = super(GlusterFSCollector, self).get_default_config()
        config.update({
            'path': 'glusterfs',
            'gluster_path': '/usr/sbin/gluster',
            'target_volume': '',
            'target_brick': ''
        })
        return config

    def get_brick_metrics(self):
        temp_bval = self.volelem.find('brickName').text
        temp_list = temp_bval.split(':')
        brick_name = temp_list[0]

        # self.log.info("checking gluster brick " + brick_name)
        if (brick_name == self.config['target_brick'] or
                self.config['target_brick'] == ''):
                running_grand_avg_total = 0.0
                running_avg_total = 0.0
                running_calls_total = 0.0
                fop_stats = {}

                for fopstatselem in \
                        self.volelem.find('cumulativeStats').find('fopStats'):
                            # self.log.info("getting gluster metrics")
                            name = fopstatselem.findtext('name')
                            hits = fopstatselem.findtext('hits')
                            avg_latency = \
                                float(fopstatselem.findtext('avgLatency'))
                            min_latency = \
                                float(fopstatselem.findtext('minLatency'))
                            max_latency = \
                                float(fopstatselem.findtext('maxLatency'))
                            fop_total_avg = avg_latency * int(hits)
                            running_grand_avg_total = \
                                running_grand_avg_total + fop_total_avg
                            fop_stats[name] = hits, avg_latency, \
                                fop_total_avg, min_latency, max_latency

                for fop in fop_stats:
                    # self.log.info("sending gluster metrics")
                    metric_name_base = self.metric_base + "." + brick_name + \
                        "." + fop
                    metric_name = metric_name_base + ".pctLatency"
                    metric_value = (fop_stats[fop][2] / running_grand_avg_total) \
                        * 100
                    self.publish(metric_name, metric_value)
                    metric_name = metric_name_base + ".hits"
                    metric_value = fop_stats[fop][0]
                    self.publish(metric_name, metric_value)
                    metric_name = metric_name_base + ".avgLatency"
                    metric_value = fop_stats[fop][1]
                    self.publish(metric_name, metric_value)
                    metric_name = metric_name_base + ".totalLatency"
                    metric_value = fop_stats[fop][2]
                    self.publish(metric_name, metric_value)
                    metric_name = metric_name_base + ".minLatency"
                    metric_value = fop_stats[fop][3]
                    self.publish(metric_name, metric_value)
                    metric_name = metric_name_base + ".maxLatency"
                    metric_value = fop_stats[fop][4]
                    self.publish(metric_name, metric_value)

    def collect(self):
        gluster_call = self.config['gluster_path'] + ' volume list'
        out = subprocess.Popen([gluster_call], stdout=subprocess.PIPE,
            shell=True)
        (volumes, err) = out.communicate()

        for volume in volumes.splitlines():
            # self.log.info("checking gluster volume " + volume)
            if (volume == self.config['target_volume'] or
                    self.config['target_volume'] == ''):
                        self.metric_base = volume

                        xml_out = subprocess.Popen([self.config['gluster_path']
                            + " volume profile " + volume +
                            " info cumulative --xml"], stdout=subprocess.PIPE,
                            shell=True)
                        (raw_metrics, err) = xml_out.communicate()
                        xml_metrics = ET.XML(raw_metrics)

                        for self.volelem in xml_metrics.find('volProfile'):
                            if (self.volelem.tag == 'brick'):

                                brick_metrics = self.get_brick_metrics()
