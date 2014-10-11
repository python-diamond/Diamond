# coding=utf-8
"""
The function of MountStatsCollector is to parse the detailed per-mount NFS
performance statistics provided by `/proc/self/mountstats` (reads, writes,
remote procedure call count/latency, etc.) and provide counters to Diamond.
Filesystems may be included/excluded using a regular expression filter,
like the existing disk check collectors.

#### Dependencies

 * /proc/self/mountstats

"""

import os
import re
import subprocess

import diamond.collector


class MountStatsCollector(diamond.collector.Collector):
    """Diamond collector for statistics from /proc/self/mountstats
    """

    BYTES_MAP = ['normalreadbytes', 'normalwritebytes', 'directreadbytes',
                 'directwritebytes', 'serverreadbytes', 'serverwritebytes']
    EVENTS_MAP = ['inoderevalidates', 'dentryrevalidates',
                  'datainvalidates', 'attrinvalidates', 'syncinodes',
                  'vfsopen', 'vfslookup', 'vfspermission', 'vfsreadpage',
                  'vfsreadpages', 'vfswritepage', 'vfswritepages',
                  'vfsreaddir', 'vfsflush', 'vfsfsync', 'vfsflock',
                  'vfsrelease', 'setattrtrunc', 'extendwrite',
                  'sillyrenames', 'shortreads', 'shortwrites', 'delay']
    XPRT_MAP = {'rdma': ['port', 'bind_count', 'connect_count',
                         'connect_time', 'idle_time', 'rpcsends',
                         'rpcreceives', 'badxids', 'backlogutil',
                         'read_chunks', 'write_chunks', 'reply_chunks',
                         'total_rdma_req', 'total_dma_rep', 'pullup',
                         'fixup', 'hardway', 'failed_marshal', 'bad_reply'],
                'tcp': ['port', 'bind_count', 'connect_count',
                        'connect_time', 'idle_time', 'rpcsends',
                        'rpcreceives', 'badxids', 'backlogutil'],
                'udp': ['port', 'bind_count', 'rpcsends', 'rpcreceives',
                        'badxids', 'backlogutil']}

    RPCS_MAP = ['ACCESS', 'CLOSE', 'COMMIT', 'CREATE', 'DELEGRETURN',
                'FSINFO', 'FSSTAT', 'FS_LOCATIONS', 'GETACL', 'GETATTR',
                'LINK', 'LOCK', 'LOCKT', 'LOCKU', 'LOOKUP', 'LOOKUP_ROOT',
                'MKDIR', 'MKNOD', 'NULL', 'OPEN', 'OPEN_CONFIRM',
                'OPEN_DOWNGRADE', 'OPEN_NOATTR', 'PATHCONF', 'READ',
                'READDIR', 'READDIRPLUS', 'READLINK', 'REMOVE', 'RENAME',
                'RENEW', 'RMDIR', 'SERVER_CAPS', 'SETACL', 'SETATTR',
                'SETCLIENTID', 'SETCLIENTID_CONFIRM', 'STATFS', 'SYMLINK',
                'WRITE']

    MOUNTSTATS = '/proc/self/mountstats'

    def process_config(self):
        self.exclude_filters = self.config['exclude_filters']
        if isinstance(self.exclude_filters, basestring):
            self.exclude_filters = [self.exclude_filters]

        if len(self.exclude_filters) > 0:
            self.exclude_reg = re.compile('|'.join(self.exclude_filters))
        else:
            self.exclude_reg = None

        self.include_filters = self.config['include_filters']
        if isinstance(self.include_filters, basestring):
            self.include_filters = [self.include_filters]

        if len(self.include_filters) > 0:
            self.include_reg = re.compile('|'.join(self.include_filters))
        else:
            self.include_reg = None

    def get_default_config_help(self):
        config_help = super(MountStatsCollector,
                            self).get_default_config_help()
        config_help.update({
            'exclude_filters': "A list of regex patterns. Any filesystem"
            + " matching any of these patterns will be excluded from"
            + " mount stats metrics collection.",
            'include_filters': "A list of regex patterns. Any filesystem"
            + " matching any of these patterns will be included from"
            + " mount stats metrics collection.",
            'use_sudo': 'Use sudo?',
            'sudo_cmd': 'Path to sudo',
        })
        return config_help

    def get_default_config(self):
        config = super(MountStatsCollector, self).get_default_config()
        config.update({
            'enabled': 'False',
            'exclude_filters': [],
            'include_filters': [],
            'path': 'mountstats',
            'use_sudo': False,
            'sudo_cmd': '/usr/bin/sudo',
        })
        return config

    def collect(self):
        """Collect statistics from /proc/self/mountstats.

        Currently, we do fairly naive parsing and do not actually check
        the statvers value returned by mountstats.
        """

        if self.config['use_sudo']:
            if not os.access(self.config['sudo_cmd'], os.X_OK):
                self.log.error("Cannot find or exec %s"
                               % self.config['sudo_cmd'])
                return None

            command = [self.config['sudo_cmd'], '/bin/cat', self.MOUNTSTATS]
            p = subprocess.Popen(command,
                                 stdout=subprocess.PIPE).communicate()[0][:-1]
            lines = p.split("\n")

        else:
            if not os.access(self.MOUNTSTATS, os.R_OK):
                self.log.error("Cannot read path %s" % self.MOUNTSTATS)
                return None

            f = open(self.MOUNTSTATS)
            lines = f.readlines()
            f.close()

        path = None
        for line in lines:
            tokens = line.split()
            if len(tokens) == 0:
                continue

            if tokens[0] == 'device':
                path = tokens[4]

                skip = False
                if self.exclude_reg:
                    skip = self.exclude_reg.match(path)
                if self.include_reg:
                    skip = not self.include_reg.match(path)

                if skip:
                    self.log.debug("Ignoring %s", path)
                else:
                    self.log.debug("Keeping %s", path)

                path = path.replace('.', '_')
                path = path.replace('/', '_')
            elif skip:
                # If we are in a skip state, don't pay any attention to
                # anything that isn't the next device line
                continue
            elif tokens[0] == 'events:':
                for i in range(0, len(self.EVENTS_MAP)):
                    metric_name = "%s.events.%s" % (path, self.EVENTS_MAP[i])
                    metric_value = long(tokens[i + 1])
                    self.publish_counter(metric_name, metric_value)
            elif tokens[0] == 'bytes:':
                for i in range(0, len(self.BYTES_MAP)):
                    metric_name = "%s.bytes.%s" % (path, self.BYTES_MAP[i])
                    metric_value = long(tokens[i + 1])
                    self.publish_counter(metric_name, metric_value)
            elif tokens[0] == 'xprt:':
                proto = tokens[1]
                if not self.XPRT_MAP[proto]:
                    self.log.error("Unknown protocol %s", proto)
                    continue

                for i in range(0, len(self.XPRT_MAP[proto])):
                    metric_name = "%s.xprt.%s.%s" % (path, proto,
                                                     self.XPRT_MAP[proto][i])
                    metric_value = long(tokens[i + 2])
                    self.publish_counter(metric_name, metric_value)
            elif tokens[0][:-1] in self.RPCS_MAP:
                rpc = tokens[0][:-1]
                ops = long(tokens[1])
                rtt = long(tokens[7])
                exe = long(tokens[8])

                metric_fmt = "%s.rpc.%s.%s"
                ops_name = metric_fmt % (path, rpc.lower(), 'ops')
                rtt_name = metric_fmt % (path, rpc.lower(), 'rtt')
                exe_name = metric_fmt % (path, rpc.lower(), 'exe')

                self.publish_counter(ops_name, ops)
                self.publish_counter(rtt_name, rtt)
                self.publish_counter(exe_name, exe)
