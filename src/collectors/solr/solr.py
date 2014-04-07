# coding=utf-8

"""
Collect the solr stats for the local node

#### Dependencies

 * posixpath
 * urllib2
 * json

"""

import posixpath
import urllib2
import re

try:
    import json
    json  # workaround for pyflakes issue #13
except ImportError:
    import simplejson as json

import diamond.collector


class SolrCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(SolrCollector, self).get_default_config_help()
        config_help.update({
            'host': "",
            'port': "",
            'stats': "Available stats: \n"
            " - jvm (JVM information) \n"
            " - core (Core stats)\n"
            " - scheme (Individual index stats)\n",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(SolrCollector, self).get_default_config()
        config.update({
            'host':     'localhost',
            'port':     8983,
            'core':     None,
            'scheme':   "solr",
        })
        return config

    def _try_convert(self, value):
        if isinstance(value, (int, float)):
            return value
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            return value

    def _get(self, path):
        url = 'http://%s:%i/%s' % (
            self.config['host'], int(self.config['port']), path)
        try:
            return urllib2.urlopen(url)
        except Exception, err:
            self.log.error("%s: %s", url, err)
            return False

        try:
            return json.load(response)
        except (TypeError, ValueError):
            self.log.error("Unable to parse response from solr as a"
                           " json object")
            return False

    def collect(self):
        if json is None:
            self.log.error('Unable to import json')
            return {}

        cores = []
        if self.config['core']:
            cores = [self.config['core']]
        else:
            # If no core is specified, provide statistics for all cores
            result = self._get('/solr/admin/cores?action=STATUS&wt=json')
            cores = result['status'].keys()

        metrics = {}
        for core in cores:
            if core:
                path = self.config['scheme']
            else:
                path = "{0}.{1}".format(self.config['scheme'], core)

            ping_url = posixpath.normpath(
                "/solr/{0}/admin/ping?wt=json".format(core))

            result = self._get(ping_url)
            if not result:
                continue

            metrics.update({
                "{0}.response.QueryTime".format(path):
                    result["responseHeader"]["QTime"],
                "{0}.response.Status".format(path):
                    result["responseHeader"]["status"],
            })

            stats_url = posixpath.normpath(
                "/solr/{0}/admin/mbeans?stats=true&wt=json".format(core))

            result = self._get(stats_url)
            if not result:
                continue

            s = result['solr-mbeans']
            stats = dict((s[i], s[i+1]) for i in xrange(0, len(s), 2))

            core_searcher = stats["CORE"]["searcher"]["stats"]
            standard = stats["QUERYHANDLER"]["standard"]["stats"]
            update = stats["QUERYHANDLER"]["/update"]["stats"]
            updatehandler = stats["UPDATEHANDLER"]["updateHandler"]["stats"]
            cache = stats["CACHE"]

            metrics.update([
                ("{0}.core.{1}".format(path, key),
                 core_searcher[key])
                for key in ("maxDoc", "numDocs", "warmupTime")
            ])

            metrics.update([
                ("{0}.queryhandler.standard.{1}".format(path, key),
                 standard[key])
                for key in ("requests", "errors", "timeouts", "totalTime",
                            "avgTimePerRequest", "avgRequestsPerSecond")
            ])

            metrics.update([
                ("{0}.queryhandler.update.{1}".format(path, key),
                 update[key])
                for key in ("requests", "errors", "timeouts", "totalTime",
                            "avgTimePerRequest", "avgRequestsPerSecond")
                if update[key] != 'NaN'
            ])

            metrics.update([
                ("{0}.updatehandler.{1}".format(path, key),
                 updatehandler[key]), for key in (
                     "commits", "autocommits", "optimizes", "rollbacks",
                     "docsPending", "adds", "errors", "cumulative_adds",
                     "cumulative_errors")
            ])

            metrics.update([
                ("{0}.cache.{1}.{2}".format(path, cache_type, key),
                 self._try_convert(cache[cache_type]['stats'][key]))
                for cache_type in (
                     u'fieldValueCache', u'filterCache',
                     u'documentCache', u'queryResultCache')
                for key in (
                    u'lookups', u'hits', u'hitratio', u'inserts',
                    u'evictions', u'size', u'warmupTime',
                    u'cumulative_lookups', u'cumulative_hits',
                    u'cumulative_hitratio', u'cumulative_inserts',
                    u'cumulative_evictions')
            ])

            system_url = posixpath.normpath(
                "/solr/{0}/admin/system?stats=true&wt=json".format(core))

            result = self._get(system_url)
            if not result:
                continue

            mem = result['jvm']['memory']
            metrics.update([
                ('{0}.jvm.mem.{1}'.format(path, key),
                 self._try_convert(mem[key].split()[0]))
                for k in ('free', 'total', 'max', 'used')
            ])

        for key in metrics:
            self.publish(key, metrics[key])
