# coding=utf-8

"""
Collect [dropwizard](http://dropwizard.codahale.com/) stats for the local node

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

        memory = result['jvm']['memory']
        mempool = memory['memory_pool_usages']
        jvm = result['jvm']
        thread_st = jvm['thread-states']

        metrics['jvm.memory.totalInit'] = memory['totalInit']
        metrics['jvm.memory.totalUsed'] = memory['totalUsed']
        metrics['jvm.memory.totalMax'] = memory['totalMax']
        metrics['jvm.memory.totalCommitted'] = memory['totalCommitted']

        metrics['jvm.memory.heapInit'] = memory['heapInit']
        metrics['jvm.memory.heapUsed'] = memory['heapUsed']
        metrics['jvm.memory.heapMax'] = memory['heapMax']
        metrics['jvm.memory.heapCommitted'] = memory['heapCommitted']
        metrics['jvm.memory.heap_usage'] = memory['heap_usage']
        metrics['jvm.memory.non_heap_usage'] = memory['non_heap_usage']
        metrics['jvm.memory.code_cache'] = mempool['Code Cache']
        metrics['jvm.memory.eden_space'] = mempool['PS Eden Space']
        metrics['jvm.memory.old_gen'] = mempool['PS Old Gen']
        metrics['jvm.memory.perm_gen'] = mempool['PS Perm Gen']
        metrics['jvm.memory.survivor_space'] = mempool['PS Survivor Space']

        metrics['jvm.daemon_thread_count'] = jvm['daemon_thread_count']
        metrics['jvm.thread_count'] = jvm['thread_count']
        metrics['jvm.fd_usage'] = jvm['fd_usage']

        metrics['jvm.thread_states.timed_waiting'] = thread_st['timed_waiting']
        metrics['jvm.thread_states.runnable'] = thread_st['runnable']
        metrics['jvm.thread_states.blocked'] = thread_st['blocked']
        metrics['jvm.thread_states.waiting'] = thread_st['waiting']
        metrics['jvm.thread_states.new'] = thread_st['new']
        metrics['jvm.thread_states.terminated'] = thread_st['terminated']

        for key in metrics:
            self.publish(key, metrics[key])
