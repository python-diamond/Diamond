# coding=utf-8

"""
The OneWireCollector collects data from 1-Wire Filesystem

You can configure which sensors are read in two way:

-  add section [scan] with attributes and aliases,
   (collector will scan owfs to find attributes)

or

- add sections with format id:$SENSOR_ID

See also: http://owfs.org/
Author: Tomasz Prus

#### Dependencies

 * owfs

"""

import os
import diamond.collector


class OneWireCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(OneWireCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(OneWireCollector, self).get_default_config()
        config.update({
            'path': 'owfs',
            'owfs': '/mnt/1wire',
            #'scan': {'temperature': 't'},
            #'id:24.BB000000': {'file_with_value': 'alias'},
        })
        return config

    def collect(self):
        """
        Overrides the Collector.collect method
        """

        metrics = {}

        if 'scan' in self.config:
            for ld in os.listdir(self.config['owfs']):
                if '.' in ld:
                    self.read_values(ld, self.config['scan'], metrics)

        for oid, files in self.config.iteritems():
            if oid[:3] == 'id:':
                self.read_values(oid[3:], files, metrics)

        for fn, fv in metrics.iteritems():
            self.publish(fn, fv, 2)

    def read_values(self, oid, files, metrics):
        """
        Reads values from owfs/oid/{files} and update
        metrics with format [oid.alias] = value
        """

        oid_path = os.path.join(self.config['owfs'], oid)
        oid = oid.replace('.', '_')

        for fn, alias in files.iteritems():
            fv = os.path.join(oid_path, fn)
            if os.path.isfile(fv):
                try:
                    f = open(fv)
                    v = f.read()
                    f.close()
                except:
                    self.log.error("Unable to read %s", fv)
                    raise

                try:
                    v = float(v)
                except:
                    self.log.error("Unexpected value %s in %s", v, fv)
                    raise

                metrics["%s.%s" % (oid, alias)] = v
