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
    
    if not options.dump:
        print    
        print 'I will be over writing files in'
        print config['server']['collectors_config_path']
        print 'Please type yes to continue'
        
        val = raw_input('Are you sure? ')
        if val != 'yes':
            sys.exit()
        
    getCollectors(config['server']['collectors_path'])
    
    tests = []
    for collector in collectors:
        if options.collector and collector != options.collector:
            continue
        
        # Skip configuring the basic collector object
        if collector == "Collector":
            continue
        
        config_keys = { 'enabled': True}
        config_file = ConfigObj()
        config_file.filename = config['server']['collectors_config_path']+"/"+collector+".conf"
        
        # Find the class and load it from the collector module
        try:
            
            # We can for the name above, so we dont have to scan here anymore
            if not hasattr(collectors[collector], collector):
                continue
            
            cls = getattr(collectors[collector], collector)
            obj = cls(config = config, handlers = {})
            
            if options.dump:
                print collector+" "+str(obj.config)
                continue
            
            default_conf = obj.get_default_config()
        
            for key in obj.get_default_config():
                config_keys[key] = True
                
            # Disable some keys
            config_keys['path'] = False
            config_keys['method'] = False
                
            print
            print "\t\tNow configuring "+collector
            
            for key in config_keys:
                if not config_keys[key]:
                    continue
                
                if isinstance(obj.config[key], basestring):
                    user_val = obj.config[key]
                elif isinstance(obj.config[key], bool):
                    user_val = str(obj.config[key])
                elif isinstance(obj.config[key], int):
                    user_val = str(obj.config[key])
                
                elif isinstance(obj.config[key], list):
                    user_val = str(obj.config[key])[1:-1]
                else:
                    continue
                
                val = raw_input(key+' ['+user_val+']: ')
                
                # Empty user input? Default to current value
                if not val:
                    val = obj.config[key]
                
                if type(obj.config[key]) is type(val):
                    config_file[key] = val
                elif isinstance(obj.config[key], basestring):
                    config_file[key] = val
                elif isinstance(obj.config[key], bool):
                    config_file[key] = bool(val)
                elif isinstance(obj.config[key], int):
                    config_file[key] = int(val)
                
                elif isinstance(obj.config[key], list):
                    print key + ' = ' + val
                    entry = ConfigObj([key + ' = ' + val])
                    print entry
                    config_file[key] = entry[key]
                else:
                    continue
                
            config_file.write()
            
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
        except KeyboardInterrupt:
            print
            sys.exit()
