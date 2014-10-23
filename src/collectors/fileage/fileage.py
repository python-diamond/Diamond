# coding=utf-8

"""
Collect the age in seconds of one or more files. An alias may be assigned
in place of the actuall file name. If no alias is included the base filename
will have dots replaced with underscores and be used as the metric name.



#### Dependencies


#### Example Configuration

FileAgeCollector.conf

```
    enabled = True
    paths = MyMetricName@/somepath/to/somefile.file, /somepath/to/somefile.file
```
"""

import diamond.collector
import os
import time
import re

class FileAgeCollector(diamond.collector.Collector):

    def __init__(self, *args, **kwargs):
        self.__totals = {}
        super(FileAgeCollector, self).__init__(*args, **kwargs)

    def get_default_config_help(self):
        config_help = super(FileAgeCollector, self).get_default_config_help()
        config_help.update({
	    'paths': 'Array of paths to collect info on.'
                     'Add an alias by prefixing with alias@',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(FileAgeCollector, self).get_default_config()
        config.update({
            'paths':     ['/tmp'],
        })
        return config

    def collect(self):
        paths = self.config.get('paths')
	if isinstance(paths, basestring):
            paths = [paths]

	for path in paths:
	    try:
		test = open(path)
            except IOError:
		self.log.error('Unable to access file: %s', path)
	        continue	
	    matches = re.search('((.+)\@)?(.+)?', path)
            alias = matches.group(2)
            file = matches.group(3)
	    if alias is None:
	    	try:
			filename = os.path.basename(path)
			alias = filename.replace (".","_")
	    	except Exception, e:
			self.log.error('Could not derive bucket name: %s', e)	
			continue
	    stats = os.stat(path)
	    fileage = (time.time()-stats.st_mtime)
	    self.publish(alias, fileage)

