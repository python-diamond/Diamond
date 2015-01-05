# coding=utf-8

"""
Collects the number of emails for each user, and an aggregate.

#### Example configuration

```
[MailCollector]
spool_path = /var/mail/vhosts
[[prefixes]]
[[[example_com]]]
spool_path = example.com
[[[example_net]]]
spool_path = example.net
```

This will analyze, e.g: /var/mail/vhosts/example.com and publish metrics
with the following pattern:

<hostname>.mail.example_com.<user>.count
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
            'path': 'mail',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MailCollector, self).get_default_config()
        config.update({
            'spool_path': '/var/mail/',
            'prefixes': {}
        })
        return config

    def collect(self):
        metrics = {}
        metrics['total'] = 0

        base_path = self.config['spool_path']
        paths = {
            '': base_path,
        }
        for prefix, conf in self.config['prefixes'].iteritems():
            # if conf['spool_path'] is an absolute path, os.path.join will
            # remove base_path automatically
            path = os.path.join(base_path, conf['spool_path'])
            paths[prefix] = path

        for prefix, path in paths.iteritems():
            metricparts = []
            if prefix:
                metricparts.append(prefix)

            for uname in os.listdir(path):
                metricparts.append(uname)
                fpath = os.path.join(self.config['spool_path'], uname)
                if os.path.isfile(fpath):
                    mbox = mailbox.mbox(fpath)
                    mname = ".".join(metricparts + ['count'])
                    metrics[mname] = len(mbox)
                    metrics['total'] += metrics[mname]

        self.publish_metrics(metrics)

        return True

    def publish_metrics(self, metrics):
        for name, value in metrics.iteritems():
            self.publish(name, value)
