# coding=utf-8

import logging
import multiprocessing
import os
import signal
import sys
import time

try:
    from setproctitle import getproctitle, setproctitle
except ImportError:
    setproctitle = None

# Path Fix
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../")))

from diamond.utils.classes import initialize_collector
from diamond.utils.classes import load_collectors
from diamond.utils.classes import load_dynamic_class
from diamond.utils.classes import load_handlers
from diamond.utils.classes import load_include_path

from diamond.utils.config import load_config

from diamond.utils.scheduler import collector_process
from diamond.utils.scheduler import handler_process

from diamond.handler.Handler import Handler

from diamond.utils.signals import signal_to_exception
from diamond.utils.signals import SIGHUPException


class Server(object):
    """
    Server class loads and starts Handlers and Collectors
    """

    def __init__(self, configfile):
        # Initialize Logging
        self.log = logging.getLogger('diamond')
        # Initialize Members
        self.configfile = configfile
        self.config = None
        self.handlers = []
        self.handler_queue = []
        self.modules = {}
        self.metric_queue = None

        # We do this weird process title swap around to get the sync manager
        # title correct for ps
        if setproctitle:
            oldproctitle = getproctitle()
            setproctitle('%s - SyncManager' % getproctitle())
        self.manager = multiprocessing.Manager()
        if setproctitle:
            setproctitle(oldproctitle)

    def run(self):
        """
        Load handler and collector classes and then start collectors
        """

        #######################################################################
        # Config
        #######################################################################
        self.config = load_config(self.configfile)

        collectors = load_collectors(self.config['server']['collectors_path'])
        metric_queue_size = int(self.config['server'].get('metric_queue_size',
                                                          16384))
        self.metric_queue = self.manager.Queue(maxsize=metric_queue_size)
        self.log.debug('metric_queue_size: %d', metric_queue_size)

        #######################################################################
        # Handlers
        #
        # TODO: Eventually move each handler to it's own process space?
        #######################################################################

        if 'handlers_path' in self.config['server']:
            handlers_path = self.config['server']['handlers_path']

            # Make an list if not one
            if isinstance(handlers_path, basestring):
                handlers_path = handlers_path.split(',')
                handlers_path = map(str.strip, handlers_path)
                self.config['server']['handlers_path'] = handlers_path

            load_include_path(handlers_path)

        if 'handlers' not in self.config['server']:
            self.log.critical('handlers missing from server section in config')
            sys.exit(1)

        handlers = self.config['server'].get('handlers')
        if isinstance(handlers, basestring):
            handlers = [handlers]

        # Prevent the Queue Handler from being a normal handler
        if 'diamond.handler.queue.QueueHandler' in handlers:
            handlers.remove('diamond.handler.queue.QueueHandler')

        self.handlers = load_handlers(self.config, handlers)

        QueueHandler = load_dynamic_class(
            'diamond.handler.queue.QueueHandler',
            Handler
        )

        self.handler_queue = QueueHandler(
            config=self.config, queue=self.metric_queue, log=self.log)

        process = multiprocessing.Process(
            name="Handlers",
            target=handler_process,
            args=(self.handlers, self.metric_queue, self.log),
        )

        process.daemon = True
        process.start()

        #######################################################################
        # Signals
        #######################################################################

        if hasattr(signal, 'SIGHUP'):
            signal.signal(signal.SIGHUP, signal_to_exception)

        #######################################################################

        while True:
            try:
                active_children = multiprocessing.active_children()
                running_processes = []
                for process in active_children:
                    running_processes.append(process.name)
                running_processes = set(running_processes)

                ##############################################################
                # Collectors
                ##############################################################

                running_collectors = []
                for collector, config in self.config['collectors'].iteritems():
                    if config.get('enabled', False) is not True:
                        continue
                    running_collectors.append(collector)
                running_collectors = set(running_collectors)

                # Collectors that are running but shouldn't be
                for process_name in running_processes - running_collectors:
                    if 'Collector' not in process_name:
                        continue
                    for process in active_children:
                        if process.name == process_name:
                            process.terminate()

                collector_classes = dict(
                    (cls.__name__.split('.')[-1], cls)
                    for cls in collectors.values()
                )

                load_delay = self.config['server'].get('collectors_load_delay',
                                                       1.0)
                for process_name in running_collectors - running_processes:
                    # To handle running multiple collectors concurrently, we
                    # split on white space and use the first word as the
                    # collector name to spin
                    collector_name = process_name.split()[0]

                    if 'Collector' not in collector_name:
                        continue

                    if collector_name not in collector_classes:
                        self.log.error('Can not find collector %s',
                                       collector_name)
                        continue

                    collector = initialize_collector(
                        collector_classes[collector_name],
                        name=process_name,
                        configfile=self.configfile,
                        handlers=[self.handler_queue])

                    if collector is None:
                        self.log.error('Failed to load collector %s',
                                       process_name)
                        continue

                    # Splay the loads
                    time.sleep(float(load_delay))

                    process = multiprocessing.Process(
                        name=process_name,
                        target=collector_process,
                        args=(collector, self.metric_queue, self.log)
                    )
                    process.daemon = True
                    process.start()

                ##############################################################

                time.sleep(1)

            except SIGHUPException:
                # ignore further SIGHUPs for now
                original_sighup_handler = signal.getsignal(signal.SIGHUP)
                signal.signal(signal.SIGHUP, signal.SIG_IGN)

                self.log.info('Reloading state due to HUP')
                self.config = load_config(self.configfile)
                collectors = load_collectors(
                    self.config['server']['collectors_path'])
                # restore SIGHUP handler
                signal.signal(signal.SIGHUP, original_sighup_handler)
