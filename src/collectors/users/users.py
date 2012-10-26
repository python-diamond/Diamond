# coding=utf-8

"""
Collects the number of users logged in and shells per user

#### Dependencies

 * [pyutmp](http://software.clapper.org/pyutmp/)

"""

import diamond.collector
from pyutmp import UtmpFile


class UsersCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        """
        Returns the default collector help text
        """
        config_help = super(UsersCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(UsersCollector, self).get_default_config()
        config.update({
            'path':     'users',
            'method':   'Threaded',
        })
        return config

    def collect(self):
        metrics = {}
        metrics['total'] = 0
        
        for utmp in UtmpFile():
            if utmp.ut_user_process:
                metrics[utmp.ut_user] = metrics.get(utmp.ut_user, 0)+1
                metrics['total'] = metrics['total']+1

        for metric_name in metrics.keys():
            self.publish(metric_name, metrics[metric_name])

        return True
