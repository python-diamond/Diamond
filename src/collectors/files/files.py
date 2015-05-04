# coding=utf-8

"""
This class collects data from plain text files

#### Dependencies

"""

import diamond.collector
import os
import re

_RE = re.compile(r'([A-Za-z0-9._-]+)[\s=:]+(-?[0-9]+)(\.?\d*)')


class FilesCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(FilesCollector, self).get_default_config_help()
        config_help.update({
            'path': 'Prefix added to all stats collected by this module, a '
                    'single dot means don''t add prefix',
            'dir': 'The directory that the performance files are in',
            'delete': 'Delete files after they are picked up',
        })
        return config_help

    def get_default_config(self):
        """
        Returns default collector settings.
        """
        config = super(FilesCollector, self).get_default_config()
        config.update({
            'path': '.',
            'dir': '/tmp/diamond',
            'delete': False,
        })
        return config

    def collect(self):
        if os.path.exists(self.config['dir']):
            for fn in os.listdir(self.config['dir']):
                if os.path.isfile(os.path.join(self.config['dir'], fn)):
                    try:
                        fh = open(os.path.join(self.config['dir'], fn))
                        found = False
                        for line in fh:
                            m = _RE.match(line)
                            if (m):
                                self.publish(
                                    m.groups()[0],
                                    m.groups()[1] + m.groups()[2],
                                    precision=max(0, len(m.groups()[2]) - 1))
                                found = True
                        fh.close()
                        if (found and self.config['delete']):
                            os.unlink(os.path.join(self.config['dir'], fn))
                    except:
                        pass
