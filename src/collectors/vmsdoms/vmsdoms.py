# coding=utf-8

"""
Uses the vms suite to query per instance memory metrics, for VMS-enabled
instances

#### Dependencies

 * vms

"""

# Note, the DIAMOUND_USER has to be added to the VMS_GROUP specified
# in /etc/sysconfig/vms. VMS_GROUP may not be defined in which case it
# defaults to the login group of VMS_USER. If you are running diamond
# as root, no worries. In most other cases:
#     usermod -G kvm diamond
# should suffice

import diamond.collector
try:
    import vms
except ImportError:
    vms = None


class VMSDomsCollector(diamond.collector.Collector):
    PLUGIN_STATS = {
        'nominal': ('pages', 4096),
        'current': ('memory.current', 4096),
        'clean': ('memory.clean', 4096),
        'dirty': ('memory.dirty', 4096),
        'limit': ('memory.limit', 4096),
        'target': ('memory.target', 4096),
        'evicted': ('eviction.dropped', 4096),
        'pagedout': ('eviction.pagedout', 4096),
        'pagedin': ('eviction.pagedin', 4096),
    }

    def get_default_config_help(self):
        config_help = super(VMSDomsCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(VMSDomsCollector, self).get_default_config()
        config.update({
            'path':     'vms'
        })
        return config

    def collect(self):
        if vms is None:
            self.log.error('Unable to import vms')
            return {}

        vms.virt.init()
        hypervisor = vms.virt.AUTO.Hypervisor()

        # Get list of domains and iterate.
        domains = hypervisor.domain_list()
        vms_domains = []
        count = 0

        # Pre filter VMS domains.
        for d in domains:
            # Skip non-VMS domains.
            if not vms.control.exists(d):
                continue

            # Grab a control connection.
            dom = hypervisor.domain_lookup(d)
            if dom is None:
                continue
            ctrl = dom._wait_for_control(wait=False)
            if ctrl is None:
                continue

            try:
                # Skip ghost domains.
                if ctrl.get('gd.isghost') == '1':
                    continue
            except vms.control.ControlException:
                continue

            vms_domains.append((dom, ctrl))
            count += 1

        # Add the number of domains.
        self.publish('domains', count)

        # For each stat,
        for stat in self.PLUGIN_STATS:
            key = self.PLUGIN_STATS[stat][0]
            scale = self.PLUGIN_STATS[stat][1]
            total = 0

            # For each domain,
            for dom, ctrl in vms_domains:
                try:
                    # Get value and scale.
                    value = long(ctrl.get(key)) * scale
                except vms.control.ControlException:
                    continue

                # Dispatch.
                self.publish(stat, value, instance=dom.name())

                # Add to total.
                total = total + value

            # Dispatch total value.
            self.publish(stat, total)
