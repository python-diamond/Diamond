# coding=utf-8

"""
Runs third party scripts and collects their output.

Scripts need to be +x and should output metrics in the form of

```
metric.path.a 1
metric.path.b 2
metric.path.c 3
```

They are not passed any arguments and if they return an error code,
no metrics are collected.

#### Dependencies

 * [subprocess](http://docs.python.org/library/subprocess.html)
 * [kitchen](http://packages.python.org/kitchen/index.html)

"""

import diamond.collector
import diamond.convertor
import os
import sys
# Get a subprocess capable of check_output
if sys.version_info < (2, 7):
    from kitchen.pycompat27 import subprocess
else:
    import subprocess


class UserScriptsCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(UserScriptsCollector,
                            self).get_default_config_help()
        config_help.update({
            'scripts_path': "Path to find the scripts to run",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(UserScriptsCollector, self).get_default_config()
        config.update({
            'path':         '.',
            'scripts_path': '/etc/diamond/user_scripts/',
            'method':       'Threaded',
            'floatprecision': 4,
        })
        return config

    def collect(self):
        scripts_path = self.config['scripts_path']
        if not os.access(scripts_path, os.R_OK):
            return None
        for script in os.listdir(scripts_path):
            absolutescriptpath = os.path.join(scripts_path, script)
            if not os.access(absolutescriptpath, os.X_OK):
                self.log.info("%s is not executable" % absolutescriptpath)
                continue
            out = None
            self.log.debug("Executing %s" % absolutescriptpath)
            try:
                out = subprocess.check_output([absolutescriptpath])
            except subprocess.CalledProcessError, e:
                self.log.error("%s return exit value %s; skipping" %
                        (absolutescriptpath, e.returncode))
                continue
            if not out:
                self.log.info("%s return no output" % absolutescriptpath)
                continue
            # Use filter to remove empty lines of output
            for line in filter(None, out.split('\n')):
                name, value = line.split()
                floatprecision = 0
                if "." in value:
                    floatprecision = self.config['floatprecision']
                self.publish(name, value, floatprecision)
