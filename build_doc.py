#!/usr/bin/env python
################################################################################

import os
import sys
import optparse

from configobj import ConfigObj

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'collectors')))

from diamond import *
from diamond.collector import Collector

collectors = {}
def getCollectors(path):
    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))

        if os.path.isfile(cPath) and len(f) > 3 and f[-3:] == '.py' and f[0:4] != 'Test':
            sys.path.append(os.path.dirname(cPath))
            modname = f[:-3]
            try:
                # Import the module
                module = __import__(modname, globals(), locals(), ['*'])
                
                # Find the name
                for attr in dir(module):
                    cls = getattr(module, attr)
                    try:
                        if issubclass(cls, Collector):
                            collectors[cls.__name__] = module
                            break
                    except TypeError:
                        continue
                # print "Imported module: %s %s" % (modname, cls.__name__)
            except Exception, e:
                print "Failed to import module: %s. %s" % (modname, traceback.format_exc())
                collectors[modname] = False
                continue

    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))
        if os.path.isdir(cPath):
            getCollectors(cPath)

################################################################################

if __name__ == "__main__":
    
    # Initialize Options
    parser = optparse.OptionParser()
    parser.add_option("-c", "--configfile", dest="configfile", default="/etc/diamond/diamond.conf", help="Path to the config file")
    parser.add_option("-C", "--collector", dest="collector", default=None, help="Configure a single collector")
    parser.add_option("-p", "--print", action="store_true", dest="dump", default=False, help="Just print the defaults")

    # Parse Command Line Args
    (options, args) = parser.parse_args()
    
    # Initialize Config
    if os.path.exists(options.configfile):
        config = configobj.ConfigObj(os.path.abspath(options.configfile))
        config['configfile'] = options.configfile
    else:
        print >> sys.stderr, "ERROR: Config file: %s does not exist." % (options.configfile)
        print >> sys.stderr, "Please run python config.py -c /path/to/diamond.conf"
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    collector_path = config['server']['collectors_path']
    docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'docs'))
    
    getCollectors(collector_path)
    
    for collector in collectors:
        
        # Skip configuring the basic collector object
        if collector == "Collector":
            continue
        
        print collector
        
        print collectors[collector].__doc__

        if not hasattr(collectors[collector], collector):
            continue
        
        cls = getattr(collectors[collector], collector)
        
        obj = cls(config = config, handlers = {})
        
        break
