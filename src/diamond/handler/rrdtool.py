# coding=utf-8

"""
Save stats in RRD files using rrdtool.
"""

import os
import re
import subprocess
import Queue

from Handler import Handler

#
# Constants for RRD file creation.
#

# NOTE: We default to the collectd RRD directory
# simply as a compatibility tool. Users that have
# tools that look in that location and would like
# to switch to Diamond need to make zero changes.

BASEDIR = '/var/lib/collectd/rrd'

METRIC_STEP = 10

BATCH_SIZE = 1

# NOTE: We don't really have a rigorous defition
# for metrics, particularly how often they will be
# reported, etc. Because of this, we have to guess
# at the steps and RRAs used for creation of the
# RRD files. These are a fairly sensible default,
# and basically allow for aggregated up from a single
# datapoint (because the XFF is 0.1, and each step
# aggregates not more than 10 of the previous step).
#
# Given a METRIC_STEP of 10 seconds, then these will
# represent data for up to the last full year.

RRA_SPECS = [
    "RRA:AVERAGE:0.1:1:1200",
    "RRA:MIN:0.1:1:1200",
    "RRA:MAX:0.1:1:1200",
    "RRA:AVERAGE:0.1:7:1200",
    "RRA:MIN:0.1:7:1200",
    "RRA:MAX:0.1:7:1200",
    "RRA:AVERAGE:0.1:50:1200",
    "RRA:MIN:0.1:50:1200",
    "RRA:MAX:0.1:50:1200",
    "RRA:AVERAGE:0.1:223:1200",
    "RRA:MIN:0.1:223:1200",
    "RRA:MAX:0.1:223:1200",
    "RRA:AVERAGE:0.1:2635:1200",
    "RRA:MIN:0.1:2635:1200",
    "RRA:MAX:0.1:2635:1200",
]


class RRDHandler(Handler):

    # NOTE: This handler is fairly loose about locking (none),
    # and the reason is because the calls are always protected
    # by locking done in the _process and _flush routines.
    # If this were to change at some point, we would definitely
    # want to be a bit more sensible about how we lock.
    #
    # We would probably also want to restructure this as a
    # consumer and producer so that one thread can continually
    # write out data, but that really depends on the design
    # at the top level.

    def __init__(self, *args, **kwargs):
        super(RRDHandler, self).__init__(*args, **kwargs)
        self._exists_cache = dict()
        self._basedir = self.config['basedir']
        self._batch = self.config['batch']
        self._step = self.config['step']
        self._queues = {}
        self._last_update = {}

    def get_default_config_help(self):
        config = super(RRDHandler, self).get_default_config_help()
        config.update({
            'basedir': 'The base directory for all RRD files.',
            'batch': 'Wait for this many updates before saving to the RRD file',
            'step': 'The minimum interval represented in generated RRD files.',
        })
        return config

    def get_default_config(self):
        config = super(RRDHandler, self).get_default_config()
        config.update({
            'basedir': BASEDIR,
            'batch': BATCH_SIZE,
            'step': METRIC_STEP,
        })
        return config

    def _ensure_exists(self, filename, metric_name, metric_type):
        # We're good to go!
        if filename in self._exists_cache:
            return True

        # Does the file already exist?
        if os.path.exists(filename):
            self._exists_cache[filename] = True
            return True

        # Attempt the creation.
        self._create(filename, metric_name, metric_type)
        self._exists_cache[filename] = True
        return True

    def _create(self, filename, metric_name, metric_type):
        # Sanity check the metric name.
        if not re.match("^[a-zA-Z0-9_]+$", metric_name):
            raise Exception("Invalid metric name: %s" % metric_name)

        # Sanity check the metric type.
        if metric_type not in ("GAUGE", "COUNTER"):
            raise Exception("Unknown metric type: %s" % metric_type)

        # Try to create the directory.
        # NOTE: If we aren't successful, the check_call()
        # will fail anyways so we can do this optimistically.
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError:
            pass

        ds_spec = "DS:%s:%s:%d:U:U" % (
            metric_name, metric_type, self._step * 2)
        rrd_create_cmd = [
            "rrdtool", "create", filename,
            "--no-overwrite",
            "--step", str(self._step),
            ds_spec
        ]
        rrd_create_cmd.extend(RRA_SPECS)
        subprocess.check_call(rrd_create_cmd, close_fds=True)

    def process(self, metric):
        # Extract the filename given the metric.
        # NOTE: We have to tweak the metric name and limit
        # the length to 19 characters for the RRD file format.
        collector = metric.getCollectorPath()
        metric_name = metric.getMetricPath().replace(".", "_")[:19]

        dirname = os.path.join(self._basedir, metric.host, collector)
        filename = os.path.join(dirname, metric_name + ".rrd")

        # Ensure that there is an RRD file for this metric.
        # This is done inline because it's quickly cached and
        # we would like to have exceptions related to creating
        # the RRD file raised in the main thread.
        self._ensure_exists(filename, metric_name, metric.metric_type)
        if self._queue(filename, metric.timestamp, metric.value) >= self._batch:
            self._flush_queue(filename)

    def _queue(self, filename, timestamp, value):
        if not filename in self._queues:
            queue = Queue.Queue()
            self._queues[filename] = queue
        else:
            queue = self._queues[filename]
        queue.put((timestamp, value))
        return queue.qsize()

    def flush(self):
        # Grab all current queues.
        for filename in self._queues.keys():
            self._flush_queue(filename)

    def _flush_queue(self, filename):
        queue = self._queues[filename]

        # Collect all pending updates.
        updates = {}
        max_timestamp = 0
        while True:
            try:
                (timestamp, value) = queue.get(block=False)
                # RRD only supports granularity at a
                # per-second level (not milliseconds, etc.).
                timestamp = int(timestamp)

                # Remember the latest update done.
                last_update = self._last_update.get(filename, 0)
                if last_update >= timestamp:
                    # Yikes. RRDtool won't let us do this.
                    # We need to drop this update and log a warning.
                    self.log.warning(
                        "Dropping update to %s. Too frequent!" % filename)
                    continue
                max_timestamp = max(timestamp, max_timestamp)

                # Add this update.
                if not timestamp in updates:
                    updates[timestamp] = []
                updates[timestamp].append(value)
            except Queue.Empty:
                break

        # Save the last update time.
        self._last_update[filename] = max_timestamp

        if len(updates) > 0:
            # Construct our command line.
            # This will look like <time>:<value1>[:<value2>...]
            # The timestamps must be sorted, and we each of the
            # <time> values must be unique (like a snowflake).
            data_points = map(
                    lambda (timestamp, values): "%d:%s" %
                        (timestamp, ":".join(map(str, values))),
                    sorted(updates.items()))

            # Optimisticly update.
            # Nothing can really be done if we fail.
            rrd_update_cmd = ["rrdupdate", filename, "--"]
            rrd_update_cmd.extend(data_points)
            self.log.info("update: %s" % str(rrd_update_cmd))
            subprocess.call(rrd_update_cmd)
