# coding=utf-8

import configobj
import os


def load_config(configfile):
    """
    Load the full config / merge splitted configs if configured
    """

    configfile = os.path.abspath(configfile)
    config = configobj.ConfigObj(configfile)
    config['configfile'] = configfile
    try:
        for cfgfile in os.listdir(config['configs']['path']):
            if cfgfile.endswith(config['configs']['extension']):
                newconfig = configobj.ConfigObj(
                    config['configs']['path'] + cfgfile)
                config.merge(newconfig)
    except KeyError:
            pass

    if 'server' not in config:
        raise Exception('Failed to reload config file %s!' % configfile)

    return config
