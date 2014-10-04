# coding=utf-8

"""
Collects the number of users logged in and shells per user

#### Dependencies

 * [pyutmp](http://software.clapper.org/pyutmp/)
or
 * [utmp] (python-utmp on Debian and derivatives)

"""

import diamond.collector

try:
    from pyutmp import UtmpFile
except ImportError:
    UtmpFile = None
try:
    from utmp import UtmpRecord
    import UTMPCONST
except ImportError:
    UtmpRecord = None


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
            'utmp':     None,
        })
        return config

    def collect(self):
        if UtmpFile is None and UtmpRecord is None:
            self.log.error('Unable to import either pyutmp or python-utmp')
            return False

        metrics = {}
        metrics['total'] = 0

        if UtmpFile:
            for utmp in UtmpFile(path=self.config['utmp']):
                if utmp.ut_user_process:
                    metrics[utmp.ut_user] = metrics.get(utmp.ut_user, 0) + 1
                    metrics['total'] = metrics['total'] + 1

        if UtmpRecord:
            for utmp in UtmpRecord(fname=self.config['utmp']):
                if utmp.ut_type == UTMPCONST.USER_PROCESS:
                    metrics[utmp.ut_user] = metrics.get(utmp.ut_user, 0) + 1
                    metrics['total'] = metrics['total'] + 1

        for metric_name in metrics.keys():
            self.publish(metric_name, metrics[metric_name])

        return True
