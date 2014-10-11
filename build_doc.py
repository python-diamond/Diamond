#!/usr/bin/env python
# coding=utf-8
################################################################################

import os
import sys
import optparse
import configobj
import traceback
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))


def getIncludePaths(path):
    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))

        if os.path.isfile(cPath) and len(f) > 3 and f.endswith('.py'):
            sys.path.append(os.path.dirname(cPath))

        elif os.path.isdir(cPath):
            getIncludePaths(cPath)

collectors = {}


def getCollectors(path):
    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))

        if os.path.isfile(cPath) and len(f) > 3 and f.endswith('.py'):
            modname = f[:-3]

            if modname.startswith('Test'):
                continue
            if modname.startswith('test'):
                continue

            try:
                # Import the module
                module = __import__(modname, globals(), locals(), ['*'])

                # Find the name
                for attr in dir(module):
                    if not attr.endswith('Collector'):
                        continue

                    cls = getattr(module, attr)

                    if cls.__name__ not in collectors:
                        collectors[cls.__name__] = module
            except Exception:
                print "Failed to import module: %s. %s" % (
                    modname, traceback.format_exc())
                collectors[modname] = False

        elif os.path.isdir(cPath):
            getCollectors(cPath)

handlers = {}


def getHandlers(path):
    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))

        if os.path.isfile(cPath) and len(f) > 3 and f.endswith('.py'):
            modname = f[:-3]

            try:
                # Import the module
                module = __import__(modname, globals(), locals(), ['*'])

                # Find the name
                for attr in dir(module):
                    if (not attr.endswith('Handler')
                            or attr.startswith('Handler')):
                        continue

                    cls = getattr(module, attr)

                    if cls.__name__ not in handlers:
                        handlers[cls.__name__] = module
            except Exception:
                print "Failed to import module: %s. %s" % (
                    modname, traceback.format_exc())
                handlers[modname] = False

        elif os.path.isdir(cPath):
            getHandlers(cPath)

################################################################################

if __name__ == "__main__":

    # Initialize Options
    parser = optparse.OptionParser()
    parser.add_option("-c", "--configfile",
                      dest="configfile",
                      default="/etc/diamond/diamond.conf",
                      help="Path to the config file")
    parser.add_option("-C", "--collector",
                      dest="collector",
                      default=None,
                      help="Configure a single collector")
    parser.add_option("-p", "--print",
                      action="store_true",
                      dest="dump",
                      default=False,
                      help="Just print the defaults")

    # Parse Command Line Args
    (options, args) = parser.parse_args()

    # Initialize Config
    if os.path.exists(options.configfile):
        config = configobj.ConfigObj(os.path.abspath(options.configfile))
    else:
        print >> sys.stderr, "ERROR: Config file: %s does not exist." % (
            options.configfile)
        print >> sys.stderr, ("Please run python config.py -c "
                              + "/path/to/diamond.conf")
        parser.print_help(sys.stderr)
        sys.exit(1)

    collector_path = config['server']['collectors_path']
    docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'docs'))
    handler_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'src', 'diamond', 'handler'))

    getIncludePaths(collector_path)

    # Ugly hack for snmp collector overrides
    getCollectors(os.path.join(collector_path, 'snmp'))
    getCollectors(collector_path)

    collectorIndexFile = open(os.path.join(docs_path, "Collectors.md"), 'w')
    collectorIndexFile.write("## Collectors\n")
    collectorIndexFile.write("\n")
    collectorIndexFile.write("Note that the default collectors are noted via "
                             + "the super-script symbol <sup>♦</sup>.\n")
    collectorIndexFile.write("\n")

    for collector in sorted(collectors.iterkeys()):

        # Skip configuring the basic collector object
        if collector == "Collector":
            continue
        if collector.startswith('Test'):
            continue

        print "Processing %s..." % (collector)

        if not hasattr(collectors[collector], collector):
            continue

        cls = getattr(collectors[collector], collector)

        obj = cls(config=config, handlers={})

        options = obj.get_default_config_help()

        defaultOptions = obj.get_default_config()

        docFile = open(os.path.join(docs_path,
                                    "collectors-" + collector + ".md"), 'w')

        enabled = ''
        if defaultOptions['enabled']:
            enabled = ' <sup>♦</sup>'

        collectorIndexFile.write(" - [%s](collectors-%s)%s\n" % (collector,
                                                                 collector,
                                                                 enabled))

        docFile.write("%s\n" % (collector))
        docFile.write("=====\n")
        if collectors[collector].__doc__ is None:
            print "No __doc__ string!"
        docFile.write("%s\n" % (collectors[collector].__doc__))
        docFile.write("#### Options - [Generic Options](Configuration)\n")
        docFile.write("\n")

        docFile.write("<table>")

        docFile.write("<tr>")
        docFile.write("<th>Setting</th>")
        docFile.write("<th>Default</th>")
        docFile.write("<th>Description</th>")
        docFile.write("<th>Type</th>")
        docFile.write("</tr>\n")

        for option in sorted(options.keys()):
            defaultOption = ''
            defaultOptionType = ''
            if option in defaultOptions:
                defaultOptionType = defaultOptions[option].__class__.__name__
                if isinstance(defaultOptions[option], list):
                    defaultOption = ', '.join(map(str, defaultOptions[option]))
                    defaultOption += ','
                else:
                    defaultOption = str(defaultOptions[option])

            docFile.write("<tr>")
            docFile.write("<td>%s</td>" % (option))
            docFile.write("<td>%s</td>" % (defaultOption))
            docFile.write("<td>%s</td>" % (options[option].replace(
                "\n", '<br>\n')))
            docFile.write("<td>%s</td>" % (defaultOptionType))
            docFile.write("</tr>\n")

        docFile.write("</table>\n")

        docFile.write("\n")
        docFile.write("#### Example Output\n")
        docFile.write("\n")
        docFile.write("```\n")
        docFile.write("__EXAMPLESHERE__\n")
        docFile.write("```\n")
        docFile.write("\n")
        docFile.write("### This file was generated from the python source\n")
        docFile.write("### Please edit the source to make changes\n")
        docFile.write("\n")

        docFile.close()

    collectorIndexFile.close()

    getIncludePaths(handler_path)
    getHandlers(handler_path)

    handlerIndexFile = open(os.path.join(docs_path, "Handlers.md"), 'w')
    handlerIndexFile.write("## Handlers\n")
    handlerIndexFile.write("\n")

    for handler in sorted(handlers.iterkeys()):

        # Skip configuring the basic handler object
        if handler == "Handler":
            continue

        if handler[0:4] == "Test":
            continue

        print "Processing %s..." % (handler)

        if not hasattr(handlers[handler], handler):
            continue

        cls = getattr(handlers[handler], handler)

        tmpfile = tempfile.mkstemp()

        options = None
        defaultOptions = None

        try:
            obj = cls({
                'log_file': tmpfile[1],
                })

            options = obj.get_default_config_help()
            defaultOptions = obj.get_default_config()
        except Exception, e:
            print "Caught Exception %s" % e

        os.remove(tmpfile[1])

        docFile = open(os.path.join(docs_path,
                                    "handler-" + handler + ".md"), 'w')

        handlerIndexFile.write(" - [%s](handler-%s)\n" % (handler, handler))

        docFile.write("%s\n" % (handler))
        docFile.write("====\n")
        docFile.write("%s" % (handlers[handler].__doc__))

        docFile.write("#### Options - [Generic Options](Configuration)\n")
        docFile.write("\n")

        docFile.write("<table>")

        docFile.write("<tr>")
        docFile.write("<th>Setting</th>")
        docFile.write("<th>Default</th>")
        docFile.write("<th>Description</th>")
        docFile.write("<th>Type</th>")
        docFile.write("</tr>\n")

        if options:
            for option in sorted(options.keys()):
                defaultOption = ''
                defaultOptionType = ''
                if option in defaultOptions:
                    defaultOptionType = defaultOptions[
                        option].__class__.__name__
                    if isinstance(defaultOptions[option], list):
                        defaultOption = ', '.join(map(str,
                                                      defaultOptions[option]))
                        defaultOption += ','
                    else:
                        defaultOption = str(defaultOptions[option])

                docFile.write("<tr>")
                docFile.write("<td>%s</td>" % (option))
                docFile.write("<td>%s</td>" % (defaultOption))
                docFile.write("<td>%s</td>" % (options[option].replace(
                    "\n", '<br>\n')))
                docFile.write("<td>%s</td>" % (defaultOptionType))
                docFile.write("</tr>\n")

        docFile.write("</table>\n")

        docFile.write("\n")
        docFile.write("### This file was generated from the python source\n")
        docFile.write("### Please edit the source to make changes\n")
        docFile.write("\n")

        docFile.close()

    handlerIndexFile.close()
