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

"""

import diamond.collector
import diamond.convertor
import os
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
            'floatprecision': 4,
        })
        return config

    def collect(self):
        scripts_path = self.config['scripts_path']
        if not os.access(scripts_path, os.R_OK):
            return None
        for script in os.listdir(scripts_path):
            absolutescriptpath = os.path.join(scripts_path, script)
            executable = os.access(absolutescriptpath, os.X_OK)
            is_file = os.path.isfile(absolutescriptpath)
            if is_file:
                if not executable:
                    self.log.info("%s is not executable" % absolutescriptpath)
                    continue
            else:
                # Don't bother logging skipped non-file files (typically
                # directories)
                continue
            out = None
            self.log.debug("Executing %s" % absolutescriptpath)
            try:
                proc = subprocess.Popen([absolutescriptpath],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                (out, err) = proc.communicate()
            except subprocess.CalledProcessError, e:
                self.log.error("%s error launching: %s; skipping" %
                               (absolutescriptpath, e))
                continue
            if proc.returncode:
                self.log.error("%s return exit value %s; skipping" %
                               (absolutescriptpath, proc.returncode))
            if not out:
                self.log.info("%s return no output" % absolutescriptpath)
                continue
            if err:
                self.log.error("%s return error output: %s" %
                               (absolutescriptpath, err))
            # Use filter to remove empty lines of output
            for line in filter(None, out.split('\n')):
                # Ignore invalid lines
                try:
                    name, value = line.split()
                    float(value)
                except ValueError:
                    self.log.error("%s returned error output: %s" %
                                   (absolutescriptpath, line))
                    continue
                name, value = line.split()
                floatprecision = 0
                if "." in value:
                    floatprecision = self.config['floatprecision']
                self.publish(name, value, precision=floatprecision)
