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

Timer and counter metrics are aggregated and all times are converted to seconds. Clients are expected to send metrics in
milliseconds.
"""
import re
import sys
import diamond.metric
import threading
import socket
import Queue
from collections import namedtuple, defaultdict


ALIVE = True

#remove non-alphanumeric characters
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
            'pct_threshold': 90.0,
        })
        return config

    def flush(self):
        for key, value in self.listener_thread.gauges.items():
            self.publish(key, value)
            #self.log.info('GAUGE: ({}, {})'.format(key, value))

        for key, value in self.listener_thread.counters.items():
            value = value / (float(self.config['interval']))
            self.publish(key, value, metric_type='COUNTER')
            #self.log.info('COUNTER: ({}, {})'.format(key, value))
            del(self.listener_thread.counters[key])

        for key, values in self.listener_thread.timers.items():
            if len(values) > 0:
                values.sort()
                if len(values) > 0:
                # Sort all the received values. We need it to extract percentiles
                    values.sort()
                    count = float(len(values))
                    min_val = values[0]
                    max_val = values[-1]

                    mean = min_val
                    max_threshold = max_val

                    if count > 1:
                        thresh_index = int((float(self.config['pct_threshold']) / 100.0) * count)
                        max_threshold = values[thresh_index - 1]
                        total = sum(values)
                        mean = total / count

                    del(self.listener_thread.timers[key])

                    self.publish(key + '_mean', mean / 1000.0)
                    #self.log.info('TIMER: ({}, {})'.format(key + '_mean', mean/1000.0))
                    self.publish(key + '_min', min_val / 1000.0)
                    #self.log.info('TIMER: ({}, {})'.format(key + '_min', min_val/1000.0))
                    self.publish(key + '_max', max_val / 1000.0)
                    self.publish(key + '_count', count)
                    self.publish(key + '_' + str(self.config['pct_threshold']) + 'pct', max_threshold/1000.0)
                    #self.log.info('TIMER: ({}, {})'.format(key + str(self.config['pct_threshold']) + 'pct', max_threshold/1000.0))

    def collect(self):
        if not self.listener_thread:
            self.start_listener()

        self.flush()

    def start_listener(self):
        self.listener_thread = ListenerThread(self.config['listener_host'],
                                              self.config['listener_port'],
                                              self.log)
        self.listener_thread.start()

    def stop_listener(self):
        global ALIVE
        ALIVE = False
        self.listener_thread.join()
        self.flush()
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

        self.gauges = defaultdict(float)
        self.counters = defaultdict(float)
        self.timers = defaultdict(list)

    def run(self):
        self.log.info('ListenerThread started on {}:{}(udp)'.format(
            self.host, self.port))

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, int(self.port)))

        while ALIVE:
            try:
                items = self.receive()
                if items is not None:
                    self.parse_metrics(items)
            except ValueError as e:
                self.log.warn('Dropping bad packet: {}', format(e))
            except Exception as e:
                self.log.error('type={}, exception={}'.format(type(e), e))

    def receive(self):
        data = self._sock.recv(self.BUFFER_SIZE)
        return data or None

    def parse_metrics(self, raw_metrics):
        raw_metrics.rstrip('\n')

        for metric in raw_metrics.split('\n'):
            data, mtype = metric.split("|")[:2]
            key, value = data.split(":")
            key = _clean_key(key)

            if mtype == 'ms':
                self.record_timer(key, value)
            elif mtype == 'g':
                self.record_gauge(key, value)
            elif mtype == 'c':
                self.record_counter(key, value)
            else:
                raise ValueError("Metric type %s not recognized/supported" % metric_type)

    def record_timer(self, key, value):
        self.timers[key].append(float(value) or 0)

    def record_gauge(self, key, value):
        self.gauges[key] = float(value)

    def record_counter(self, key, value):
        self.counters[key] += float(value or 1)

