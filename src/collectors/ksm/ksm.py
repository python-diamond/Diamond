# coding=utf-8

"""
This class collects 'Kernel Samepage Merging' statistics.
KSM is a memory de-duplication feature of the Linux Kernel (2.6.32+).

It can be enabled, if compiled into your kernel, by echoing 1 to
/sys/kernel/mm/ksm/run. You can find more information about KSM at
[http://www.linux-kvm.org/page/KSM](http://www.linux-kvm.org/page/KSM).

#### Dependencies

 * KSM built into your kernel. It does not have to be enabled, but the stats
 will be less than useful if it isn't:-)

"""

import os
import glob
import diamond.collector


class KSMCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(KSMCollector, self).get_default_config_help()
        config_help.update({
            'ksm_path': "location where KSM kernel data can be found",
        })
        return config_help

    def get_default_config(self):
        """
        Return default config.

        path: Graphite path output
        ksm_path: location where KSM kernel data can be found
        """
        config = super(KSMCollector, self).get_default_config()
        config.update({
            'path': 'ksm',
            'ksm_path': '/sys/kernel/mm/ksm'})
        return config

    def collect(self):
        for item in glob.glob(os.path.join(self.config['ksm_path'], "*")):
            if os.access(item, os.R_OK):
                filehandle = open(item)
                try:
                    self.publish(os.path.basename(item),
                                 float(filehandle.readline().rstrip()))
                except ValueError:
                    pass
                filehandle.close()
