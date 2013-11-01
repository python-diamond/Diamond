# coding=utf-8

import os
import sys
import time
import logging
import traceback
import configobj
import inspect

# Path Fix
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../")))

import diamond

from diamond.collector import Collector
from diamond.handler.Handler import Handler
from diamond.scheduler import ThreadedScheduler
from diamond.util import load_class_from_name


class Server(object):
    """
    Server class loads and starts Handlers and Collectors
    """

    def __init__(self, config):
        # Initialize Logging
        self.log = logging.getLogger('diamond')
        # Initialize Members
        self.config = config
        self.running = False
        self.handlers = []
        self.modules = {}
        self.tasks = {}
        # Initialize Scheduler
        self.scheduler = ThreadedScheduler()

    def load_config(self):
        """
        Load the full config
        """

        configfile = os.path.abspath(self.config['configfile'])
        config = configobj.ConfigObj(configfile)
        config['configfile'] = self.config['configfile']

        # Merge in handler config files into the main config
        if 'handlers_config_path' in config['server']:
            files = os.listdir(config['server']['handlers_config_path'])
            for filename in files:
                configname = os.path.basename(filename)
                handlername = configname.split('.')[0]
                if handlername not in self.config['handlers']:
                    config['handlers'][handlername] = configobj.ConfigObj()

                configfile = os.path.join(
                    config['server']['handlers_config_path'],
                    configname)
                hconfig = configobj.ConfigObj(configfile)
                if handlername in config['handlers']:
                    config['handlers'][handlername].merge(hconfig)
                else:
                    config['handlers'][handlername] = hconfig

        self.config = config

    def load_handler(self, fqcn):
        """
        Load Handler class named fqcn
        """
        # Load class
        cls = load_class_from_name(fqcn)
        # Check if cls is subclass of Handler
        if cls == Handler or not issubclass(cls, Handler):
            raise TypeError("%s is not a valid Handler" % fqcn)
        # Log
        self.log.debug("Loaded Handler: %s", fqcn)
        return cls

    def load_handlers(self):
        """
        Load handlers
        """
        if type(self.config['server']['handlers']) == str:
            handlers = [self.config['server']['handlers']]
            self.config['server']['handlers'] = handlers

        for h in self.config['server']['handlers']:
            try:
                # Load Handler Class
                cls = self.load_handler(h)

                # Initialize Handler config
                handler_config = configobj.ConfigObj()
                # Merge default Handler default config
                handler_config.merge(self.config['handlers']['default'])
                # Check if Handler config exists
                if cls.__name__ in self.config['handlers']:
                    # Merge Handler config section
                    handler_config.merge(self.config['handlers'][cls.__name__])

                # Initialize Handler class
                self.handlers.append(cls(handler_config))

            except (ImportError, SyntaxError):
                # Log Error
                self.log.debug("Failed to load handler %s. %s", h,
                               traceback.format_exc())
                continue

    def load_collector(self, fqcn):
        """
        Load Collector class named fqcn
        """
        # Load class
        cls = load_class_from_name(fqcn)
        # Check if cls is subclass of Collector
        if cls == Collector or not issubclass(cls, Collector):
            raise TypeError("%s is not a valid Collector" % fqcn)
        # Log
        self.log.debug("Loaded Collector: %s", fqcn)
        return cls

    def load_include_path(self, path):
        """
        Scan for and add paths to the include path
        """
        # Verify the path is valid
        if not os.path.isdir(path):
            return
        # Add path to the system path, to avoid name clashes
        # with mysql-connector for example ...
        sys.path.insert(1, path)
        # Load all the files in path
        for f in os.listdir(path):
            # Are we a directory? If so process down the tree
            fpath = os.path.join(path, f)
            if os.path.isdir(fpath):
                self.load_include_path(fpath)

    def load_collectors(self, path, filter=None):
        """
        Scan for collectors to load from path
        """
        # Initialize return value
        collectors = {}

        # Get a list of files in the directory, if the directory exists
        if not os.path.exists(path):
            raise OSError("Directory does not exist: %s" % path)

        if path.endswith('tests') or path.endswith('fixtures'):
            return collectors

        # Log
        self.log.debug("Loading Collectors from: %s", path)

        # Load all the files in path
        for f in os.listdir(path):

            # Are we a directory? If so process down the tree
            fpath = os.path.join(path, f)
            if os.path.isdir(fpath):
                subcollectors = self.load_collectors(fpath)
                for key in subcollectors:
                    collectors[key] = subcollectors[key]

            # Ignore anything that isn't a .py file
            elif (os.path.isfile(fpath)
                  and len(f) > 3
                  and f[-3:] == '.py'
                  and f[0:4] != 'test'
                  and f[0] != '.'):

                # Check filter
                if filter and os.path.join(path, f) != filter:
                    continue

                modname = f[:-3]

                # Stat module file to get mtime
                st = os.stat(os.path.join(path, f))
                mtime = st.st_mtime
                # Check if module has been loaded before
                if modname in self.modules:
                    # Check if file mtime is newer then the last loaded verison
                    if mtime <= self.modules[modname]:
                        # Module hasn't changed
                        # Log
                        self.log.debug("Found %s, but it hasn't changed.",
                                       modname)
                        continue

                try:
                    # Import the module
                    mod = __import__(modname, globals(), locals(), ['*'])
                except (ImportError, SyntaxError):
                    # Log error
                    self.log.error("Failed to import module: %s. %s", modname,
                                   traceback.format_exc())
                    continue

                # Update module mtime
                self.modules[modname] = mtime
                # Log
                self.log.debug("Loaded Module: %s", modname)

                # Find all classes defined in the module
                for attrname in dir(mod):
                    attr = getattr(mod, attrname)
                    # Only attempt to load classes that are infact classes
                    # are Collectors but are not the base Collector class
                    if (inspect.isclass(attr)
                            and issubclass(attr, Collector)
                            and attr != Collector):
                        if attrname.startswith('parent_'):
                            continue
                        # Get class name
                        fqcn = '.'.join([modname, attrname])
                        try:
                            # Load Collector class
                            cls = self.load_collector(fqcn)
                            # Add Collector class
                            collectors[cls.__name__] = cls
                        except Exception:
                            # Log error
                            self.log.error("Failed to load Collector: %s. %s",
                                           fqcn, traceback.format_exc())
                            continue

        # Return Collector classes
        return collectors

    def init_collector(self, cls):
        """
        Initialize collector
        """
        collector = None
        try:
            # Initialize Collector
            collector = cls(self.config, self.handlers)
            # Log
            self.log.debug("Initialized Collector: %s", cls.__name__)
        except Exception:
            # Log error
            self.log.error("Failed to initialize Collector: %s. %s",
                           cls.__name__, traceback.format_exc())

        # Return collector
        return collector

    def schedule_collector(self, c, interval_task=True):
        """
        Schedule collector
        """
        # Check collector is for realz
        if c is None:
            self.log.warn("Skipped loading invalid Collector: %s",
                          c.__class__.__name__)
            return

        if c.config['enabled'] != True:
            self.log.debug("Skipped loading disabled Collector: %s",
                          c.__class__.__name__)
            return

        # Get collector schedule
        for name, schedule in c.get_schedule().items():
            # Get scheduler args
            func, args, splay, interval = schedule

            # Check if Collecter with same name has already been scheduled
            if name in self.tasks:
                self.scheduler.cancel(self.tasks[name])
                # Log
                self.log.debug("Canceled task: %s", name)

            method = diamond.scheduler.method.sequential

            if 'method' in c.config:
                if c.config['method'] == 'Threaded':
                    method = diamond.scheduler.method.threaded
                elif c.config['method'] == 'Forked':
                    method = diamond.scheduler.method.forked

            # Schedule Collector
            if interval_task:
                task = self.scheduler.add_interval_task(func,
                                                        name,
                                                        splay,
                                                        interval,
                                                        method,
                                                        args,
                                                        None,
                                                        True)
            else:
                task = self.scheduler.add_single_task(func,
                                                      name,
                                                      splay,
                                                      method,
                                                      args,
                                                      None)

            # Log
            self.log.debug("Scheduled task: %s", name)
            # Add task to list
            self.tasks[name] = task

    def run(self):
        """
        Load handler and collector classes and then start collectors
        """

        # Set Running Flag
        self.running = True

        # Load handlers
        if 'handlers_path' in self.config['server']:
            handlers_path = self.config['server']['handlers_path']
            self.load_include_path(handlers_path)
        self.load_handlers()

        # Load config
        self.load_config()

        # Load collectors
        collectors_path = self.config['server']['collectors_path']
        self.load_include_path(collectors_path)
        collectors = self.load_collectors(collectors_path)

        # Setup Collectors
        for cls in collectors.values():
            # Initialize Collector
            c = self.init_collector(cls)
            # Schedule Collector
            self.schedule_collector(c)

        # Start main loop
        self.mainloop()

    def run_one(self, file):
        """
        Run given collector once and then exit
        """
        # Set Running Flag
        self.running = True

        # Load handlers
        if 'handlers_path' in self.config['server']:
            handlers_path = self.config['server']['handlers_path']
            self.load_include_path(handlers_path)
        self.load_handlers()

        # Overrides collector config dir
        collector_config_path = os.path.abspath(os.path.dirname(file))
        self.config['server']['collectors_config_path'] = collector_config_path

        # Load config
        self.load_config()

        # Load collectors
        self.load_include_path(os.path.dirname(file))
        collectors = self.load_collectors(os.path.dirname(file), file)

        # Setup Collectors
        for cls in collectors.values():
            # Initialize Collector
            c = self.init_collector(cls)

            # Schedule collector
            self.schedule_collector(c, False)

        # Start main loop
        self.mainloop(False)

    def mainloop(self, reload=True):

        # Start scheduler
        self.scheduler.start()

        # Log
        self.log.info('Started task scheduler.')

        # Initialize reload timer
        time_since_reload = 0

        # Main Loop
        while self.running:
            time.sleep(1)
            time_since_reload += 1

            # Check if its time to reload collectors
            if (reload
                    and time_since_reload
                    > int(self.config['server']['collectors_reload_interval'])):
                self.log.debug("Reloading config.")
                self.load_config()
                # Log
                self.log.debug("Reloading collectors.")
                # Load collectors
                collectors_path = self.config['server']['collectors_path']
                collectors = self.load_collectors(collectors_path)
                # Setup any Collectors that were loaded
                for cls in collectors.values():
                    # Initialize Collector
                    c = self.init_collector(cls)
                    # Schedule Collector
                    self.schedule_collector(c)

                # Reset reload timer
                time_since_reload = 0

            # Is the queue empty and we won't attempt to reload it? Exit
            if not reload and len(self.scheduler.sched._queue) == 0:
                self.running = False

        # Log
        self.log.debug('Stopping task scheduler.')
        # Stop scheduler
        self.scheduler.stop()
        # Log
        self.log.info('Stopped task scheduler.')
        # Log
        self.log.debug("Exiting.")

    def stop(self):
        """
        Close all connections and terminate threads.
        """
        # Set Running Flag
        self.running = False
