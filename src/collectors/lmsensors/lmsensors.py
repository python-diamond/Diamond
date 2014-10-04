# coding=utf-8

"""
This class collects data from libsensors. It should work against libsensors 2.x
and 3.x, pending support within the PySensors Ctypes binding:
[http://pypi.python.org/pypi/PySensors/](http://pypi.python.org/pypi/PySensors/)

Requires: 'sensors' to be installed, configured, and the relevant kernel modules
to be loaded. Requires: PySensors requires Python 2.6+

If you're having issues, check your version of 'sensors'. This collector written
against: sensors version 3.1.2 with libsensors version 3.1.2

#### Dependencies

 * [PySensors](http://pypi.python.org/pypi/PySensors/)

"""

import diamond.collector

try:
    import sensors
except ImportError:
    sensors = None


class LMSensorsCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(LMSensorsCollector, self).get_default_config_help()
        config_help.update({
            'fahrenheit': "True/False",
        })
        return config_help

    def get_default_config(self):
        """
        Returns default collector settings.
        """
        config = super(LMSensorsCollector, self).get_default_config()
        config.update({
            'path': 'sensors',
            'fahrenheit': 'True'
        })
        return config

    def collect(self):
        if sensors is None:
            self.log.error('Unable to import module sensors')
            return {}

        sensors.init()
        try:
            for chip in sensors.iter_detected_chips():
                for feature in chip:
                    self.publish(".".join([str(chip),
                                           feature.label.replace(' ', '-')]),
                                 feature.get_value())
        finally:
            sensors.cleanup()
