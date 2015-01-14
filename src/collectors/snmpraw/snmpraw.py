# coding=utf-8

"""
The SNMPRawCollector is a deprecated collector. It's functionality
has been moved to the top level SNMPCollector

#### Dependencies

 * pysmnp (which depends on pyasn1 0.1.7 and pycrypto)

"""

import os
import sys
import warnings

file_path = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(file_path, 'snmp'))

from snmp import SNMPCollector as SNMPRawCollector  # NOQA

warnings.warn('SNMPRawCollector is deprecated. Use SNMPCollector',
              DeprecationWarning)
