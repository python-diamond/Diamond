# coding=utf-8

"""
Collect the solr stats for the local node

#### Dependencies

 * posixpath
 * urllib2
 * socket
 * json
 * lxml

"""

import posixpath
import urllib2
import re
import socket

try:
    import json
    json  # workaround for pyflakes issue #13
except ImportError:
    import simplejson as json

from lxml import etree as ET

import diamond.collector


class SolrCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(SolrCollector, self).get_default_config_help()
        config_help.update({
            'host': "",
            'port': "",
            'stats': "Available stats: \n"
            + " - core (Solr Core to check) \n"
            + " - scheme (Metric naming scheme, text to prepend to metric)",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(SolrCollector, self).get_default_config()
        config.update({
            'host':     '127.0.0.1',
            'port':     8983,
            'core':     None,
            'scheme':   "{0}.solr".format(socket.getfqdn()),
        })
        return config

    def _get(self, path):
        url = 'http://%s:%i/%s' % (
            self.config['host'], int(self.config['port']), path)
        try:
            return urllib2.urlopen(url)
        except Exception, err:
            self.log.error("%s: %s", url, err)
            return False

    def _get_json(self, path):
        response = self._get(path)

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
            result = self._get_json('/solr/admin/cores?action=STATUS&wt=json')
            cores = result['status'].keys()

        metrics = {}
        for core in cores:
            if core:
                path = self.config['scheme']
            else:
                path = "{0}.{1}".format(self.config['scheme'], core)

            ping_url = posixpath.normpath(
                "/solr/{0}/admin/ping?wt=json".format(core))

            result = self._get_json(ping_url)
            if not result:
                continue

            metrics.update({
                "{0}.solr.QueryTime".format(path):
                    result["responseHeader"]["QTime"],
                "{0}.solr.Status".format(path):
                    result["responseHeader"]["status"],
            })

            stats_url = posixpath.normpath(
                "/solr/{0}/admin/stats.jsp".format(core))

            result = self._get(stats_url)
            if not result:
                continue

            stats  = ET.parse(result)

            core_searcher = stats.xpath(
                '//solr/solr-info/CORE/entry'
                '[name[normalize-space()="searcher"]]/stats/stat/text()')
            standard = stats.xpath(
                '//solr/solr-info/QUERYHANDLER/entry'
                '[name[normalize-space()="standard"]]/stats/stat/text()')
            update = stats.xpath(
                '//solr/solr-info/QUERYHANDLER/entry'
                '[name[normalize-space()="/update"]]/stats/stat/text()')
            updatehandler = stats.xpath(
                '//solr/solr-info/UPDATEHANDLER/entry/stats/stat/text()')
            querycache = stats.xpath(
                '//solr/solr-info/CACHE/entry'
                '[name[normalize-space()="queryResultCache"]]'
                '/stats/stat/text()')
            documentcache = stats.xpath(
                '//solr/solr-info/CACHE/entry'
                '[name[normalize-space()="documentCache"]]/stats/stat/text()')
            filtercache = stats.xpath(
                '//solr/solr-info/CACHE/entry'
                '[name[normalize-space()="filterCache"]]/stats/stat/text()')

            metrics.update({
                "{0}.core.maxdocs".format(path):
                    core_searcher[2].strip(),
                "{0}.core.maxdocs".format(path):
                    core_searcher[3].strip(),
                "{0}.core.warmuptime".format(path):
                    core_searcher[9].strip(),

                "{0}.queryhandler.standard.requests".format(path):
                    standard[1].strip(),
                "{0}.queryhandler.standard.errors".format(path):
                    standard[2].strip(),
                "{0}.queryhandler.standard.timeouts".format(path):
                    standard[3].strip(),
                "{0}.queryhandler.standard.totaltime".format(path):
                    standard[4].strip(),
                "{0}.queryhandler.standard.timeperrequest".format(path):
                    standard[5].strip(),
                "{0}.queryhandler.standard.requestspersecond".format(path):
                    standard[6].strip(),

                "{0}.queryhandler.update.requests".format(path):
                    update[1].strip(),
                "{0}.queryhandler.update.errors".format(path):
                    update[2].strip(),
                "{0}.queryhandler.update.timeouts".format(path):
                    update[3].strip(),
                "{0}.queryhandler.update.totaltime".format(path):
                    update[4].strip(),
                "{0}.queryhandler.update.timeperrequest".format(path):
                    update[5].strip(),
                "{0}.queryhandler.update.requestspersecond".format(path):
                    standard[6].strip(),

                "{0}.queryhandler.updatehandler.commits".format(path):
                    updatehandler[0].strip(),
                "{0}.queryhandler.updatehandler.autocommits".format(path):
                    updatehandler[3].strip(),
                "{0}.queryhandler.updatehandler.optimizes".format(path):
                    updatehandler[4].strip(),
                "{0}.queryhandler.updatehandler.rollbacks".format(path):
                    updatehandler[5].strip(),
                "{0}.queryhandler.updatehandler.docspending".format(path):
                    updatehandler[7].strip(),
                "{0}.queryhandler.updatehandler.adds".format(path):
                    updatehandler[8].strip(),
                "{0}.queryhandler.updatehandler.errors".format(path):
                    updatehandler[11].strip(),
                "{0}.queryhandler.updatehandler.cumulativeadds".format(path):
                    updatehandler[12].strip(),
                "{0}.queryhandler.updatehandler.cumulativeerrors".format(path):
                    updatehandler[15].strip(),

                "{0}.queryhandler.querycache.lookups".format(path):
                    querycache[0].strip(),
                "{0}.queryhandler.querycache.hits".format(path):
                    querycache[1].strip(),
                "{0}.queryhandler.querycache.hitRatio".format(path):
                    querycache[2].strip(),
                "{0}.queryhandler.querycache.inserts".format(path):
                    querycache[3].strip(),
                "{0}.queryhandler.querycache.size".format(path):
                    querycache[5].strip(),
                "{0}.queryhandler.querycache.warmuptime".format(path):
                    querycache[6].strip(),
                "{0}.queryhandler.querycache.cumulativelookups".format(path):
                    querycache[7].strip(),
                "{0}.queryhandler.querycache.cumulativehits".format(path):
                    querycache[8].strip(),
                "{0}.queryhandler.querycache.cumulativehitratio".format(path):
                    querycache[9].strip(),
                "{0}.queryhandler.querycache.cumulativeinserts".format(path):
                    querycache[10].strip(),

                "{0}.queryhandler.documentcache.lookups".format(path):
                    documentcache[0].strip(),
                "{0}.queryhandler.documentcache.hits".format(path):
                    documentcache[1].strip(),
                "{0}.queryhandler.documentcache.hitRatio".format(path):
                    documentcache[2].strip(),
                "{0}.queryhandler.documentcache.inserts".format(path):
                    documentcache[3].strip(),
                "{0}.queryhandler.documentcache.size".format(path):
                    documentcache[5].strip(),
                "{0}.queryhandler.documentcache.warmuptime".format(path):
                    documentcache[6].strip(),
                "{0}.queryhandler.documentcache.cumulativelookups".format(path):
                    documentcache[7].strip(),
                "{0}.queryhandler.documentcache.cumulativehits".format(path):
                    documentcache[8].strip(),
                "{0}.queryhandler.documentcache.cumulativehitratio".format(path):
                    documentcache[9].strip(),
                "{0}.queryhandler.documentcache.cumulativeinserts".format(path):
                    documentcache[10].strip(),

                "{0}.queryhandler.filtercache.lookups".format(path):
                    filtercache[0].strip(),
                "{0}.queryhandler.filtercache.hits".format(path):
                    filtercache[1].strip(),
                "{0}.queryhandler.filtercache.hitRatio".format(path):
                    filtercache[2].strip(),
                "{0}.queryhandler.filtercache.inserts".format(path):
                    filtercache[3].strip(),
                "{0}.queryhandler.filtercache.size".format(path):
                    filtercache[5].strip(),
                "{0}.queryhandler.filtercache.warmuptime".format(path):
                    filtercache[6].strip(),
                "{0}.queryhandler.filtercache.cumulativelookups".format(path):
                    filtercache[7].strip(),
                "{0}.queryhandler.filtercache.cumulativehits".format(path):
                    filtercache[8].strip(),
                "{0}.queryhandler.filtercache.cumulativehitratio".format(path):
                    filtercache[9].strip(),
                "{0}.queryhandler.filtercache.cumulativeinserts".format(path):
                    documentcache[10].strip(),
            })

        for key in metrics:
            self.publish(key, metrics[key])
