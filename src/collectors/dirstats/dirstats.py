# coding=utf-8

"""
Collect given directories stats.

"""

import os

from stat import S_ISDIR, S_ISREG
from time import time

try:
    import Queue as queue
except ImportError:
    import queue

import diamond.collector

BLOCK = 512
DAY = 86400
MB = 1048576


class Directory(object):
    """
    Directory object.
    """
    def __init__(self, path):

        self.path = path
        self.allocated = 0
        self.size = 0
        self.subdirs = 0
        self.files = 0
        self.modified = 0
        self.skipped = set()

    def _log_skipped(self, os_error):
        """
        Log skipped path.
        """
        self.skipped.add(
            'Dirstats: skipping ' + os_error.filename + \
            ' Reason: ' + os_error.strerror)

    def get_stats(self):
        """
        Calculate directory size and number of days since last update.
        """
        dirs_queue = queue.Queue()
        dirs_queue.put(self.path)

        while not dirs_queue.empty():

            try:

                path = dirs_queue.get()
                entities = os.listdir(path)

            except OSError as os_error:
                self._log_skipped(os_error)
                continue

            for entity in entities:
                fullpath = os.path.join(path, entity)

                try:

                    mode = os.stat(fullpath).st_mode

                    if S_ISDIR(mode):

                        self.subdirs += 1
                        dirs_queue.put(fullpath)

                    elif S_ISREG(mode):

                        self.files += 1
                        self.size += os.stat(fullpath).st_blocks * BLOCK
                        self.allocated += os.stat(fullpath).st_size
                        last_modified = os.stat(fullpath).st_mtime
                        if last_modified > self.modified:
                            self.modified = last_modified

                except OSError as os_error:
                    self._log_skipped(os_error)
                    continue

        if not self.skipped and not self.modified:
            self.modified = os.stat(self.path).st_mtime


class DirStatsCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this collector.
        """
        config_help = super(DirStatsCollector, self).get_default_config_help()
        config_help.update({
            'dirs': 'directories to collect stats on'})

        return config_help

    def get_default_config(self):
        """
        Returns default configuration options.
        """
        config = super(DirStatsCollector, self).get_default_config()
        config.update({
            'path': 'dirstats',
            'dirs': {}})

        return config

    def collect(self):
        """
        Collect and publish directories stats.
        """
        metrics = {}

        for dir_name in self.config['dirs']:

            directory = Directory(self.config['dirs'][dir_name])
            directory.get_stats()

            if directory.skipped:
                for message in directory.skipped:
                    self.log.error(message)

            metrics.update({
                dir_name + '.size.allocated': int(directory.allocated/MB),
                dir_name + '.size.current': int(directory.size/MB),
                dir_name + '.subdirs': directory.subdirs,
                dir_name + '.files': directory.files,
                dir_name + '.days_unmodified': int(
                    (time()-directory.modified)/DAY)})

        for metric in metrics:
            self.publish(metric, metrics[metric])
