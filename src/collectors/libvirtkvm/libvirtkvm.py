# coding=utf-8

"""
Uses libvirt to harvest per KVM instance stats

#### Dependencies

 * python-libvirt, xml

"""

import diamond.collector

try:
    from xml.etree import ElementTree
except ImportError:
    import cElementTree as ElementTree

try:
    import libvirt
except ImportError:
    libvirt = None


class LibvirtKVMCollector(diamond.collector.Collector):
    blockStats = {
        'read_reqs':   0,
        'read_bytes':  1,
        'write_reqs':  2,
        'write_bytes': 3
        }

    vifStats = {
        'rx_bytes':   0,
        'rx_packets': 1,
        'rx_errors':  2,
        'rx_drops':   3,
        'tx_bytes':   4,
        'tx_packets': 5,
        'tx_errors':  6,
        'tx_drops':   7
        }

    def get_default_config_help(self):
        config_help = super(LibvirtKVMCollector, self).get_default_config_help()
        config_help.update({
            'uri': """The libvirt connection URI. By default it's
'qemu:///system'. One decent option is
'qemu+unix:///system?socket=/var/run/libvirt/libvit-sock-ro'.""",
            'sort_by_uuid': """Use the <uuid> of the instance instead of the
 default <name>, useful in Openstack deploments where <name> is only
specific to the compute node""",
            'cpu_absolute': """CPU stats reported as percentage by default, or
as cummulative nanoseconds since VM creation if this is True."""
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(LibvirtKVMCollector, self).get_default_config()
        config.update({
            'path':     'libvirt-kvm',
            'sort_by_uuid': False,
            'uri':      'qemu:///system',
            'cpu_absolute': False
        })
        return config

    def get_devices(self, dom, type):
        devices = []

        # Create a XML tree from the domain XML description.
        tree = ElementTree.fromstring(dom.XMLDesc(0))

        for target in tree.findall("devices/%s/target" % type):
            dev = target.get("dev")
            if not dev in devices:
                devices.append(dev)

        return devices

    def get_disk_devices(self, dom):
        return self.get_devices(dom, 'disk')

    def get_network_devices(self, dom):
        return self.get_devices(dom, 'interface')

    def report_cpu_metric(self, statname, value, instance):
        # Value in cummulative nanoseconds
        if self.config['cpu_absolute'] is True:
            metric = value
        else:
            # Nanoseconds (10^9), however, we want to express in 100%
            metric = self.derivative(statname, float(value) / 10000000.0,
                                     max_value=diamond.collector.MAX_COUNTER,
                                     instance=instance)
        self.publish(statname, metric, instance=instance)

    def collect(self):
        if libvirt is None:
            self.log.error('Unable to import libvirt')
            return {}

        conn = libvirt.openReadOnly(self.config['uri'])
        for dom in [conn.lookupByID(n) for n in conn.listDomainsID()]:
            if self.config['sort_by_uuid'] is True:
                name = dom.UUIDString()
            else:
                name = dom.name()

            # CPU stats
            vcpus = dom.getCPUStats(True, 0)
            totalcpu = 0
            idx = 0
            for vcpu in vcpus:
                cputime = vcpu['cpu_time']
                self.report_cpu_metric('cpu.%s.time' % idx, cputime, name)
                idx += 1
                totalcpu += cputime
            self.report_cpu_metric('cpu.total.time', totalcpu, name)

            # Disk stats
            disks = self.get_disk_devices(dom)
            accum = {}
            for stat in self.blockStats.keys():
                accum[stat] = 0

            for disk in disks:
                stats = dom.blockStats(disk)
                for stat in self.blockStats.keys():
                    idx = self.blockStats[stat]
                    val = stats[idx]
                    accum[stat] += val
                    self.publish('block.%s.%s' % (disk, stat), val,
                                 instance=name)
            for stat in self.blockStats.keys():
                self.publish('block.total.%s' % stat, accum[stat],
                             instance=name)

            # Network stats
            vifs = self.get_network_devices(dom)
            accum = {}
            for stat in self.vifStats.keys():
                accum[stat] = 0

            for vif in vifs:
                stats = dom.interfaceStats(vif)
                for stat in self.vifStats.keys():
                    idx = self.vifStats[stat]
                    val = stats[idx]
                    accum[stat] += val
                    self.publish('net.%s.%s' % (vif, stat), val,
                                 instance=name)
            for stat in self.vifStats.keys():
                self.publish('net.total.%s' % stat, accum[stat],
                             instance=name)

            # Memory stats
            mem = dom.memoryStats()
            self.publish('memory.nominal', mem['actual'] * 1024,
                         instance=name)
            self.publish('memory.rss', mem['rss'] * 1024, instance=name)
