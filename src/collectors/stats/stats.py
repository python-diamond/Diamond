# coding=utf-8

"""

This is a slightly unusual 'collector'. It collects and uploads stats to a
app engine instance run by Rob Smith. The stats collected are:

 * Per collector enabled or not
 * Per collector interval time
 * Global collector reload interval
 * Global handlers
 * Any custom collector set stats

These stats are stored anonymously (other then UUID), processed and the results
are at [http://diamond-stats.appspot.com/](http://diamond-stats.appspot.com/).

These values can help us know more about how Diamond is being used and can help
us target development efforts in the future.

#### Requirements

You can install Smolt and run it once or run the following from a terminal

Linux:

 * mkdir /etc/smolt
 * cd /etc/smolt
 * cat /proc/sys/kernel/random/uuid > hw-uuid

Others:

 * mkdir /etc/smolt
 * cd /etc/smolt
 * curl -Lo- http://utils.kormoc.com/uuid/get.php > hw-uuid

#### Dependencies

 * /etc/smolt/hw-uuid
 * urllib
 * json/simplejson

"""

from diamond.collector import Collector
from diamond.util import get_diamond_version
import diamond

import urllib
import os
import sys
import platform

try:
    import json
    json  # workaround for pyflakes issue #13
except ImportError:
    import simplejson as json


def getIncludePaths(path):
    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))

        if os.path.isfile(cPath) and len(f) > 3 and f[-3:] == '.py':
            sys.path.append(os.path.dirname(cPath))

    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))
        if os.path.isdir(cPath):
            getIncludePaths(cPath)

collectors = {}


def getCollectors(path):
    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))

        if (os.path.isfile(cPath)
                and len(f) > 3
                and f[-3:] == '.py'
                and f[0:4] != 'test'):
            modname = f[:-3]
            try:
                # Import the module
                module = __import__(modname, globals(), locals(), ['*'])

                # Find the name
                for attr in dir(module):
                    cls = getattr(module, attr)
                    try:
                        if (issubclass(cls, Collector)
                                and cls.__name__ not in collectors):
                            collectors[cls.__name__] = module
                            break
                    except TypeError:
                        continue
            except Exception:
                collectors[modname] = False
                continue

    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))
        if os.path.isdir(cPath):
            getCollectors(cPath)


class StatsCollector(diamond.collector.Collector):
    full_config = None

    def __init__(self, config, handlers):
        self.full_config = config
        super(StatsCollector, self).__init__(config, handlers)

    def get_default_config_help(self):
        config_help = super(StatsCollector, self).get_default_config_help()
        config_help.update({
            'url': 'The url to post stats to.',
            'uuidfile': 'The path to the uuid file'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(StatsCollector, self).get_default_config()
        config.update({
            'url': 'http://diamond-stats.appspot.com/submitstats',
            'uuidfile': '/etc/smolt/hw-uuid',
            'interval': 604800,
        })
        return config

    def collect(self):
        getIncludePaths(self.full_config['server']['collectors_path'])
        getCollectors(self.full_config['server']['collectors_path'])

        stats = {}

        stats['version'] = get_diamond_version()
        stats['python_version'] = platform.python_version()

        if platform.system() == 'Darwin':
            ver = platform.mac_ver()
            os_version = ('Darwin', ver[0], '')

        elif platform.system() == 'Linux':
            os_version = platform.linux_distribution()

        elif platform.system() == 'Windows':
            ver = platform.win32_ver()
            os_version = ('Windows', ver[0], ver[2])

        stats['os'] = "%s %s" % (os_version[0], os_version[1])
        stats['os_distname'] = os_version[0]
        stats['os_version'] = os_version[1]
        stats['os_id'] = os_version[2]

        uuid_file = open(self.config['uuidfile'])
        stats['uuid'] = uuid_file.read().strip()
        uuid_file.close()

        stats['collectors'] = {}

        stats['collectors']['Default'] = self.get_stats_for_upload(
            config=self.full_config['collectors']['default'])

        for collector in collectors:
            if not hasattr(collectors[collector], collector):
                continue

            cls = getattr(collectors[collector], collector)
            obj = cls(config=self.full_config, handlers={})
            stats['collectors'][collector] = obj.get_stats_for_upload()

        stats['collectors']['StatsCollector'] = self.get_stats_for_upload()

        stats['server'] = {}

        if type(self.full_config['server']['handlers']) is list:
            handlers = self.full_config['server']['handlers']
        else:
            handlers = self.full_config['server']['handlers'].split(',')
        stats['server']['handlers'] = handlers

        reload_i = self.full_config['server']['collectors_reload_interval']
        stats['server']['collectors_reload_interval'] = reload_i

        hmeth = 'Default'
        if 'hostname_method' in self.full_config['collectors']['default']:
            hmeth = self.full_config['collectors']['default']['hostname_method']
        stats['server']['hostname_method'] = hmeth

        data = urllib.urlencode({'stats': json.dumps(stats)})
        f = urllib.urlopen(self.config['url'], data)
        f.read()
        f.close()

        return True
