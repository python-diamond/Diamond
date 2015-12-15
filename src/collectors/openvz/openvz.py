# coding=utf-8

"""
OpenvzCollector grabs stats from Openvz and submits them the Graphite

#### Dependencies

 * /usr/sbin/vzlist

"""

import diamond.collector
import json
import subprocess


class OpenvzCollector(diamond.collector.Collector):

    _FIELDS = (
        'laverage',
        'uptime'
    )

    def get_default_config_help(self):
        config_help = super(OpenvzCollector, self).get_default_config_help()
        config_help.update({
            'bin': 'The path to the vzlist',
            'keyname' : 'the name of key for concatenate value (default: hostname)',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(OpenvzCollector, self).get_default_config()
        config.update({
            'path': 'openvz',
            'bin': '/usr/sbin/vzlist',
            'keyname' : 'hostname'
        })
        return config

    def collect(self):
        data = {}
        output = self.poll()

        instances_infos = json.loads(output)

        if not instances_infos:
            return

        for instance_values in instances_infos:
            serverkey = instance_values[self.config['keyname']].replace('.','_')

            for keyvalue in instance_values:
                sfield = ['held', 'maxheld', 'usage']
                # Get Array values
                if isinstance(instance_values[keyvalue], dict):
                    for subkey in instance_values[keyvalue]:
                        stat_name = '%s.%s.%s' % (
                            serverkey,
                            keyvalue,
                            subkey
                        )
                        if subkey in sfield:
                            try:
                                metric_value = float(instance_values[keyvalue][subkey])
                            except ValueError:
                                continue

                            self.publish(
                                stat_name,
                                metric_value,
                                precision=5
                            )
                else:
                    # Get field value
                    if keyvalue in self._FIELDS:
                        # Get Load average values
                        if keyvalue == 'laverage':
                            submetric_name = ['01', '05', '15']
                            for idx in range(0,3):
                                try:
                                    metric_value = float(instance_values[keyvalue][idx])
                                except ValueError:
                                    continue

                                stat_name = '%s.%s.%s' % (serverkey, keyvalue, submetric_name[idx])
                                self.publish(
                                    stat_name,
                                    metric_value,
                                    precision=5
                                )
                        else:
                            # Field value
                            try:
                                metric_value = float(instance_values[keyvalue])
                            except ValueError:
                                continue

                            stat_name = '%s.%s' % (serverkey, keyvalue)
                            self.publish(stat_name, metric_value, precision=5)

    def poll(self):
        try:
            command = [self.config['bin'], '-j']

            output = subprocess.Popen(command,
                                      stdout=subprocess.PIPE).communicate()[0]
        except OSError:
            output = ""

        return output
