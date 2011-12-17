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

if __name__ == "__main__":

    # Initialize Options
    parser = optparse.OptionParser(usage="diamond [options]")
    parser.add_option("-c", "--configfile", dest="configfile", default="/etc/diamond/diamond.cfg", help="config file")
    parser.add_option("-l", "--logfile", dest="logfile", default=None, help="log file")
    parser.add_option("-f", "--foreground", dest="foreground", default=False, action="store_true", help="run in foreground")
    parser.add_option("-p", "--pidfile", dest="pidfile", default=None, help="pid file")
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="verbose")
    parser.add_option("-r", "--run", dest="collector", default=None, help="run a given collector once and exit")
    parser.add_option("-s", "--noswitchuser", dest="noswitchuser", default=False, action="store_true", help="dont switch user")

    # Parse Command Line Args
    (options, args) = parser.parse_args()

    # Initialize Config
    if os.path.exists(options.configfile):
        config = configobj.ConfigObj(os.path.abspath(options.configfile))
    else:
        print >> sys.stderr, "ERROR: Config file: %s does not exist." % (options.configfile)
        print >> sys.stderr, parser.usage
        sys.exit(1)
   
    # Switch user to specified user/group if required
    if not options.noswitchuser:     
        try:
            # Get UID
            uid = pwd.getpwnam(config['server']['user']).pw_uid       
            # Get GID
            gid = grp.getgrnam(config['server']['group']).gr_gid
        
            if os.getuid() != uid:
                # Set GID 
                os.setgid(gid)

            if os.getgid() != gid:
                # Set UID 
                os.setuid(uid)
        except Exception, e:
            print >> sys.stderr, "ERROR: Failed to set UID/GID. %s" % (e)
            sys.exit(1)

    # Initialize Logging
    log = logging.getLogger('diamond')
    log.setLevel(logging.INFO)

    # Configure Logging Format
    formatter = logging.Formatter('[%(asctime)s] [%(threadName)s] %(message)s')
    
    # Configure Log Stream Handler
    if options.foreground:
        streamHandler = logging.StreamHandler(sys.stdout)
        streamHandler.setFormatter(formatter)
        streamHandler.setLevel(logging.DEBUG)
        log.addHandler(streamHandler)

    # Got Log File Handler log file 
    if not options.logfile:
        options.logfile = str(config['server']['log_file'])

    # Attempt to Log File Directory
    logdir = os.path.abspath(os.path.dirname(options.logfile)) 
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    
    # Configure Log File handler
    fileHandler = logging.FileHandler(options.logfile, 'w')
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(logging.DEBUG)
    log.addHandler(fileHandler)
    
    # Configure Logging Verbosity
    if options.verbose:
        log.setLevel(logging.DEBUG)
    
    if not options.noswitchuser:     
        # Log 
        log.info('Changed UID: %d (%s) GID: %d (%s).' % (uid, config['server']['user'], gid, config['server']['group']))
            
    # Initialize Pid file
    if not options.pidfile:
        options.pidfile = str(config['server']['pid_file']) 

    # Read existing pid file
    try:
        pf = file(options.pidfile,'r')
        pid = int(pf.read().strip())
        pf.close()
    except IOError:
        pid = None

    # Check existing pid file
    if pid:
        # Check if pid is real
        if not os.path.exists("/".join(["/proc", str(pid), "cmdline"])):
            # Pid is not real
            os.unlink(options.pidfile)
            pid = None
            print >> sys.stderr, "WARN: Bogus pid file was found. I deleted it."
        else:
            print >> sys.stderr, "ERROR: Pidfile already exists. Server already running?"
            sys.exit(1)

    # Detatch Process
    if not options.foreground and not options.collector:

        # Double fork to serverize process
        log.info('Deatching Process.')

        # Fork 1 
        try: 
            pid = os.fork() 
            if pid > 0:
                # Exit first parent
                sys.exit(0) 
        except OSError, e:
            print >> sys.stderr, "Failed to fork process." % (e) 
            sys.exit(1)
        # Decouple from parent environment
        os.setsid() 
        os.umask(0) 
        # Fork 2
        try: 
            pid = os.fork() 
            if pid > 0:
                # Exit econd parent
                sys.exit(0) 
        except OSError, e: 
            print >> sys.stderr, "Failed to fork process." % (e) 
            sys.exit(1)
        # Close file descriptors so that we can detach
        sys.stdout.close()
        sys.stderr.close()
        sys.stdin.close()
        os.close(0)
        os.close(1)
        os.close(2)

    # Finish Initialize PID file 
    if not options.foreground and not options.collector:  
        # Write pid file
        pid = str(os.getpid())
        pf = file(options.pidfile,'w+')
        pf.write("%s\n" % pid)
        pf.close()
        # Log
        log.debug("Wrote PID file: %s" % (options.pidfile))

    # Initialize Server 
    server = Server(config)
        
    def sigint_handler(signum, frame):
            # Log
            log.debug("Signal Received: %d" % (signum))
            # Stop Server
            server.stop()
            # Delete Pidfile
            if os.path.exists(options.pidfile):
                os.remove(options.pidfile)
                # Log
                log.debug("Removed PID file: %s" % (options.pidfile))

    # Set the signal handlers 
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)

    if options.collector:
        # Run Server with one collector
        server.run_one(options.collector)
    else:
        # Run Server 
        server.run()
