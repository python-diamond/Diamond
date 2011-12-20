# Copyright (C) 2011-2012 by Ivan Pouzyrevsky.
# Copyright (C) 2010-2011 by Brightcove Inc. 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sys
import time
import logging
import traceback
import configobj
import optparse
import signal
import inspect
import pwd
import grp 

# Path Fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../")))

from diamond import *
import diamond

from diamond.collector import Collector
from diamond.handler import Handler
from diamond.scheduler import *
from diamond.util import * 

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

    def load_handler(self, fqcn):
        """
        Load Handler class named fqcn
        """
        # Load class
        cls = load_class_from_name(fqcn)
        # Check if cls is subclass of Handler
        if cls == Handler or not issubclass(cls, Handler):
            raise TypeError, "%s is not a vaild Handler" % (fqcn)          
        # Log 
        self.log.debug("Loaded Handler: %s" % (fqcn))
        return cls

    def load_handlers(self):
        """
        Load handlers
        """
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

            except Exception, e:
                # Log Error
                self.log.debug("Failed to load handler %s. %s" % (h, traceback.format_exc()))
                continue

    def load_collector(self, fqcn):
        """
        Load Collector class named fqcn 
        """
        # Load class
        cls = load_class_from_name(fqcn)
        # Check if cls is subclass of Collector
        if cls == Collector or not issubclass(cls, Collector):
            raise TypeError, "%s is not a valid Collector" % (fqcn)
        # Log
        self.log.debug("Loaded Collector: %s" % (fqcn))
        return cls

    def load_collectors(self, path, filter=None):
        """
        Scan for collectors to load from path 
        """
        # Initialize return value 
        collectors = {}    

        # Get a list of files in the directory, if the directory exists
        if not os.path.exists(path):
            raise OSError, "Directory does not exist: %s" % (path)

        # Log
        self.log.debug("Loading Collectors from: %s" % (path))
            
        # Add path to the system path
        sys.path.append(path)
        # Load all the files in path
        for f in os.listdir(path):
            # Ignore anything that isn't a .py file
            if len(f) > 3 and f[-3:] == '.py':

                # Check filter
                if filter and os.path.join(path, f) != filter:
                    continue

                modname = f[:-3]
                # Stat module file to get mtime
                st = os.stat(os.path.join(path, f))
                mtime = st.st_mtime
                # Check if module has been loaded before
                if modname in self.modules:
                    # Check if file mtime is newer then the last verison we loaded
                    if mtime <= self.modules[modname]:
                        # Module hasn't changed
                        # Log
                        self.log.debug("Found Module %s, but it hasn't changed." % (modname))
                        continue

                try:
                    # Import the module
                    mod = __import__(modname, globals(), locals(), ['*'])
                except Exception, e:
                    # Log error
                    self.log.error("Failed to import module: %s. %s" % (modname, traceback.format_exc()))
                    continue
 
                # Update module mtime 
                self.modules[modname] = mtime
                # Log
                self.log.debug("Loaded Module: %s" % (modname))

                # Find all classes defined in the module
                for attrname in dir(mod):
                    attr = getattr(mod, attrname)
                    # Only attempt to load classes that are infact classes, are Collectors but are not the base Collector class
                    if inspect.isclass(attr) and issubclass(attr, Collector) and attr != Collector:
                        # Get class name
                        fqcn = '.'.join([modname, attrname])
                        try:
                            # Load Collector class
                            cls = self.load_collector(fqcn)
                            # Add Collector class
                            collectors[cls.__name__] = cls
                        except Exception, e:
                            # Log error
                            self.log.error("Failed to load Collector: %s. %s" % (c, traceback.format_exc()))
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
            self.log.debug("Initialized Collector: %s" % (cls.__name__))
        except Exception, e:
            # Log error
            self.log.error("Failed to initialize Collector: %s. %s" % (cls.__name__, traceback.format_exc()))

        # Return collector
        return collector

    def schedule_collector(self, c, interval_task=True):
        """
        Schedule collector
        """
        # Check collector is for realz 
        if c is None: 
            self.log.warn("Skipped loading invalid Collector: %s" % (c.__class__.__name__))
            return 
            
        # Get collector schedule
        for name,schedule in c.get_schedule().items():
            # Get scheduler args
            func, args, splay, interval = schedule

            # Check if Collecter with same name has already been scheduled
            if name in self.tasks:
                self.scheduler.cancel(self.tasks[name])
                # Log
                self.log.debug("Canceled task: %s" % (name))

            # Schedule Collector
            if interval_task:
                task = self.scheduler.add_interval_task(func, name, splay, interval, diamond.scheduler.method.sequential, args, None, True)
            else:
                task = self.scheduler.add_single_task(func, name, splay, diamond.scheduler.method.sequential, args, None)

            # Log
            self.log.debug("Scheduled task: %s" % (name))
            # Add task to list 
            self.tasks[name] = task
 
    def run(self):
        """
        Load handler and collector classes and then start collectors
        """
        
        # Set Running Flag
        self.running = True
            
        # Load handlers
        self.load_handlers()

        # Load collectors
        collectors = self.load_collectors(self.config['server']['collectors_path'])

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
        self.load_handlers()

        # Overrides collector config dir
        self.config['server']['collectors_config_path'] = os.path.abspath(os.path.dirname(file))
 
        # Load collectors
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
            if reload and time_since_reload > int(self.config['server']['collectors_reload_interval']):
                # Log 
                self.log.debug("Reloading collectors.")
                # Load collectors
                collectors = self.load_collectors(self.config['server']['collectors_path'])
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
