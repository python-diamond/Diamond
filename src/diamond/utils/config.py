# coding=utf-8

import configobj
import os


def str_to_bool(value):
    """
    Converts string truthy/falsey strings to a bool
    Empty strings are false
    """
    if isinstance(value, basestring):
        value = value.strip().lower()
        if value in ['true', 't', 'yes', 'y']:
            return True
        elif value in ['false', 'f', 'no', 'n', '']:
            return False
        else:
            raise NotImplementedError("Unknown bool %s" % value)

    return value


def load_config(configfile):
    """
    Load the full config / merge splitted configs if configured
    """

    configfile = os.path.abspath(configfile)
    config = configobj.ConfigObj(configfile)

    config_extension = '.conf'

    #########################################################################
    # Load up other config files
    #########################################################################

    if 'configs' in config:
        config_extension = config['configs'].get('extension', config_extension)

        # Load other configs
        if 'path' in config['configs']:
            for cfgfile in os.listdir(config['configs']['path']):
                cfgfile = os.path.join(config['configs']['path'],
                                       cfgfile)
                cfgfile = os.path.abspath(cfgfile)
                if not cfgfile.endswith(config_extension):
                    continue
                newconfig = configobj.ConfigObj(cfgfile)
                config.merge(newconfig)

    #########################################################################

    if 'server' not in config:
        raise Exception('Failed to load config file %s!' % configfile)

    #########################################################################
    # Load up handler specific configs
    #########################################################################

    if 'handlers' not in config:
        config['handlers'] = configobj.ConfigObj()

    if 'handlers_config_path' in config['server']:
        for cfgfile in os.listdir(config['server']['handlers_config_path']):
            cfgfile = os.path.join(config['server']['handlers_config_path'],
                                   cfgfile)
            cfgfile = os.path.abspath(cfgfile)
            if not cfgfile.endswith(config_extension):
                continue
            filename = os.path.basename(cfgfile)
            handler = os.path.splitext(filename)[0]

            if handler not in config['handlers']:
                config['handlers'][handler] = configobj.ConfigObj(cfgfile)
            else:
                newconfig = configobj.ConfigObj(cfgfile)
                config['handlers'][handler].merge(newconfig)

    #########################################################################
    # Load up Collector specific configs
    #########################################################################

    if 'collectors' not in config:
        config['collectors'] = configobj.ConfigObj()

    if 'collectors_config_path' in config['server']:
        for cfgfile in os.listdir(config['server']['collectors_config_path']):
            cfgfile = os.path.join(config['server']['collectors_config_path'],
                                   cfgfile)
            cfgfile = os.path.abspath(cfgfile)
            if not cfgfile.endswith(config_extension):
                continue
            filename = os.path.basename(cfgfile)
            collector = os.path.splitext(filename)[0]

            if collector not in config['collectors']:
                config['collectors'][collector] = configobj.ConfigObj(cfgfile)
            else:
                newconfig = configobj.ConfigObj(cfgfile)
                config['collectors'][collector].merge(newconfig)


    # Convert enabled to a bool
    for collector in config['collectors']:
        if 'enabled' in config['collectors'][collector]:
            config['collectors'][collector]['enabled'] = str_to_bool(
                config['collectors'][collector]['enabled']
            )

    #########################################################################

    return config
