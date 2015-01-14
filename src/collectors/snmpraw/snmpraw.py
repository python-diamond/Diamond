# coding=utf-8

"""
The SNMPRawCollector is a deprecated collector. It's functionality has been moved to the
top level SNMPCollector

#### Dependencies

 * pysmnp (which depends on pyasn1 0.1.7 and pycrypto)

"""

import os
import sys
import warnings

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'snmp'))

from snmp import SNMPCollector as SNMPRawCollector  # NOQA

warnings.warn('The SNMPRawCollector is deprecated. Use SNMPCollector instead', DeprecationWarning)
