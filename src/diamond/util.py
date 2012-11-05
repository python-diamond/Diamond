# coding=utf-8

import os
import sys
import inspect


def get_diamond_version():
    try:
        from diamond.version import __VERSION__
        return __VERSION__
    except ImportError:
        return "Unknown"


def load_modules_from_path(path):
    """
    Import all modules from the given directory
    """
    # Check and fix the path
    if path[-1:] != '/':
        path += '/'

    # Get a list of files in the directory, if the directory exists
    if not os.path.exists(path):
        raise OSError("Directory does not exist: %s" % path)

    # Add path to the system path
    sys.path.append(path)
    # Load all the files in path
    for f in os.listdir(path):
        # Ignore anything that isn't a .py file
        if len(f) > 3 and f[-3:] == '.py':
            modname = f[:-3]
            # Import the module
            __import__(modname, globals(), locals(), ['*'])


def load_class_from_name(fqcn):
    # Break apart fqcn to get module and classname
    paths = fqcn.split('.')
    modulename = '.'.join(paths[:-1])
    classname = paths[-1]
    # Import the module
    __import__(modulename, globals(), locals(), ['*'])
    # Get the class
    cls = getattr(sys.modules[modulename], classname)
    # Check cls
    if not inspect.isclass(cls):
        raise TypeError("%s is not a class" % fqcn)
    # Return class
    return cls
