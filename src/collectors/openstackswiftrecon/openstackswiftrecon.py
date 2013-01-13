# coding=utf-8

"""
Openstack Swift Recon collector. Reads any present recon cache files and
reports their current metrics.

#### Dependencies

 * Running Swift services must have a recon enabled

"""

import os
try:
    import json
    json  # workaround for pyflakes issue #13
except ImportError:
    import simplejson as json

import diamond.collector


class OpenstackSwiftReconCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(OpenstackSwiftReconCollector,
                            self).get_default_config_help()
        config_help.update({
            'recon_account_cache': 'path to swift recon account cache '
            '(default /var/cache/swift/account.recon)',
            'recon_container_cache': 'path to swift recon container cache '
            '(default /var/cache/swift/container.recon)',
            'recon_object_cache': 'path to swift recon object cache '
            '(default /var/cache/swift/object.recon)'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(OpenstackSwiftReconCollector, self).get_default_config()
        config.update({
            'path': 'swiftrecon',
            'recon_account_cache': '/var/cache/swift/account.recon',
            'recon_container_cache': '/var/cache/swift/container.recon',
            'recon_object_cache': '/var/cache/swift/object.recon',
            'method': 'Threaded',
            'interval': 300,
        })
        return config

    def _process_cache(self, d, path=()):
        """Recusively walk a nested recon cache dict to obtain path/values"""
        for k, v in d.iteritems():
            if not isinstance(v, dict):
                self.metrics.append((path + (k,), v))
            else:
                self._process_cache(v, path + (k,))

    def collect(self):
        self.metrics = []
        recon_cache = {'account': self.config['recon_account_cache'],
                       'container': self.config['recon_container_cache'],
                       'object': self.config['recon_object_cache']}
        for recon_type in recon_cache:
            if not os.access(recon_cache[recon_type], os.R_OK):
                continue
            try:
                f = open(recon_cache[recon_type])
                try:
                    rmetrics = json.loads(f.readlines()[0].strip())
                    self.metrics = []
                    self._process_cache(rmetrics)
                    for k, v in self.metrics:
                        metric_name = '%s.%s' % (recon_type, ".".join(k))
                        if isinstance(v, (int, float)):
                            self.publish(metric_name, v)
                except (ValueError, IndexError):
                    continue
            finally:
                f.close()
