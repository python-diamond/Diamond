# coding=utf-8

import configobj
import os
import sys
import logging
import inspect
import traceback
import pkg_resources
import imp

from diamond.util import load_class_from_name
from diamond.collector import Collector
from diamond.handler.Handler import Handler

logger = logging.getLogger('diamond')


def load_include_path(paths):
    """
    Scan for and add paths to the include path
    """
    for path in paths:
        # Verify the path is valid
        if not os.path.isdir(path):
            continue
        # Add path to the system path, to avoid name clashes
        # with mysql-connector for example ...
        if path not in sys.path:
            sys.path.insert(1, path)
        # Load all the files in path
        for f in os.listdir(path):
            # Are we a directory? If so process down the tree
            fpath = os.path.join(path, f)
            if os.path.isdir(fpath):
                load_include_path([fpath])


def load_dynamic_class(fqn, subclass):
    """
    Dynamically load fqn class and verify it's a subclass of subclass
    """
    if not isinstance(fqn, basestring):
        return fqn

    cls = load_class_from_name(fqn)

    if cls == subclass or not issubclass(cls, subclass):
        raise TypeError("%s is not a valid %s" % (fqn, subclass.__name__))

    return cls


def load_handlers(config, handler_names):
    """
    Load handlers
    """

    handlers = []

    if isinstance(handler_names, basestring):
        handler_names = [handler_names]

    for handler in handler_names:
        logger.debug('Loading Handler %s', handler)
        try:
            # Load Handler Class
            cls = load_dynamic_class(handler, Handler)
            cls_name = cls.__name__

            # Initialize Handler config
            handler_config = configobj.ConfigObj()
            # Merge default Handler default config
            handler_config.merge(config['handlers']['default'])
            # Check if Handler config exists
            if cls_name in config['handlers']:
                # Merge Handler config section
                handler_config.merge(config['handlers'][cls_name])

            # Check for config file in config directory
            if 'handlers_config_path' in config['server']:
                configfile = os.path.join(
                    config['server']['handlers_config_path'],
                    cls_name) + '.conf'
                if os.path.exists(configfile):
                    # Merge Collector config file
                    handler_config.merge(configobj.ConfigObj(configfile))

            # Initialize Handler class
            h = cls(handler_config)
            handlers.append(h)

        except (ImportError, SyntaxError):
            # Log Error
            logger.warning("Failed to load handler %s. %s",
                           handler,
                           traceback.format_exc())
            continue

    return handlers


def load_collectors(paths):
    """
    Load all collectors
    """
    collectors = load_collectors_from_paths(paths)
    collectors.update(load_collectors_from_entry_point('diamond.collectors'))
    return collectors


def load_collectors_from_paths(paths):
    """
    Scan for collectors to load from path
    """
    # Initialize return value
    collectors = {}

    if paths is None:
        return

    if isinstance(paths, basestring):
        paths = paths.split(',')
        paths = map(str.strip, paths)

    load_include_path(paths)

    for path in paths:
        # Get a list of files in the directory, if the directory exists
        if not os.path.exists(path):
            raise OSError("Directory does not exist: %s" % path)

        if path.endswith('tests') or path.endswith('fixtures'):
            return collectors

        # Load all the files in path
        for f in os.listdir(path):

            # Are we a directory? If so process down the tree
            fpath = os.path.join(path, f)
            if os.path.isdir(fpath):
                subcollectors = load_collectors_from_paths([fpath])
                for key in subcollectors:
                    collectors[key] = subcollectors[key]

            # Ignore anything that isn't a .py file
            elif (os.path.isfile(fpath) and
                  len(f) > 3 and
                  f[-3:] == '.py' and
                  f[0:4] != 'test' and
                  f[0] != '.'):

                modname = f[:-3]

                fp, pathname, description = imp.find_module(modname, [path])

                try:
                    # Import the module
                    mod = imp.load_module(modname, fp, pathname, description)
                except (KeyboardInterrupt, SystemExit) as err:
                    logger.error(
                        "System or keyboard interrupt "
                        "while loading module %s"
                        % modname)
                    if isinstance(err, SystemExit):
                        sys.exit(err.code)
                    raise KeyboardInterrupt
                except Exception:
                    # Log error
                    logger.error("Failed to import module: %s. %s",
                                 modname,
                                 traceback.format_exc())
                else:
                    for name, cls in get_collectors_from_module(mod):
                        collectors[name] = cls
                finally:
                    if fp:
                        fp.close()

    # Return Collector classes
    return collectors


def load_collectors_from_entry_point(path):
    """
    Load collectors that were installed into an entry_point.
    """
    collectors = {}
    for ep in pkg_resources.iter_entry_points(path):
        try:
            mod = ep.load()
        except Exception:
            logger.error('Failed to import entry_point: %s. %s',
                         ep.name,
                         traceback.format_exc())
        else:
            collectors.update(get_collectors_from_module(mod))
    return collectors


def get_collectors_from_module(mod):
    """
    Locate all of the collector classes within a given module
    """
    for attrname in dir(mod):
        attr = getattr(mod, attrname)
        # Only attempt to load classes that are infact classes
        # are Collectors but are not the base Collector class
        if ((inspect.isclass(attr) and
             issubclass(attr, Collector) and
             attr != Collector)):
            if attrname.startswith('parent_'):
                continue
            # Get class name
            fqcn = '.'.join([mod.__name__, attrname])
            try:
                # Load Collector class
                cls = load_dynamic_class(fqcn, Collector)
                # Add Collector class
                yield cls.__name__, cls
            except Exception:
                # Log error
                logger.error(
                    "Failed to load Collector: %s. %s",
                    fqcn, traceback.format_exc())
                continue


def initialize_collector(cls, name=None, configfile=None, handlers=[]):
    """
    Initialize collector
    """
    collector = None

    try:
        # Initialize Collector
        collector = cls(name=name, configfile=configfile, handlers=handlers)
    except Exception:
        # Log error
        logger.error("Failed to initialize Collector: %s. %s",
                     cls.__name__, traceback.format_exc())

    # Return collector
    return collector
