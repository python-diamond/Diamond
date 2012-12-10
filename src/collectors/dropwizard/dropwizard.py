# coding=utf-8

"""
Collect dropwizard stats for the local node

#### Dependencies

 * urlib2

"""

import urllib2

try:
    import json
    json  # workaround for pyflakes issue #13
except ImportError:
    import simplejson as json

import diamond.collector


class DropwizardCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(DropwizardCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': "",
            'port': "",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(DropwizardCollector, self).get_default_config()
        config.update({
            'host':     '127.0.0.1',
            'port':     8081,
            'path':     'dropwizard',
        })
        return config

    def collect(self):
        if json is None:
            self.log.error('Unable to import json')
            return {}
        url = 'http://%s:%i/metrics' % (
            self.config['host'], int(self.config['port']))
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, err:
            self.log.error("%s: %s", url, err)
            return

        try:
            result = json.load(response)
        except (TypeError, ValueError):
            self.log.error("Unable to parse response from elasticsearch as a"
                           + " json object")
            return

        metrics = {}


        #
        # http connections to ES
        #metrics['http.current'] = data['http']['current_open']

        #
        # jvm memory
        metrics['jvm.memory.totalInit'] = result['jvm']['memory']['totalInit']
        metrics['jvm.memory.totalUsed'] = result['jvm']['memory']['totalUsed']
        metrics['jvm.memory.totalMax'] = result['jvm']['memory']['totalMax']
        metrics['jvm.memory.totalCommitted'] = result['jvm']['memory']['totalCommitted']

        metrics['jvm.memory.heapInit'] = result['jvm']['memory']['heapInit']
        metrics['jvm.memory.heapUsed'] = result['jvm']['memory']['heapUsed']
        metrics['jvm.memory.heapMax'] = result['jvm']['memory']['heapMax']
        metrics['jvm.memory.heapCommitted'] = result['jvm']['memory']['heapCommitted']
        metrics['jvm.memory.heap_usage'] = result['jvm']['memory']['heap_usage']
        metrics['jvm.memory.non_heap_usage'] = result['jvm']['memory']['non_heap_usage']
        metrics['jvm.memory.code_cache'] = result['jvm']['memory']['memory_pool_usages']['Code Cache']
        metrics['jvm.memory.eden_space'] = result['jvm']['memory']['memory_pool_usages']['PS Eden Space']
        metrics['jvm.memory.old_gen'] = result['jvm']['memory']['memory_pool_usages']['PS Old Gen']
        metrics['jvm.memory.perm_gen'] = result['jvm']['memory']['memory_pool_usages']['PS Perm Gen']
        metrics['jvm.memory.survivor_space'] = result['jvm']['memory']['memory_pool_usages']['PS Survivor Space']

        metrics['jvm.daemon_thread_count'] = result['jvm']['daemon_thread_count']
        metrics['jvm.thread_count'] = result['jvm']['thread_count']
        metrics['jvm.fd_usage'] = result['jvm']['fd_usage']

        metrics['jvm.thread_states.timed_waiting'] = result['jvm']['thread-states']['timed_waiting']
        metrics['jvm.thread_states.runnable'] = result['jvm']['thread-states']['runnable']
        metrics['jvm.thread_states.blocked'] = result['jvm']['thread-states']['blocked']
        metrics['jvm.thread_states.waiting'] = result['jvm']['thread-states']['waiting']
        metrics['jvm.thread_states.new'] = result['jvm']['thread-states']['new']
        metrics['jvm.thread_states.terminated'] = result['jvm']['thread-states']['terminated']

        for key in metrics:
            self.publish(key, metrics[key])
