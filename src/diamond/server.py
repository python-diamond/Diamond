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
from diamond.utils.signals import SIGUSR1Exception
from diamond.utils.signals import SIGUSR2Exception


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

        # We do this weird process title swap around to get the sync manager
        # title correct for ps
        if setproctitle:
            oldproctitle = getproctitle()
            setproctitle('%s - SyncManager' % getproctitle())
        self.manager = multiprocessing.Manager()
        if setproctitle:
            setproctitle(oldproctitle)
        self.metric_queue = self.manager.Queue()

    def run(self):
        """
        Load handler and collector classes and then start collectors
        """

        ########################################################################
        # Config
        ########################################################################
        self.config = load_config(self.configfile)

        collectors = load_collectors(self.config['server']['collectors_path'])

        ########################################################################
        # Handlers
        #
        # TODO: Eventually move each handler to it's own process space?
        ########################################################################

        if 'handlers_path' in self.config['server']:
            # Make an list if not one
            if isinstance(self.config['server']['handlers_path'], basestring):
                handlers_path = self.config['server']['handlers_path']
                handlers_path = handlers_path.split(',')
                handlers_path = map(str.strip, handlers_path)
                self.config['server']['handlers_path'] = handlers_path

            load_include_path(handlers_path)

        if 'handlers' not in self.config['server']:
            self.log.critical('handlers missing from server section in config')
            sys.exit(1)

        handlers = self.config['server'].get('handlers')
        handlers = handlers.split(',')
        handlers = map(str.strip, handlers)

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

        ########################################################################
        # Signals
        ########################################################################

        signal.signal(signal.SIGUSR1, signal_to_exception)
        signal.signal(signal.SIGUSR2, signal_to_exception)

        ########################################################################

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

                for process_name in running_collectors - running_processes:
                    if 'Collector' not in process_name:
                        continue
                    # Find the class
                    for cls in collectors.values():
                        cls_name = cls.__name__.split('.')[-1]
                        if cls_name == process_name:
                            break
                    if cls_name != process_name:
                        self.log.error('Can not find collector %s',
                                       process_name)
                        continue

                    collector = initialize_collector(
                        cls,
                        name=cls.__name__,
                        configfile=self.configfile,
                        handlers=[self.handler_queue])

                    if collector is None:
                        self.log.error('Failed to load collector %s',
                                       process_name)
                        continue

                    # Splay the loads
                    time.sleep(1)

                    process = multiprocessing.Process(
                        name=collector.__class__.__name__,
                        target=collector_process,
                        args=(collector, self.metric_queue, self.log)
                        )
                    process.daemon = True
                    process.start()

                ##############################################################

                time.sleep(1)

            except SIGUSR1Exception:
                self.log.info('Reloading state due to USR1')
                self.config = load_config(self.configfile)
                collectors = load_collectors(
                    self.config['server']['collectors_path'])

            except SIGUSR2Exception:
                pass
