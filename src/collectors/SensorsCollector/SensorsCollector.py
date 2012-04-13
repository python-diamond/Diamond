import diamond.collector

import sensors

class SensorsCollector(diamond.collector.Collector):
    """
    This class collects data from libsensors. It should work against libsensors 2.x and 3.x, pending
    support within the PySensors Ctypes binding: http://pypi.python.org/pypi/PySensors/

    Requires: 'sensors' to be installed, configured, and the relevant kernel modules to be loaded.
    Requires: PySensors requires Python 2.6+

    If you're having issues, check your version of 'sensors'. This collector written against:
    sensors version 3.1.2 with libsensors version 3.1.2
    """

    def get_default_config(self):
        """
        Returns default collector settings.
        """
        return {
            'enabled': 'True',
            'path': 'sensors',
            'fahrenheit': 'True'
        }

    def collect(self):
        sensors.init()
        try:
            for chip in sensors.iter_detected_chips():
                for feature in chip:
                    self.publish(".".join([str(chip), feature.label]), feature.get_value())
        finally:
            sensors.cleanup()
