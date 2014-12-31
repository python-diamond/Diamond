# coding=utf-8

"""
The JCollectdCollector is capable of receiving Collectd network traffic
as sent by the JCollectd jvm agent (and child Collectd processes).

Reason for developing this collector is allowing to use JCollectd, without
the need for Collectd.

A few notes:

This collector starts a UDP server to receive data. This server runs in
a separate thread and puts it on a queue, waiting for the collect() method
to pull. Because of this setup, the collector interval parameter is of
less importance. What matters is the 'sendinterval' JCollectd parameter.

See https://github.com/emicklei/jcollectd for an up-to-date jcollect fork.

#### Dependencies

 * jcollectd sending metrics

"""


import threading
import re
import Queue

import diamond.collector
import diamond.metric

import collectd_network


ALIVE = True


class JCollectdCollector(diamond.collector.Collector):

    def __init__(self, *args, **kwargs):
        super(JCollectdCollector, self).__init__(*args, **kwargs)
        self.listener_thread = None

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(JCollectdCollector, self).get_default_config()
        config.update({
            'path':     'jvm',
            'listener_host': '127.0.0.1',
            'listener_port': 25826,
        })
        return config

    def collect(self):
        if not self.listener_thread:
            self.start_listener()

        q = self.listener_thread.queue
        while True:
            try:
                dp = q.get(False)
                metric = self.make_metric(dp)
            except Queue.Empty:
                break
            self.publish_metric(metric)

    def start_listener(self):
        self.listener_thread = ListenerThread(self.config['listener_host'],
                                              self.config['listener_port'],
                                              self.log)
        self.listener_thread.start()

    def stop_listener(self):
        global ALIVE
        ALIVE = False
        self.listener_thread.join()
        self.log.error('Listener thread is shut down.')

    def make_metric(self, dp):

        path = ".".join((dp.host, self.config['path'], dp.name))

        if 'path_prefix' in self.config:
            prefix = self.config['path_prefix']
            if prefix:
                path = ".".join((prefix, path))

        if 'path_suffix' in self.config:
            suffix = self.config['path_suffix']
            if suffix:
                path = ".".join((path, suffix))

        if dp.is_counter:
            metric_type = "COUNTER"
        else:
            metric_type = "GAUGE"
        metric = diamond.metric.Metric(path, dp.value, dp.time,
                                       metric_type=metric_type)

        return metric

    def __del__(self):
        if self.listener_thread:
            self.stop_listener()


class ListenerThread(threading.Thread):
    def __init__(self, host, port, log, poll_interval=0.4):
        super(ListenerThread, self).__init__()
        self.name = 'JCollectdListener'  # thread name

        self.host = host
        self.port = port
        self.log = log
        self.poll_interval = poll_interval

        self.queue = Queue.Queue()

    def run(self):
        self.log.info('ListenerThread started on {0}:{1}(udp)'.format(
            self.host, self.port))

        rdr = collectd_network.Reader(self.host, self.port)

        try:
            while ALIVE:
                try:
                    items = rdr.interpret(poll_interval=self.poll_interval)
                    self.send_to_collector(items)
                except ValueError, e:
                    self.log.warn('Dropping bad packet: {0}'.format(e))
        except Exception, e:
            self.log.error('caught exception: type={0}, exc={1}'.format(type(e),
                                                                        e))

        self.log.info('ListenerThread - stop')

    def send_to_collector(self, items):
        if items is None:
            return

        for item in items:
            try:
                metric = self.transform(item)
                self.queue.put(metric)
            except Queue.Full:
                self.log.error('Queue to collector is FULL')
            except Exception, e:
                self.log.error('B00M! type={0}, exception={1}'.format(type(e),
                                                                      e))

    def transform(self, item):

        parts = []

        path = item.plugininstance
        # extract jvm name from 'logstash-MemoryPool Eden Space'
        if '-' in path:
            (jvm, tail) = path.split('-', 1)
            path = tail
        else:
            jvm = 'unnamed'

        # add JVM name
        parts.append(jvm)

        # add mbean name (e.g. 'java_lang')
        parts.append(item.plugin)

        # get typed mbean: 'MemoryPool Eden Space'
        if ' ' in path:
            (mb_type, mb_name) = path.split(' ', 1)
            parts.append(mb_type)
            parts.append(mb_name)
        else:
            parts.append(path)

        # add property name
        parts.append(item.typeinstance)

        # construct full path, from safe parts
        name = '.'.join([sanitize_word(part) for part in parts])

        if item[0][0] == 0:
            is_counter = True
        else:
            is_counter = False
        dp = Datapoint(item.host, item.time, name, item[0][1], is_counter)

        return dp


def sanitize_word(s):
    """Remove non-alphanumerical characters from metric word.
    And trim excessive underscores.
    """
    s = re.sub('[^\w-]+', '_', s)
    s = re.sub('__+', '_', s)
    return s.strip('_')


class Datapoint(object):
    def __init__(self, host, time, name, value, is_counter):
        self.host = host
        self.time = time
        self.name = name
        self.value = value
        self.is_counter = is_counter
