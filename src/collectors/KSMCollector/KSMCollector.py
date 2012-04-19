import os
import glob
import diamond.collector

class KSMCollector(diamond.collector.Collector):
    """
    This class collects 'Kernel Samepage Merging' statistics.
    KSM is a memory de-duplication feature of the Linux Kernel (2.6.32+).
    
    It can be enabled, if compiled into your kernel, by echoing 1 to
    /sys/kernel/mm/ksm/run. You can find more information about KSM at
    http://www.linux-kvm.org/page/KSM.
    
    Requirements: KSM built into your kernel. It does not have to be
                  enabled, but the stats will be less than useful if
                  it isn't :-)
    """
    
    def get_default_config(self):
        """
        Return default config.

        path: Graphite path output
        ksm_path: location where KSM kernel data can be found
        """
        return {
                'path': 'ksm',
                'ksm_path': '/sys/kernel/mm/ksm'
               }


    def collect(self):    
        for item in glob.glob(os.path.join(self.config['ksm_path'], "*")):
            if os.access(item, os.R_OK):
                filehandle = open(item)
                self.publish(os.path.basename(item), filehandle.readline().rstrip())
                filehandle.close()
