"""
The StatsdCollector is capable of receiving data as sent by any statsd client.

This collector was created in order to be able to collect statsd metrics without having to use statsd. Currently, this
collector supports a subset of statsd metrics as defined in
https://github.com/etsy/statsd/blob/master/docs/metric_types.md.

In particular, this collector does not support:
 - sets
 - gauges with -/+ modifiers

This collector starts a UDP server in a separate thread to receive and parse data. The server puts the data on a
queue and waits for the collect() method to pull.

"""
import re
import diamond.metric
import threading
import socket
import Queue
from collections import namedtuple

ALIVE = True
valid_types = ["g", "ms", "c"]

NewMetric = namedtuple('NewMetric', ['path', 'value', 'metric_type'])


def _clean_key(k):
    return re.sub(
        r'[^a-zA-Z_\-0-9\.]',
        '',
        re.sub(
            r'\s+',
            '_',
            k.replace('/', '-').replace(' ', '_')
        )
    )


def parse_metrics(raw_metrics):
    for raw_metric in raw_metrics.split("\n"):
        data, metric_type = raw_metric.split("|")[:2]
        metric_name, value = data.split(":")
        metric_name =_clean_key(metric_name)

        metric = NewMetric(path=metric_name, value=value, metric_type='GAUGE')
        if metric_type == "c":
            metric.metric_type = 'COUNTER'
        elif metric_type not in valid_types:
            raise ValueError("Metric type %i not recognized/supported" % metric_type)
        yield metric


class StatsdCollector(diamond.collector.Collector):

    def __init__(self, *args, **kwargs):
        super(StatsdCollector, self).__init__(*args, **kwargs)
        self.listener_thread = None

    def get_default_config(self):
        """
        Returns default collector settings
        """
        config = super(StatsdCollector, self).get_default_config()
        config.update({
            'listener_host': '127.0.0.1',
            'listener_port': 8787,
            'path': 'statsd',
        })
        return config

    def collect(self):
        if not self.listener_thread:
            self.start_listener()

        while True:
            try:
                data = self.listener_thread.queue.get(block=True, timeout=0.2)
                self.publish(data.path, data.value, metric_type=data.metric_type)
            except Queue.Empty:
                self.log.info('Queue is empty')
                break
            except Exception as e:
                self.log.error('type={}, exception={}'.format(type(e), e))
            self.log.info('Path: {}, Value: {}'.format(data.path, data.value))

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

    def __del__(self):
        if self.listener_thread:
            self.stop_listener()


class ListenerThread(threading.Thread):
    """
    Starts a udp server to listen for packets and parse them. Stores them in queue.
    """
    BUFFER_SIZE = 16384

    def __init__(self, host, port, log):
        super(ListenerThread, self).__init__()
        self.name = "statsdCollectorThread"

        self.host = host
        self.port = port
        self.log = log
        self._sock = None

        self.queue = Queue.Queue()

    def run(self):
        self.log.info('ListenerThread started on {}:{}(udp)'.format(
            self.host, self.port))

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, int(self.port)))

        try:
            while ALIVE:
                try:
                    items = self.receive()
                    if items is not None:
                        items = parse_metrics(items)
                        for item in items:
                            try:
                                self.queue.put(item, block=True, timeout=0.2)
                            except Queue.Full:
                                self.log.error("Queue to collector is FULL")
                except ValueError as e:
                    self.log.warn('Dropping bad packet: {}', format(e))
        except Exception as e:
            self.log.error('type={}, exception={}'.format(type(e), e))

    def receive(self):
        data, addr = self._sock.recvfrom(self.BUFFER_SIZE)
        return data or None


