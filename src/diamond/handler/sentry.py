# coding=utf-8

"""
Diamond handler that check if values are too high or too low, if so send an
alert to a Sentry server

This handler requires the Python module Raven:
http://raven.readthedocs.org/en/latest/index.html

To work this handler need a similar configuration:

[[SentryHandler]]

# Create a new project in Sentry and copy the DSN here:
dsn = http://user:pass@hostname/id

[[[load]]]

name = Load Average
# check for load average of the last 15 minutes
path = loadavg.15
max = 8.5

[[[free_memory]]]

name = Free Memory
path = memory.MemFree
min = 66020000
"""

__author__ = 'Bruno Clermont'
__email__ = 'bruno.clermont@gmail.com'

import logging
import re

import raven.handlers.logging
from Handler import Handler
from diamond.collector import get_hostname
from configobj import Section


class InvalidRule(ValueError):
    """
    invalid rule
    """
    pass


class BaseResult(object):
    """
    Base class for a Rule minimum/maximum check result
    """
    adjective = None

    def __init__(self, value, threshold):
        """
        @type value: float
        @param value: metric value
        @type threshold: float
        @param threshold: value that trigger a warning
        """
        self.value = value
        self.threshold = threshold

    @property
    def verbose_message(self):
        """return more complete message"""
        if self.threshold is None:
            return 'No threshold'
        return '%.1f is %s than %.1f' % (self.value,
                                         self.adjective,
                                         self.threshold)

    @property
    def _is_error(self):
        raise NotImplementedError('_is_error')

    @property
    def is_error(self):
        """
        for some reason python do this:
        >>> 1.0 > None
        True
        >>> 1.0 < None
        False
        so we just check if min/max is not None before return _is_error
        """
        if self.threshold is None:
            return False
        return self._is_error

    def __str__(self):
        name = self.__class__.__name__.lower()
        if self.threshold is None:
            return '%s: %.1f no threshold' % (name, self.value)
        return '%.1f (%s: %.1f)' % (self.value, name, self.threshold)


class Minimum(BaseResult):
    """
    Minimum result
    """
    adjective = 'lower'

    @property
    def _is_error(self):
        """if it's too low"""
        return self.value < self.threshold


class Maximum(BaseResult):
    """
    Maximum result
    """
    adjective = 'higher'

    @property
    def _is_error(self):
        """if it's too high"""
        return self.value > self.threshold


class Rule(object):
    """
    Alert rule
    """

    def __init__(self, name, path, min=None, max=None):
        """
        @type name: string
        @param name: rule name, used to identify this rule in Sentry
        @type path: string
        @param path: un-compiled regular expression of the path of the rule
        @type min: string of float/int, int or float. will be convert to float
        @param min: optional minimal value that if value goes below it send
            an alert to Sentry
        @type max: string of float/int, int or float. will be convert to float
        @param max: optional maximal value that if value goes over it send
            an alert to Sentry
        """
        self.name = name
        # counters that can be used to debug rule
        self.counter_errors = 0
        self.counter_pass = 0

        # force min and max to be float
        try:
            self.min = float(min)
        except TypeError:
            self.min = None
        try:
            self.max = float(max)
        except TypeError:
            self.max = None

        if self.min is None and self.max is None:
            raise InvalidRule("%s: %s: both min and max are unset or invalid"
                              % (name, path))

        if self.min is not None and self.max is not None:
            if self.min > self.max:
                raise InvalidRule("min %.1f is larger than max %.1f" % (
                    self.min, self.max))

        # compile path regular expression
        self.regexp = re.compile(r'(?P<prefix>.*)\.(?P<path>%s)$' % path)

    def process(self, metric, handler):
        """
        process a single diamond metric
        @type metric: diamond.metric.Metric
        @param metric: metric to process
        @type handler: diamond.handler.sentry.SentryHandler
        @param handler: configured Sentry graphite handler
        @rtype None
        """
        match = self.regexp.match(metric.path)
        if match:
            minimum = Minimum(metric.value, self.min)
            maximum = Maximum(metric.value, self.max)

            if minimum.is_error or maximum.is_error:
                self.counter_errors += 1
                message = "%s Warning on %s: %.1f" % (self.name,
                                                      handler.hostname,
                                                      metric.value)
                culprit = "%s %s" % (handler.hostname, match.group('path'))
                handler.raven_logger.error(message, extra={
                    'culprit': culprit,
                    'data': {
                        'metric prefix': match.group('prefix'),
                        'metric path': match.group('path'),
                        'minimum check': minimum.verbose_message,
                        'maximum check': maximum.verbose_message,
                        'metric original path': metric.path,
                        'metric value': metric.value,
                        'metric precision': metric.precision,
                        'metric timestamp': metric.timestamp,
                        'minimum threshold': self.min,
                        'maximum threshold': self.max,
                        'path regular expression': self.regexp.pattern,
                        'total errors': self.counter_errors,
                        'total pass': self.counter_pass,
                        'hostname': handler.hostname
                    }
                }
                )
            else:
                self.counter_pass += 1

    def __repr__(self):
        return '%s: min:%s max:%s %s' % (self.name, self.min, self.max,
                                         self.regexp.pattern)


class SentryHandler(Handler):
    """
    Diamond handler that check if a metric goes too low or too high
    """

    # valid key name in rules sub-section
    VALID_RULES_KEYS = ('name', 'path', 'min', 'max')

    def __init__(self, config=None):
        """
        @type config: configobj.ConfigObj
        """
        Handler.__init__(self, config)
        # init sentry/raven
        self.sentry_log_handler = raven.handlers.logging.SentryHandler(
            self.config['dsn'])
        self.raven_logger = logging.getLogger(self.__class__.__name__)
        self.raven_logger.addHandler(self.sentry_log_handler)
        self.configure_sentry_errors()
        self.rules = self.compile_rules()
        self.hostname = get_hostname(self.config)
        if not len(self.rules):
            self.log.warning("No rules, this graphite handler is unused")

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(SentryHandler, self).get_default_config_help()

        config.update({
            'dsn': '',
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(SentryHandler, self).get_default_config()

        config.update({
            'dsn': '',
        })

        return config

    def compile_rules(self):
        """
        Compile alert rules
        @rtype list of Rules
        """
        output = []
        # validate configuration, skip invalid section
        for key_name, section in self.config.items():
            rule = self.compile_section(section)
            if rule is not None:
                output.append(rule)
        return output

    def compile_section(self, section):
        """
        Validate if a section is a valid rule
        @type section: configobj.Section
        @param section: section to validate
        @rtype Rule or None
        @return None if invalid
        """
        if section.__class__ != Section:
            # not a section, just skip
            return

        # name and path are mandatory
        keys = section.keys()
        for key in ('name', 'path'):
            if key not in keys:
                self.log.warning("section %s miss key '%s' ignore", key,
                                 section.name)
                return

        # just warn if invalid key in section
        for key in keys:
            if key not in self.VALID_RULES_KEYS:
                self.log.warning("invalid key %s in section %s",
                                 key, section.name)

        # need at least a min or a max
        if 'min' not in keys and 'max' not in keys:
            self.log.warning("either 'min' or 'max' is defined in %s",
                             section.name)
            return

        # add rule to the list
        kwargs = {
            'name': section['name'],
            'path': section['path']
        }
        for argument in ('min', 'max'):
            try:
                kwargs[argument] = section[argument]
            except KeyError:
                pass

        # init rule
        try:
            return Rule(**kwargs)
        except InvalidRule, err:
            self.log.error(str(err))

    def configure_sentry_errors(self):
        """
        Configure sentry.errors to use the same loggers as the root handler
        @rtype: None
        """
        sentry_errors_logger = logging.getLogger('sentry.errors')
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            sentry_errors_logger.addHandler(handler)

    def process(self, metric):
        """
        process a single metric
        @type metric: diamond.metric.Metric
        @param metric: metric to process
        @rtype None
        """
        for rule in self.rules:
            rule.process(metric, self)

    def __repr__(self):
        return "SentryHandler '%s' %d rules" % (
            self.sentry_log_handler.client.servers, len(self.rules))
