# coding=utf-8

"""
Collects the number of emails for each user, and an aggregate.
"""
import os
import mailbox

import diamond.collector

class MailCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        """
        Returns the default collector help text
        """
        config_help = super(MailCollector, self).get_default_config_help()
        config_help.update({
            'spool_path': ('Path to mail spool that contains files to be '
                           'analyzed.'),
            'mailbox_prefix': ('Prefix to add to the metric name. Use in case '
                               'you are monitoring more than one domain.'),
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MailCollector, self).get_default_config()
        config.update({
            'spool_path': '/var/mail/',
            'mailbox_prefix': '',
        })
        return config

    def collect(self):
        metrics = {}
        metrics['total'] = 0

        for uname in os.listdir(self.config['spool_path']):
            fpath = os.path.join(self.config['spool_path'], uname)
            if os.path.isfile(fpath):
                mbox = mailbox.mbox(fpath)
                metrics[uname] = len(mbox)
                metrics['total'] += metrics[uname]

        self.publish_metrics(metrics)

        return True

    def publish_metrics(self, metrics):
        prefix = self.config['mailbox_prefix']
        metric_prefix = ("{0}." if prefix else '').format(prefix)
        for name, value in metrics.iteritems():
            self.publish('{0}{1}.count'.format(metric_prefix, name), value)
