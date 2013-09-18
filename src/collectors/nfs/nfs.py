# coding=utf-8

"""
The NfsCollector collects nfs utilization metrics using /proc/net/rpc/nfs.

#### Dependencies

 * /proc/net/rpc/nfs

"""

import diamond.collector
import os


class NfsCollector(diamond.collector.Collector):

    PROC = '/proc/net/rpc/nfs'

    def get_default_config_help(self):
        config_help = super(NfsCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(NfsCollector, self).get_default_config()
        config.update({
            'enabled':  False,
            'path':     'nfs'
        })
        return config

    def collect(self):
        """
        Collect stats
        """
        if os.access(self.PROC, os.R_OK):

            results = {}
            # Open file
            file = open(self.PROC)

            for line in file:
                line = line.split()

                if line[0] == 'net':
                    results['net.packets'] = line[1]
                    results['net.udpcnt'] = line[2]
                    results['net.tcpcnt'] = line[3]
                    results['net.tcpconn'] = line[4]
                elif line[0] == 'rpc':
                    results['rpc.calls'] = line[1]
                    results['rpc.retrans'] = line[2]
                    results['rpc.authrefrsh'] = line[3]
                elif line[0] == 'proc2':
                    results['v2.null'] = line[1]
                    results['v2.getattr'] = line[2]
                    results['v2.setattr'] = line[3]
                    results['v2.root'] = line[4]
                    results['v2.lookup'] = line[5]
                    results['v2.readlink'] = line[6]
                    results['v2.read'] = line[7]
                    results['v2.wrcache'] = line[8]
                    results['v2.write'] = line[9]
                    results['v2.create'] = line[10]
                    results['v2.remove'] = line[11]
                    results['v2.rename'] = line[12]
                    results['v2.link'] = line[13]
                    results['v2.symlink'] = line[14]
                    results['v2.mkdir'] = line[15]
                    results['v2.rmdir'] = line[16]
                    results['v2.readdir'] = line[17]
                    results['v2.fsstat'] = line[18]
                elif line[0] == 'proc3':
                    results['v3.null'] = line[1]
                    results['v3.getattr'] = line[2]
                    results['v3.setattr'] = line[3]
                    results['v3.lookup'] = line[4]
                    results['v3.access'] = line[5]
                    results['v3.readlink'] = line[6]
                    results['v3.read'] = line[7]
                    results['v3.write'] = line[8]
                    results['v3.create'] = line[9]
                    results['v3.mkdir'] = line[10]
                    results['v3.symlink'] = line[11]
                    results['v3.mknod'] = line[12]
                    results['v3.remove'] = line[13]
                    results['v3.rmdir'] = line[14]
                    results['v3.rename'] = line[15]
                    results['v3.link'] = line[16]
                    results['v3.readdir'] = line[17]
                    results['v3.readdirplus'] = line[18]
                    results['v3.fsstat'] = line[19]
                    results['v3.fsinfo'] = line[20]
                    results['v3.pathconf'] = line[21]
                    results['v3.commit'] = line[22]
                elif line[0] == 'proc4':
                    results['v4.null'] = line[1]
                    results['v4.read'] = line[2]
                    results['v4.write'] = line[3]
                    results['v4.commit'] = line[4]
                    results['v4.open'] = line[5]
                    results['v4.open_conf'] = line[6]
                    results['v4.open_noat'] = line[7]
                    results['v4.open_dgrd'] = line[8]
                    results['v4.close'] = line[9]
                    results['v4.setattr'] = line[10]
                    results['v4.fsinfo'] = line[11]
                    results['v4.renew'] = line[12]
                    results['v4.setclntid'] = line[13]
                    results['v4.confirm'] = line[14]
                    results['v4.lock'] = line[15]
                    results['v4.lockt'] = line[16]
                    results['v4.locku'] = line[17]
                    results['v4.access'] = line[18]
                    results['v4.getattr'] = line[19]
                    results['v4.lookup'] = line[20]
                    results['v4.lookup_root'] = line[21]
                    results['v4.remove'] = line[22]
                    results['v4.rename'] = line[23]
                    results['v4.link'] = line[24]
                    results['v4.symlink'] = line[25]
                    results['v4.create'] = line[26]
                    results['v4.pathconf'] = line[27]
                    results['v4.statfs'] = line[28]
                    results['v4.readlink'] = line[29]
                    results['v4.readdir'] = line[30]
                    try:
                        results['v4.server_caps'] = line[31]
                    except IndexError:
                        pass
                    try:
                        results['v4.delegreturn'] = line[32]
                    except IndexError:
                        pass
                    try:
                        results['v4.getacl'] = line[33]
                    except IndexError:
                        pass
                    try:
                        results['v4.setacl'] = line[34]
                    except IndexError:
                        pass
                    try:
                        results['v4.fs_locations'] = line[35]
                    except IndexError:
                        pass
                    try:
                        results['v4.rel_lkowner'] = line[36]
                    except IndexError:
                        pass
                    try:
                        results['v4.exchange_id'] = line[37]
                    except IndexError:
                        pass
                    try:
                        results['v4.create_ses'] = line[38]
                    except IndexError:
                        pass
                    try:
                        results['v4.destroy_ses'] = line[39]
                    except IndexError:
                        pass
                    try:
                        results['v4.sequence'] = line[40]
                    except IndexError:
                        pass
                    try:
                        results['v4.get_lease_t'] = line[41]
                    except IndexError:
                        pass
                    try:
                        results['v4.reclaim_comp'] = line[42]
                    except IndexError:
                        pass
                    try:
                        results['v4.layoutget'] = line[43]
                    except IndexError:
                        pass
                    try:
                        results['v4.layoutcommit'] = line[44]
                    except IndexError:
                        pass
                    try:
                        results['v4.layoutreturn'] = line[45]
                    except IndexError:
                        pass
                    try:
                        results['v4.getdevlist'] = line[46]
                    except IndexError:
                        pass
                    try:
                        results['v4.getdevinfo'] = line[47]
                    except IndexError:
                        pass
                    try:
                        results['v4.ds_write'] = line[48]
                    except IndexError:
                        pass
                    try:
                        results['v4.ds_commit'] = line[49]
                    except IndexError:
                        pass
                    try:
                        results['v4.getdevlist'] = line[50]
                    except IndexError:
                        pass

            # Close File
            file.close()

            for stat in results.keys():
                metric_name = '.' + stat
                metric_value = long(float(results[stat]))
                metric_value = self.derivative(metric_name, metric_value)
                self.publish(metric_name, metric_value)
            return True

        return False
