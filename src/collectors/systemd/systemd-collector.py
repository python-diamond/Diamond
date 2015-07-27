# coding=utf-8

"""
Custom collector for systemd process control system
(http://www.freedesktop.org/wiki/Software/systemd/)
#### Dependencies
 * python-systemd
 * diamond
#### Usage
<pre>
services = nginx,ntpd
</pre>
"""

from diamond.collector import Collector
from systemd.manager import Manager
from systemd.exceptions import SystemdError


class SystemdCollector(Collector):

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(SystemdCollector, self).get_default_config()
        config.update({
            'services': '',
        })
        return config

    def collect(self):

        try:

            manager = Manager()

            for service in [s.strip() for s in self.config['services']]:

                if not service:
                    continue

                try:
                    unit = manager.get_unit('%s.service' % service)
                    self.publish("%s.running" % service, 1
                                 if str(unit.properties.SubState) == "running"
                                 else 0)
                except SystemdError, e:
                    self.log.exception(e)

        finally:

            manager.unsubscribe()
