# coding=utf-8

"""
Uses lsof to collect data on number of open files per user per type

To report the correct values, the user running diamond may need to run lsof as sudo:

Run:
`sudo visudo -f /etc/sudoers.d/diamond`

And add this content (with user = diamond, and path to lsof = /usr/bin/lsof):
```
diamond ALL = NOPASSWD: /usr/bin/lsof
```

#### Config Options

 Check Options table below

*** Priority Explanation ***
 This is an explanation of the priority in which users, groups, and uid, are
    evaluated. EXCLUDE ALWAYS OVERRULES INCLUDE within the same level (ie within
    users or group)
  * user_include/exclude (top level/priority)
    * group_include/exclude (second level: if user not in user_include/exclude,
          groups takes affect)
      * uid_min/max (third level: if user not met above qualifications, uids
            take affect)

 * type_include - This is a list of file types to collect ('REG', 'DIR", 'FIFO'
    , etc). If left empty, will collect for all file types. (Note: it suggested
    to not leave type_include empty, as it would add significant load to your
    graphite box(es) (default = None)
 * type_exclude - This is a list of tile types to exclude from being collected
    for. If left empty, no file types will be excluded. (default = None)

 * collect_user_data - This enables or disables the collection of user specific
    file handles. (default = False)

#### Dependencies

 * /proc/sys/fs/file-nr
 * /usr/sbin/lsof

"""

import diamond.collector
from diamond.collector import str_to_bool
import re
import os
import subprocess

_RE = re.compile(r'(\d+)\s+(\d+)\s+(\d+)')


def parse_lsof_output(file_obj, users, types):
    """
    Format for "lsof -F tL":

    p PID
    L username
    repeated multiple times:
        f file descriptor
        t file type
    """
    fd_type = ''
    user = ''

    d = {}

    for line in file_obj:
        key = line[0]
        val = line[1:].rstrip('\n')
        if key == 'p':
            user = ''
            fd_type = ''
        if key == 'L':
            user = val
        if key == 't':
            fd_type = val

            if user not in users:
                continue
            if fd_type not in types:
                continue

            if user not in d:
                d[user] = {}
            if fd_type not in d[user]:
                d[user][fd_type] = 0
            d[user][fd_type] += 1

    return d


class FilestatCollector(diamond.collector.Collector):

    PROC = '/proc/sys/fs/file-nr'

    def get_default_config_help(self):
        config_help = super(FilestatCollector, self).get_default_config_help()
        config_help.update({
            'use_sudo': 'Use sudo?',
            'sudo_cmd': 'Path to sudo',
            'user_include': "This is list of users to collect data for."
                            " If this is left empty, its a wildcard"
                            " to collector for all users"
                            " (default = None)",
            'user_exclude': "This is a list of users to exclude"
                            " from collecting data. If this is left empty,"
                            " no specific users will be excluded"
                            " (default = None)",
            'group_include': "This is a list of groups to include"
                             " in data collection. This DOES NOT"
                             " override user_exclude."
                             " (default = None)",
            'group_exclude': "This is a list of groups to exclude"
                             " from collecting data. It DOES NOT override"
                             " user_include. (default = None)",
            'uid_min': "This creates a floor for the user's uid."
                       " This means that it WILL NOT collect data"
                       " for any user with a uid LOWER"
                       " than the specified minimum,"
                       " unless the user is told to be included"
                       " by user_include (default = 0)",
            'uid_max': "This creates a ceiling for the user's uid."
                       " This means that it WILL NOT collect data"
                       " for any user with a uid HIGHER"
                       " than the specified maximum,"
                       " unless the user is told to be included"
                       " by user_include (default = 65536)",
            'type_include': "This is a list of file types to collect"
                            " ('REG', 'DIR', 'FIFO', etc). If left empty,"
                            " will collect for all file types."
                            "(Note: it's suggested to not leave"
                            " type_include empty,"
                            " as it would add significant load"
                            " to your graphite box(es) (default = None)",
            'type_exclude': "This is a list of tile types to exclude"
                            " from being collected for. If left empty,"
                            " no file types will be excluded. (default = None)",
            'collect_user_data': "This enables or disables"
                                 " the collection of user specific"
                                 " file handles. (default = False)"
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(FilestatCollector, self).get_default_config()
        config.update({
            'path': 'files',
            'user_include': None,
            'user_exclude': None,
            'group_include': None,
            'group_exclude': None,
            'uid_min': 0,
            'uid_max': 65536,
            'type_include': None,
            'type_exclude': None,
            'collect_user_data': False,
            'use_sudo': False,
            'sudo_cmd': '/usr/bin/sudo',
        })
        return config

    def get_output(self, fmt):

        command = ['lsof', '-F', fmt]
        if str_to_bool(self.config['use_sudo']):
            command.insert(0, self.config['sudo_cmd'])
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return process.communicate()[0].splitlines()

    def get_userlist(self):
        """
        This collects all the users with open files on the system, and filters
        based on the variables user_include and user_exclude
        """
    # convert user/group  lists to arrays if strings
        if isinstance(self.config['user_include'], basestring):
            self.config['user_include'] = self.config['user_include'].split()
        if isinstance(self.config['user_exclude'], basestring):
            self.config['user_exclude'] = self.config['user_exclude'].split()
        if isinstance(self.config['group_include'], basestring):
            self.config['group_include'] = self.config['group_include'].split()
        if isinstance(self.config['group_exclude'], basestring):
            self.config['group_exclude'] = self.config['group_exclude'].split()

        rawusers = set()
        for line in self.get_output('L'):
            if line.startswith('L'):
                rawusers.add(line[1:].rstrip('\n'))
        rawusers = list(rawusers)

        userlist = []

        # remove any not on the user include list
        if ((self.config['user_include'] is None or
             len(self.config['user_include']) == 0)):
            userlist = rawusers
        else:
            # only work with specified include list, which is added at the end
            userlist = []

        # add any user in the group include list
        addedByGroup = []
        if ((self.config['group_include'] is not None and
             len(self.config['group_include']) > 0)):
            for u in rawusers:
                self.log.info(u)
                # get list of groups of user
                user_groups = os.popen("id -Gn %s" % (u)).read().split()
                for gi in self.config['group_include']:
                    if gi in user_groups and u not in userlist:
                        userlist.append(u)
                        addedByGroup.append(u)
                        break

        # remove any user in the exclude group list
        if ((self.config['group_exclude'] is not None and
             len(self.config['group_exclude']) > 0)):
            # create tmp list to iterate over while editing userlist
            tmplist = userlist[:]
            for u in tmplist:
                # get list of groups of user
                groups = os.popen("id -Gn %s" % (u)).read().split()
                for gi in self.config['group_exclude']:
                    if gi in groups:
                        userlist.remove(u)
                        break

        # remove any that aren't within the uid limits
        # make sure uid_min/max are ints
        self.config['uid_min'] = int(self.config['uid_min'])
        self.config['uid_max'] = int(self.config['uid_max'])
        tmplist = userlist[:]
        for u in tmplist:
            if ((self.config['user_include'] is None or
                 u not in self.config['user_include'])):
                if u not in addedByGroup:
                    uid = int(os.popen("id -u %s" % (u)).read())
                    if ((uid < self.config['uid_min'] and
                         self.config['uid_min'] is not None and
                         u in userlist)):
                        userlist.remove(u)
                    if ((uid > self.config['uid_max'] and
                         self.config['uid_max'] is not None and
                         u in userlist)):
                        userlist.remove(u)

        # add users that are in the users include list
        if ((self.config['user_include'] is not None and
             len(self.config['user_include']) > 0)):
            for u in self.config['user_include']:
                if u in rawusers and u not in userlist:
                    userlist.append(u)

        # remove any that is on the user exclude list
        if ((self.config['user_exclude'] is not None and
             len(self.config['user_exclude']) > 0)):
            for u in self.config['user_exclude']:
                if u in userlist:
                    userlist.remove(u)

        return userlist

    def get_typelist(self):
        """
        This collects all avaliable types and applies include/exclude filters
        """
        typelist = []

        # convert type list into arrays if strings
        if isinstance(self.config['type_include'], basestring):
            self.config['type_include'] = self.config['type_include'].split()
        if isinstance(self.config['type_exclude'], basestring):
            self.config['type_exclude'] = self.config['type_exclude'].split()

        # remove any not in include list
        if self.config['type_include'] is None or len(
                self.config['type_include']) == 0:

            typelist = set()
            for line in self.get_output('t'):
                if line.startswith('t'):
                    typelist.add(line[1:].rstrip('\n'))
            typelist = list(typelist)
        else:
            typelist = self.config['type_include']

        # remove any in the exclude list
        if self.config['type_exclude'] is not None and len(
                self.config['type_include']) > 0:
            for t in self.config['type_exclude']:
                if t in typelist:
                    typelist.remove(t)

        return typelist

    def process_lsof(self, users, types):
        """
        Get the list of users and file types to collect for and collect the
        data from lsof
        """
        return parse_lsof_output(self.get_output('tL'), users, types)

    def collect(self):
        if not os.access(self.PROC, os.R_OK):
            return None

        # collect total open files
        with open(self.PROC) as proc_file:
            for line in proc_file:
                match = _RE.match(line)
                if match:
                    self.publish('assigned', int(match.group(1)))
                    self.publish('unused', int(match.group(2)))
                    self.publish('max', int(match.group(3)))

        # collect open files per user per type
        if self.config['collect_user_data']:
            data = self.process_lsof(self.get_userlist(), self.get_typelist())
            for ukey in data.iterkeys():
                for tkey in data[ukey].iterkeys():
                    self.log.debug('files.user.%s.%s %s' % (
                        ukey, tkey, int(data[ukey][tkey])))
                    self.publish('user.%s.%s' % (ukey, tkey),
                                 int(data[ukey][tkey]))
