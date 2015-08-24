#!/usr/bin/env python
# coding=utf-8
##########################################################################

from __future__ import print_function
import configobj
import optparse
import os
import shutil
import sys
import tempfile
import traceback

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'src')))


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

                    if cls.__module__ != modname:
                        continue

                    if cls.__name__ not in collectors:
                        collectors[cls.__name__] = module
            except Exception:
                print("Failed to import module: %s. %s" % (
                    modname, traceback.format_exc()))
                collectors[modname] = False

        elif os.path.isdir(cPath):
            getCollectors(cPath)

handlers = {}


def getHandlers(path, name=None):
    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))

        if os.path.isfile(cPath) and len(f) > 3 and f.endswith('.py'):
            modname = f[:-3]

            if name and f is not "%s.py" % name:
                break

            try:
                # Import the module
                module = __import__(modname, globals(), locals(), ['*'])

                # Find the name
                for attr in dir(module):
                    if ((not attr.endswith('Handler') or
                         attr.startswith('Handler'))):
                        continue

                    cls = getattr(module, attr)

                    if cls.__name__ not in handlers:
                        handlers[cls.__name__] = module
            except Exception:
                print("Failed to import module: %s. %s" % (
                    modname, traceback.format_exc()))
                handlers[modname] = False

        elif os.path.isdir(cPath):
            getHandlers(cPath)


def writeDocHeader(docFile):
    docFile.write("<!--")
    docFile.write("This file was generated from the python source\n")
    docFile.write("Please edit the source to make changes\n")
    docFile.write("-->\n")


def writeDocString(docFile, name, doc):
    docFile.write("%s\n" % (name))
    docFile.write("=====\n")
    if doc is None:
        print("No __doc__ string for %s!" % name)
    docFile.write("%s\n" % doc)


def writeDocOptionsHeader(docFile):
    docFile.write("#### Options\n")
    docFile.write("\n")

    docFile.write("Setting | Default | Description | Type\n")
    docFile.write("--------|---------|-------------|-----\n")


def writeDocOptions(docFile, options, default_options):
    for option in sorted(options.keys()):
        defaultOption = ''
        defaultOptionType = ''
        if option in default_options:
            defaultOptionType = default_options[option].__class__.__name__
            if isinstance(default_options[option], list):
                defaultOption = ', '.join(map(str, default_options[option]))
                defaultOption += ','
            else:
                defaultOption = str(default_options[option])

        docFile.write("%s | %s | %s | %s\n"
                      % (option,
                         defaultOption,
                         options[option].replace("\n", '<br>\n'),
                         defaultOptionType))


def writeDoc(items, type_name, doc_path):
    for item in sorted(items.iterkeys()):

        # Skip configuring the basic item object
        if item == type_name:
            continue
        if item.startswith('Test'):
            continue

        print("Processing %s..." % (item))

        if not hasattr(items[item], item):
            continue

        cls = getattr(items[item], item)

        item_options = None
        default_options = None

        try:
            tmpfile = None
            if type_name is "Collector":
                obj = cls(config=config, handlers={})
            elif type_name is "Handler":
                tmpfile = tempfile.mkstemp()
                obj = cls({'log_file': tmpfile[1]})

            item_options = obj.get_default_config_help()
            default_options = obj.get_default_config()
            if type_name is "Handler":
                os.remove(tmpfile[1])
        except Exception, e:
            print("Caught Exception %s" % e)

        docFile = open(os.path.join(doc_path, item + ".md"), 'w')

        enabled = ''

        writeDocHeader(docFile)
        writeDocString(docFile, item, items[item].__doc__)
        writeDocOptionsHeader(docFile)

        if item_options:
            writeDocOptions(docFile, item_options, default_options)

        if type_name is "Collector":
            docFile.write("\n")
            docFile.write("#### Example Output\n")
            docFile.write("\n")
            docFile.write("```\n")
            docFile.write("__EXAMPLESHERE__\n")
            docFile.write("```\n")
            docFile.write("\n")

        docFile.close()

##########################################################################

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
    parser.add_option("-H", "--handler",
                      dest="handler",
                      default=None,
                      help="Configure a single handler")
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
        print("ERROR: Config file: %s does not exist." % (
            options.configfile), file=sys.stderr)
        print("Please run python config.py -c /path/to/diamond.conf",
              file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    docs_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'docs'))

    if options.collector or (not options.collector and not options.handler):
        collector_path = config['server']['collectors_path']
        collectors_doc_path = os.path.join(docs_path, "collectors")
        getIncludePaths(collector_path)

        if options.collector:
            single_collector_path = os.path.join(collector_path,
                                                 options.collector)
            getCollectors(single_collector_path)
        else:
            # Ugly hack for snmp collector overrides
            getCollectors(os.path.join(collector_path, 'snmp'))
            getCollectors(collector_path)

            shutil.rmtree(collectors_doc_path)
            os.mkdir(collectors_doc_path)

        writeDoc(collectors, "Collector", collectors_doc_path)

    if options.handler or (not options.collector and not options.handler):
        handler_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    'src',
                                                    'diamond',
                                                    'handler'))
        handlers_doc_path = os.path.join(docs_path, "handlers")
        getIncludePaths(handler_path)

        if options.handler:
            getHandlers(handler_path, name=options.handler)
        else:
            getHandlers(handler_path)
            shutil.rmtree(handlers_doc_path)
            os.mkdir(handlers_doc_path)

        writeDoc(handlers, "Handler", handlers_doc_path)
