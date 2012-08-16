# coding=utf-8

"""
Runs third party scripts and collects their output.

Scripts need to be +x and should output metrics in the form of

```
metric.path.a 1
metric.path.b 2
metric.path.c 3
```

They are not passed any arguments and if they return an error code, no metrics are collected.

#### Dependencies

 * [commands](http://docs.python.org/library/commands.html)

"""

import diamond.collector
import diamond.convertor
import os
import commands


class UserScriptsCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(UserScriptsCollector, self).get_default_config_help()
        config_help.update({
            'scripts_path' : "Path to find the scripts to run",
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(UserScriptsCollector, self).get_default_config()
        config.update(  {
            'path':         '.',
            'scripts_path': '/etc/diamond/user_scripts/',
            'method':       'Threaded',
        } )
        return config

    def collect(self):
        scripts_path = self.config['scripts_path']
        if not os.access(scripts_path, os.R_OK):
            return None
        for script in os.listdir(scripts_path):
            if not os.access(os.path.join(scripts_path, script), os.X_OK):
                continue
            stat, out = commands.getstatusoutput(os.path.join(scripts_path, script))
            if stat != 0:
                continue
            for line in out.split('\n'):
                name, value = line.split()
                self.publish(name, value)
