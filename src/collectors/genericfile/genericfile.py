# coding=utf-8
"""
This class collects data in key / value form from generic files.

The collector operates on each line of a file, expecting the line to match the
format provided by a configurable regular expression. It behaves similarly
to awk.

By default, the regular expression represents a common file pattern of key
values pairs separated by either space, colon or equals (with optional
surrounding space). The key value pairs can be any alphanumeric character.

If customization is required, you can provide a different regex. Furthermore,
you can override the match method if you need to do any further processing.

#### Dependencies

* re



"""
import diamond.collector
import os
import re


class GenericFileCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(GenericFileCollector,
                            self).get_default_config_help()
        config_help.update({
            'regex': 'Defines the line format of the file.',
            'file': 'The file from which to collect the data.',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(GenericFileCollector, self).get_default_config()
        config.update({
            'regex': '^\s*(?P<key>\w+)\s*[\s|:|=]\s*(?P<value>\w+)\s*$',
            'path': '',
        })
        return config

    def match(self, line):
        """
        Extract the values from the regular expression.
        This simply takes the key / value pair represented by
        alphanumeric characters.
        """
        m = re.match(self.config['regex'], line)
        if m:
            return m.groupdict()
        return None

    def collect(self):
        """
        Collects data from the 'file' given the format defined in 'regex'.
        """
        if 'file' not in self.config:
            self.log.error('"file" is not defined in the configuration %s.' %
                           self.__class__.__name__)
            return None

        try:
            generic_file = open(self.config['file'], 'r')
        except IOError as e:
            self.log.error('Can not read file %s: %s' %
                           (self.config['file'], e.strerror))
            return None
        with generic_file:
            line_count = 0
            for line in generic_file:
                line_count += 1
                stat = self.match(line)
                if stat:
                    self.publish(stat['key'], stat['value'])
                else:
                    self.log.warn('Unexpected file format on line: %d.' %
                                  line_count)
