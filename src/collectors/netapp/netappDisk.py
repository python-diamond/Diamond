""" This collector retrieves disk information from netapp filers

    !Thread-safe!

    The following metrics are measured in this diamond collector:
        * Number of disk in spare pool and not zeroed.
        * Number of spare disks per disk type, ie SAS/SATA
        * Number of disk in 'maintenance center'
        * monitor CP
        * Monitor average disk busyness per aggregate.

        Config File:
            [devices]
            [[filer-corp-201]] <--- You can have as many filers as you want!
            ip = 192.168.1.45
            user = netapp_monitor
            password = b0bl0rd!

"""

import diamond.collector
import time
from diamond.metric import Metric

try:
    import xml.etree.ElementTree as ET
except ImportError:
    import cElementTree as ET

try:
    from netappsdk.NaServer import *
    from netappsdk.NaElement import *
    netappsdk = 0
except ImportError:
    netappsdk = 1

__author__ = 'peter@phyn3t.com'


class netappDiskCol(object):
    """ Our netappDisk Collector
    """

    def __init__(self, device, ip, user, password, parent):
        """ Collectors our metrics for our netapp filer
        """

        self.device = device
        self.ip = ip
        self.netapp_user = user
        self.netapp_password = password
        self.path_prefix = parent[0]
        self.publish_metric = parent[1]
        self.log = parent[2]
        self._netapp_login()

        # Grab our netapp XML
        disk_xml = self.get_netapp_elem(
            NaElement('disk-list-info'), 'disk-details')
        storage_disk_xml = self.get_netapp_elem(
            NaElement('storage-disk-get-iter'), 'attributes-list')

        # Our metric collection and publishing goes here
        self.zero_disk(disk_xml)
        self.spare_disk(disk_xml)
        self.maintenance_center(storage_disk_xml)
        self.consistency_point()
        self.agr_busy()

    def agr_busy(self):
        """ Collector for average disk busyness per aggregate

            As of Nov 22nd 2013 there is no API call for agr busyness.
            You have to collect all disk busyness and then compute agr
            busyness. #fml

        """

        c1 = {}  # Counters from time a
        c2 = {}  # Counters from time b
        disk_results = {}  # Disk busyness results %
        agr_results = {}  # Aggregate busyness results $
        names = ['disk_busy', 'base_for_disk_busy', 'raid_name',
                 'base_for_disk_busy', 'instance_uuid']
        netapp_api = NaElement('perf-object-get-instances')
        netapp_api.child_add_string('objectname', 'disk')
        disk_1 = self.get_netapp_elem(netapp_api, 'instances')
        time.sleep(1)
        disk_2 = self.get_netapp_elem(netapp_api, 'instances')

        for instance_data in disk_1:
            temp = {}
            for element in instance_data.findall(".//counters/counter-data"):
                if element.find('name').text in names:
                    temp[element.find('name').text] = element.find('value').text

            agr_name = temp['raid_name']
            agr_name = agr_name[agr_name.find('/', 0):agr_name.find('/', 1)]
            temp['raid_name'] = agr_name.lstrip('/')
            c1[temp.pop('instance_uuid')] = temp

        for instance_data in disk_2:
            temp = {}
            for element in instance_data.findall(".//counters/counter-data"):
                if element.find('name').text in names:
                    temp[element.find('name').text] = element.find('value').text

            agr_name = temp['raid_name']
            agr_name = agr_name[agr_name.find('/', 0):agr_name.find('/', 1)]
            temp['raid_name'] = agr_name.lstrip('/')
            c2[temp.pop('instance_uuid')] = temp

        for item in c1:
            t_c1 = int(c1[item]['disk_busy'])  # time_counter_1
            t_b1 = int(c1[item]['base_for_disk_busy'])  # time_base_1
            t_c2 = int(c2[item]['disk_busy'])
            t_b2 = int(c2[item]['base_for_disk_busy'])

            disk_busy = 100 * (t_c2 - t_c1) / (t_b2 - t_b1)

            if c1[item]['raid_name'] in disk_results:
                disk_results[c1[item]['raid_name']].append(disk_busy)
            else:
                disk_results[c1[item]['raid_name']] = [disk_busy]

        for aggregate in disk_results:
            agr_results[aggregate] = \
                sum(disk_results[aggregate]) / len(disk_results[aggregate])

        for aggregate in agr_results:
            self.push('avg_busy', 'aggregate.' + aggregate,
                      agr_results[aggregate])

    def consistency_point(self):
        """ Collector for getting count of consistancy points
        """

        cp_delta = {}
        xml_path = 'instances/instance-data/counters'
        netapp_api = NaElement('perf-object-get-instances')
        netapp_api.child_add_string('objectname', 'wafl')
        instance = NaElement('instances')
        instance.child_add_string('instance', 'wafl')
        counter = NaElement('counters')
        counter.child_add_string('counter', 'cp_count')
        netapp_api.child_add(counter)
        netapp_api.child_add(instance)

        cp_1 = self.get_netapp_elem(netapp_api, xml_path)
        time.sleep(3)
        cp_2 = self.get_netapp_elem(netapp_api, xml_path)

        for element in cp_1:
            if element.find('name').text == 'cp_count':
                cp_1 = element.find('value').text.rsplit(',')
                break
        for element in cp_2:
            if element.find('name').text == 'cp_count':
                cp_2 = element.find('value').text.rsplit(',')
                break

        if not type(cp_2) is list or not type(cp_1) is list:
            log.error("consistency point data not available for filer: %s"
                      % self.device)
            return

        cp_1 = {
            'wafl_timer': cp_1[0],
            'snapshot': cp_1[1],
            'wafl_avail_bufs': cp_1[2],
            'dirty_blk_cnt': cp_1[3],
            'full_nv_log': cp_1[4],
            'b2b': cp_1[5],
            'flush_gen': cp_1[6],
            'sync_gen': cp_1[7],
            'def_b2b': cp_1[8],
            'con_ind_pin': cp_1[9],
            'low_mbuf_gen': cp_1[10],
            'low_datavec_gen': cp_1[11]
        }

        cp_2 = {
            'wafl_timer': cp_2[0],
            'snapshot': cp_2[1],
            'wafl_avail_bufs': cp_2[2],
            'dirty_blk_cnt': cp_2[3],
            'full_nv_log': cp_2[4],
            'b2b': cp_2[5],
            'flush_gen': cp_2[6],
            'sync_gen': cp_2[7],
            'def_b2b': cp_2[8],
            'con_ind_pin': cp_2[9],
            'low_mbuf_gen': cp_2[10],
            'low_datavec_gen': cp_2[11]
        }

        for item in cp_1:
            c1 = int(cp_1[item])
            c2 = int(cp_2[item])
            cp_delta[item] = c2 - c1

        for item in cp_delta:
            self.push(item + '_CP', 'system.system', cp_delta[item])

    def maintenance_center(self, storage_disk_xml=None):
        """ Collector for how many disk(s) are in NetApp maintenance center

            For more information on maintenance center please see:
              bit.ly/19G4ptr

        """

        disk_in_maintenance = 0

        for filer_disk in storage_disk_xml:
            disk_status = filer_disk.find('disk-raid-info/container-type')
            if disk_status.text == 'maintenance':
                disk_in_maintenance += 1

        self.push('maintenance_disk', 'disk', disk_in_maintenance)

    def zero_disk(self, disk_xml=None):
        """ Collector and publish not zeroed disk metrics
        """

        troubled_disks = 0
        for filer_disk in disk_xml:
            raid_state = filer_disk.find('raid-state').text
            if not raid_state == 'spare':
                continue
            is_zeroed = filer_disk.find('is-zeroed').text

            if is_zeroed == 'false':
                troubled_disks += 1
        self.push('not_zeroed', 'disk', troubled_disks)

    def spare_disk(self, disk_xml=None):
        """ Number of spare disk per type.

            For example: storage.ontap.filer201.disk.SATA

        """

        spare_disk = {}
        disk_types = set()

        for filer_disk in disk_xml:
            disk_types.add(filer_disk.find('effective-disk-type').text)
            if not filer_disk.find('raid-state').text == 'spare':
                continue

            disk_type = filer_disk.find('effective-disk-type').text
            if disk_type in spare_disk:
                spare_disk[disk_type] += 1
            else:
                spare_disk[disk_type] = 1

        for disk_type in disk_types:
            if disk_type in spare_disk:
                self.push('spare_' + disk_type, 'disk', spare_disk[disk_type])
            else:
                self.push('spare_' + disk_type, 'disk', 0)

    def get_netapp_elem(self, netapp_api=None, sub_element=None):
        """ Retrieve netapp elem
        """

        netapp_data = self.server.invoke_elem(netapp_api)

        if netapp_data.results_status() == 'failed':
            self.log.error(
                'While using netapp API failed to retrieve '
                'disk-list-info for netapp filer %s' % self.device)
            print netapp_data.sprintf()
            return
        netapp_xml = \
            ET.fromstring(netapp_data.sprintf()).find(sub_element)

        return netapp_xml

    def _netapp_login(self):
        """ Login to our netapp filer
        """

        self.server = NaServer(self.ip, 1, 3)
        self.server.set_transport_type('HTTPS')
        self.server.set_style('LOGIN')
        self.server.set_admin_user(self.netapp_user, self.netapp_password)

    def push(self, metric_name=None, type=None, metric_value=None):
        """ Ship that shit off to graphite broski
        """

        graphite_path = self.path_prefix
        graphite_path += '.' + self.device + '.' + type
        graphite_path += '.' + metric_name

        metric = Metric(
            graphite_path,
            metric_value,
            precision=4,
            host=self.device)

        self.publish_metric(metric)


class netappDisk(diamond.collector.Collector):
    """ Netapp disk diamond scheduler
    """

    running = set()

    def collect(self, device, ip, user, password):
        """ Collectors our metrics for our netapp filer --START HERE--
        """

        if netappsdk:
            self.log.error(
                'Failed to import netappsdk.NaServer or netappsdk.NaElement')
            return

        if device in self.running:
            return

        self.running.add(device)
        parent = (self.config['path_prefix'], self.publish_metric, self.log)

        netappDiskCol(device, ip, user, password, parent)
        self.running.remove(device)
