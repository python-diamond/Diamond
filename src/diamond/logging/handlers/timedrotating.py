# coding=utf-8

from logging.handlers import TimedRotatingFileHandler as TRFH
import sys

class TimedRotatingFileHandler(TRFH):
    
    def flush():
        try:
            super(TimedRotatingFileHandler, self).flush()
        except IOError:
            sys.stderr.write('TimedRotatingFileHandler received a IOError!')
            sys.stderr.flush()
