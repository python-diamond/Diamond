# coding=utf-8

"""
The NetAppCollector collects metric from a NetApp installation using the
NetApp Manageability SDK. This allows access to many metrics not available
via SNMP.

For this to work you'll the SDK available on the system.
This module has been developed using v5.0 of the SDK.
As of writing the SDK can be found at
https://communities.netapp.com/docs/DOC-1152

You'll also need to specify which NetApp instances the collecter should
get data from.

Example NetAppCollector.conf:
```
    enabled = True
    path_prefix = netapp

    [devices]

    [[na_filer]]
    ip = 123.123.123.123
    user = root
    password = strongpassword

````

The primary source for documentation about the API has been
"NetApp unified storage performance management using open interfaces"
https://communities.netapp.com/docs/DOC-1044

"""

import sys
import time
import re
import unicodedata

from diamond.metric import Metric
import diamond.convertor


class NetAppCollector(diamond.collector.Collector):

    # This is the list of metrics to collect.
    # This is a dict of lists with tuples, which is parsed as such:
    # The dict name is the object name in the NetApp API.
    # For each object we have a list of metrics to retrieve.
    # Each tuple is built like this;
    # ("metric name in netapp api", "output name of metric", multiplier)
    # The purpose of the output name is to enable replacement of reported
    # metric names, since some the names in the API can be confusing.
    # The purpose of the multiplier is to scale all metrics to a common
    # scale, which is latencies in milliseconds, and data in bytes per sec.
    # This is needed since the API will return a mixture of percentages,
    # nanoseconds, milliseconds, bytes and kilobytes.
    METRICS = {
        'aggregate': [
            ("user_reads", "user_read_iops", 1),
            ("user_writes", "user_write_iops", 1)
            ],
        'disk': [
            ("disk_busy", "disk_busy_pct", 100),
            ("base_for_disk_busy", "base_for_disk_busy", 1),
            ("user_read_blocks", "user_read_blocks_per_sec", 1),
            ("user_write_blocks", "user_write_blocks_per_sec", 1),
            ("user_read_latency", "user_read_latency", 0.001),
            ("user_write_latency", "user_write_latency", 0.001)
            ],
        'ifnet': [
            ("send_data", "tx_bytes_per_sec", 1),
            ("recv_data", "rx_bytes_per_sec", 1)
            ],
        'lun': [
            ("total_ops", "total_iops", 1),
            ("read_ops", "read_iops", 1),
            ("write_ops", "write_iops", 1),
            ("avg_latency", "avg_latency", 1)
            ],
        'processor': [
            ("processor_busy", "processor_busy_pct", 100),
            ("processor_elapsed_time", "processor_elapsed_time", 1)
            ],
        'system': [
            ("nfs_ops", "nfs_iops", 1),
            ("cifs_ops", "cifs_iops", 1),
            ("http_ops", "http_iops", 1),
            ("fcp_ops", "fcp_iops", 1),
            ("http_ops", "http_iops", 1),
            ("iscsi_ops", "iscsi_iops", 1),
            ("read_ops", "read_iops", 1),
            ("write_ops", "write_iops", 1),
            ("total_ops", "total_iops", 1),
            ("cpu_elapsed_time", "cpu_elapsed_time", 1),
            ("total_processor_busy", "total_processor_busy_pct", 100),
            ("avg_processor_busy", "avg_processor_busy_pct", 100),
            ("net_data_recv", "total_rx_bytes_per_sec", 1000),
            ("net_data_sent", "total_tx_bytes_per_sec", 1000),
            ("disk_data_read", "total_read_bytes_per_sec", 1000),
            ("disk_data_written", "total_write_bytes_per_sec", 1000),
            ("sys_read_latency", "sys_read_latency", 1),
            ("sys_write_latency", "sys_write_latency", 1),
            ("sys_avg_latency", "sys_avg_latency", 1)
            ],
        'vfiler': [
            ("vfiler_cpu_busy", "cpu_busy_pct", 100),
            ("vfiler_cpu_busy_base", "cpu_busy_base", 1),
            ("vfiler_net_data_recv", "rx_bytes_per_sec", 1000),
            ("vfiler_net_data_sent", "tx_bytes_per_sec", 1000),
            ("vfiler_read_ops", "read_iops", 1),
            ("vfiler_write_ops", "write_iops", 1),
            ("vfiler_read_bytes", "read_bytes_per_sec", 1000),
            ("vfiler_write_bytes", "write_bytes_per_sec", 1000),
            ],
        'volume': [
            ("total_ops", "total_iops", 1),
            ("avg_latency", "avg_latency", 0.001),
            ("read_ops", "read_iops", 1),
            ("write_ops", "write_iops", 1),
            ("read_latency", "read_latency", 0.001),
            ("write_latency", "write_latency", 0.001),
            ("read_data", "read_bytes_per_sec", 1),
            ("write_data", "write_bytes_per_sec", 1),
            ("cifs_read_data", "cifs_read_bytes_per_sec", 1),
            ("cifs_write_data", "cifs_write_bytes_per_sec", 1),
            ("cifs_read_latency", "cifs_read_latency", 0.001),
            ("cifs_write_latency", "cifs_write_latency", 0.001),
            ("cifs_read_ops", "cifs_read_iops", 1),
            ("cifs_write_ops", "cifs_write_iops", 1),
            ("fcp_read_data", "fcp_read_bytes_per_sec", 1),
            ("fcp_write_data", "fcp_write_bytes_per_sec", 1),
            ("fcp_read_latency", "fcp_read_latency", 0.001),
            ("fcp_write_latency", "fcp_write_latency", 0.001),
            ("fcp_read_ops", "fcp_read_iops", 1),
            ("fcp_write_ops", "fcp_write_iops", 1),
            ("iscsi_read_data", "iscsi_read_bytes_per_sec", 1),
            ("iscsi_write_data", "iscsi_write_bytes_per_sec", 1),
            ("iscsi_read_latency", "iscsi_read_latency", 0.001),
            ("iscsi_write_latency", "iscsi_write_latency", 0.001),
            ("iscsi_read_ops", "iscsi_read_iops", 1),
            ("iscsi_write_ops", "iscsi_write_iops", 1),
            ("nfs_read_data", "nfs_read_bytes_per_sec", 1),
            ("nfs_write_data", "nfs_write_bytes_per_sec", 1),
            ("nfs_read_latency", "nfs_read_latency", 0.001),
            ("nfs_write_latency", "nfs_write_latency", 0.001),
            ("nfs_read_ops", "nfs_read_iops", 1),
            ("nfs_write_ops", "nfs_write_iops", 1)
            ],
    }

    # For some metrics we need to divide one value from the API with another.
    # This is a key-value list of the connected values.
    DIVIDERS = {
        "avg_latency": "total_ops",
        "read_latency": "read_ops",
        "write_latency": "write_ops",
        "sys_avg_latency": "total_ops",
        "sys_read_latency": "read_ops",
        "sys_write_latency": "write_ops",
        "cifs_read_latency": "cifs_read_ops",
        "cifs_write_latency": "cifs_write_ops",
        "fcp_read_latency": "fcp_read_ops",
        "fcp_write_latency": "fcp_write_ops",
        "iscsi_read_latency": "iscsi_read_ops",
        "iscsi_write_latency": "iscsi_write_ops",
        "nfs_read_latency": "nfs_read_ops",
        "nfs_write_latency": "nfs_write_ops",
        "user_read_latency": "user_read_blocks",
        "user_write_latency": "user_write_blocks",
        "total_processor_busy": "cpu_elapsed_time",
        "avg_processor_busy": "cpu_elapsed_time",
        "processor_busy": "processor_elapsed_time",
        "disk_busy": "base_for_disk_busy",
        "vfiler_cpu_busy": "vfiler_cpu_busy_base",
    }

    # Some metrics are collected simply to calculate other metrics.
    # These should not be reported.
    DROPMETRICS = [
        "cpu_elapsed_time",
        "processor_elapsed_time",
        "base_for_disk_busy",
        "vfiler_cpu_busy_base",
    ]

    # Since we might have large collections collected often,
    # we need a pretty good time_delta.
    # We'll use a dict for this, keeping time_delta for each object.
    LastCollectTime = {}

    def get_default_config_help(self):
        config_help = super(NetAppCollector, self).get_default_config_help()
        return config_help

    def get_default_config(self):
        default_config = super(NetAppCollector, self).get_default_config()
        default_config['enabled'] = "false"
        default_config['path_prefix'] = "netapp"
        default_config['netappsdkpath'] = "/opt/netapp/lib/python/NetApp"
        return default_config

    def _replace_and_publish(self, path, prettyname, value, device):
        """
        Inputs a complete path for a metric and a value.
        Replace the metric name and publish.
        """
        if value is None:
            return
        newpath = path
        # Change metric name before publish if needed.
        newpath = ".".join([".".join(path.split(".")[:-1]), prettyname])
        metric = Metric(newpath, value, precision=4, host=device)
        self.publish_metric(metric)

    def _gen_delta_depend(self, path, derivative, multiplier, prettyname,
                          device):
        """
        For some metrics we need to divide the delta for one metric
        with the delta of another.
        Publishes a metric if the convertion goes well.
        """
        primary_delta = derivative[path]
        shortpath = ".".join(path.split(".")[:-1])
        basename = path.split(".")[-1]
        secondary_delta = None
        if basename in self.DIVIDERS.keys():
            mateKey = ".".join([shortpath, self.DIVIDERS[basename]])
        else:
            return
        if mateKey in derivative.keys():
            secondary_delta = derivative[mateKey]
        else:
            return

        # If we find a corresponding secondary_delta, publish a metric
        if primary_delta > 0 and secondary_delta > 0:
            value = (float(primary_delta) / secondary_delta) * multiplier
            self._replace_and_publish(path, prettyname, value, device)

    def _gen_delta_per_sec(self, path, value_delta, time_delta, multiplier,
                           prettyname, device):
        """
        Calulates the difference between to point, and scales is to per second.
        """
        if time_delta < 0:
            return
        value = (value_delta / time_delta) * multiplier
        # Only publish if there is any data.
        # This helps keep unused metrics out of Graphite
        if value > 0.0:
            self._replace_and_publish(path, prettyname, value, device)

    def collect(self, device, ip, user, password):
        """
        This function collects the metrics for one filer.
        """
        sys.path.append(self.config['netappsdkpath'])
        try:
            import NaServer
        except ImportError:
            self.log.error("Unable to load NetApp SDK from %s" % (
                self.config['netappsdkpath']))
            return

        # Set up the parameters
        server = NaServer.NaServer(ip, 1, 3)
        server.set_transport_type('HTTPS')
        server.set_style('LOGIN')
        server.set_admin_user(user, password)

        # We're only able to query a single object at a time,
        # so we'll loop over the objects.
        for na_object in self.METRICS.keys():

            # For easy reference later, generate a new dict for this object
            LOCALMETRICS = {}
            for metric in self.METRICS[na_object]:
                metricname, prettyname, multiplier = metric
                LOCALMETRICS[metricname] = {}
                LOCALMETRICS[metricname]["prettyname"] = prettyname
                LOCALMETRICS[metricname]["multiplier"] = multiplier

            # Keep track of how long has passed since we checked last
            CollectTime = time.time()
            time_delta = None
            if na_object in self.LastCollectTime.keys():
                time_delta = CollectTime - self.LastCollectTime[na_object]
            self.LastCollectTime[na_object] = CollectTime

            self.log.debug("Collecting metric of object %s" % na_object)
            query = NaServer.NaElement("perf-object-get-instances-iter-start")
            query.child_add_string("objectname", na_object)
            counters = NaServer.NaElement("counters")
            for metric in LOCALMETRICS.keys():
                counters.child_add_string("counter", metric)
            query.child_add(counters)

            res = server.invoke_elem(query)
            if(res.results_status() == "failed"):
                self.log.error("Connection to filer %s failed; %s" % (
                    device, res.results_reason()))
                return

            iter_tag = res.child_get_string("tag")
            num_records = 1
            max_records = 100

            # For some metrics there are dependencies between metrics for
            # a single object, so we'll need to collect all, so we can do
            # calculations later.
            raw = {}

            while(num_records != 0):
                query = NaServer.NaElement(
                    "perf-object-get-instances-iter-next")
                query.child_add_string("tag", iter_tag)
                query.child_add_string("maximum", max_records)
                res = server.invoke_elem(query)

                if(res.results_status() == "failed"):
                    print "Connection to filer %s failed; %s" % (
                        device, res.results_reason())
                    return

                num_records = res.child_get_int("records")

                if(num_records > 0):
                    instances_list = res.child_get("instances")
                    instances = instances_list.children_get()

                    for instance in instances:
                        raw_name = unicodedata.normalize(
                            'NFKD',
                            instance.child_get_string("name")).encode(
                            'ascii', 'ignore')
                        # Shorten the name for disks as they are very long and
                        # padded with zeroes, eg:
                        # 5000C500:3A236B0B:00000000:00000000:00000000:...
                        if na_object is "disk":
                            non_zero_blocks = [
                                block for block in raw_name.split(":")
                                if block != "00000000"
                                ]
                            raw_name = "".join(non_zero_blocks)
                        instance_name = re.sub(r'\W', '_', raw_name)
                        counters_list = instance.child_get("counters")
                        counters = counters_list.children_get()

                        for counter in counters:
                            metricname = unicodedata.normalize(
                                'NFKD',
                                counter.child_get_string("name")).encode(
                                'ascii', 'ignore')
                            metricvalue = counter.child_get_string("value")
                            # We'll need a long complete pathname to not
                            # confuse self.derivative
                            pathname = ".".join([self.config["path_prefix"],
                                                 device, na_object,
                                                 instance_name, metricname])
                            raw[pathname] = int(metricvalue)

            # Do the math
            self.log.debug("Processing %i metrics for object %s" % (len(raw),
                                                                    na_object))

            # Since the derivative function both returns the derivative
            # and saves a new point, we'll need to store all derivatives
            # for local reference.
            derivative = {}
            for key in raw.keys():
                derivative[key] = self.derivative(key, raw[key])

            for key in raw.keys():
                metricname = key.split(".")[-1]
                prettyname = LOCALMETRICS[metricname]["prettyname"]
                multiplier = LOCALMETRICS[metricname]["multiplier"]

                if metricname in self.DROPMETRICS:
                    continue
                elif metricname in self.DIVIDERS.keys():
                    self._gen_delta_depend(key, derivative, multiplier,
                                           prettyname, device)
                else:
                    self._gen_delta_per_sec(key, derivative[key], time_delta,
                                            multiplier, prettyname, device)
