# coding=utf-8

"""
Collect linux RAID/md state by parsing /proc/mdstat.
https://raid.wiki.kernel.org/index.php/Mdstat

#### Dependencies

 * /proc/mdstat

"""

import diamond.collector
import re


class MdStatCollector(diamond.collector.Collector):
    MDSTAT_PATH = '/proc/mdstat'

    def get_default_config_help(self):
        config_help = super(MdStatCollector, self).get_default_config_help()
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MdStatCollector, self).get_default_config()
        config.update({
            'path': 'mdstat',
        })
        return config

    def process_config(self):
        super(MdStatCollector, self).process_config()

    def collect(self):
        """Publish all mdstat metrics."""
        def traverse(d, metric_name=''):
            for key, value in d.iteritems():
                if isinstance(value, dict):
                    if metric_name == '':
                        metric_name_next = key
                    else:
                        metric_name_next = metric_name + '.' + key
                    traverse(value, metric_name_next)
                else:
                    metric_name_finished = metric_name + '.' + key
                    self.publish_gauge(
                        name=metric_name_finished,
                        value=value,
                        precision=1
                    )

        md_state = self.parse_mdstat()

        traverse(md_state, '')

    def parse_mdstat(self):
        """
        Parse /proc/mdstat.

        File format:
        The first line is the "Personalities" line.
        It won't get parsed since it contains only string metrics.
        The second to second-last lines contain raid array information.
        The last line contains the unused devices.
        It won't get parsed since it contains only string metrics.

        :return: Parsed information
        :rtype: dict
        """

        arrays = {}
        mdstat_array_blocks = ''

        try:
            with open(self.MDSTAT_PATH, 'r') as f:
                lines = f.readlines()
        except IOError as err:
            self.log.exception(
                'Error opening {mdstat_path} for reading: {err}'.format(
                    mdstat_path=self.MDSTAT_PATH,
                    err=err
                )
            )
            return arrays

        for line in lines[1:-1]:
            # remove first and last line
            # reverse readlines() afterwards
            mdstat_array_blocks += line

        if mdstat_array_blocks == '':
            # no md arrays found
            return arrays
        for block in mdstat_array_blocks.split('\n\n'):
            md_device_name = self.parse_mdstat_device_name(block)
            if md_device_name:
                # this block contains a whitelisted md device name
                arrays[md_device_name] = {
                    'member_count': self.parse_array_member_state(block),
                    'status': self.parse_mdstat_array_status(block),
                    'bitmap': self.parse_mdstat_array_bitmap(block),
                    'recovery': self.parse_mdstat_array_recovery(block)
                }
                if not arrays[md_device_name]['bitmap']:
                    arrays[md_device_name].pop('bitmap')
                if not arrays[md_device_name]['recovery']:
                    arrays[md_device_name].pop('recovery')

        return arrays

    def parse_mdstat_device_name(self, block):
        """
        Parse and match for a whitelisted md device name.

        >>> block = 'md0 : active raid1 sdd2[0] sdb2[2](S) sdc2[1]\n'
        >>>         '      100171776 blocks super 1.2 [2/2] [UU]\n'
        >>>         '      bitmap: 1/1 pages [4KB], 65536KB chunk\n\n'
        >>> print parse_mdstat_device_name(block)
        md0

        :return: matched device name or None
        :rtype: string
        """
        return block.split('\n')[0].split(' : ')[0]

    def parse_array_member_state(self, block):
        """
        Parses the state of the the md array members.

        >>> block = 'md0 : active raid1 sdd2[0] sdb2[2](S) sdc2[1]\n'
        >>>         '      100171776 blocks super 1.2 [2/2] [UU]\n'
        >>>         '      bitmap: 1/1 pages [4KB], 65536KB chunk\n\n'
        >>> print parse_array_member_state(block)
        {
            'active': 2,
            'faulty': 0,
            'spare': 1
        }

        :return: dictionary of states with according count
        :rtype: dict
        """
        devices = block.split('\n')[0].split(' : ')[1].split(' ')[2:]

        device_regexp = re.compile(
            '^(?P<device_name>.*)'
            '\[(?P<role_number>\d*)\]'
            '\(?(?P<device_state>[FS])?\)?$'
        )

        ret = {
            'active': 0,
            'faulty': 0,
            'spare': 0
        }
        for device in devices:
            device_dict = device_regexp.match(device).groupdict()

            if device_dict['device_state'] == 'S':
                ret['spare'] += 1
            elif device_dict['device_state'] == 'F':
                ret['faulty'] += 1
            else:
                ret['active'] += 1

        return ret

    def parse_mdstat_array_status(self, block):
        """
        Parses the status of the md array.

        >>> block = 'md0 : active raid1 sdd2[0] sdb2[2](S) sdc2[1]\n'
        >>>         '      100171776 blocks super 1.2 [2/2] [UU]\n'
        >>>         '      bitmap: 1/1 pages [4KB], 65536KB chunk\n\n'
        >>> print parse_mdstat_array_status(block)
        {
            'total_members': '2',
            'actual_members': '2',
            'algorithm': None,
            'superblock_version': '1.2',
            'chunk_size': None,
            'blocks': '100171776'
        }

        :return: dictionary of status information
        :rtype: dict
        """
        array_status_regexp = re.compile(
            '^ *(?P<blocks>\d*) blocks '
            '(?:super (?P<superblock_version>\d\.\d) )?'
            '(?:level (?P<raid_level>\d), '
            '(?P<chunk_size>\d*)k chunk, '
            'algorithm (?P<algorithm>\d) )?'
            '(?:\[(?P<total_members>\d*)/(?P<actual_members>\d*)\])?'
            '(?:(?P<rounding_factor>\d*)k rounding)?.*$'
        )

        array_status_dict = \
            array_status_regexp.match(block.split('\n')[1]).groupdict()

        array_status_dict_sanitizied = {}

        # convert all non None values to float
        for key, value in array_status_dict.iteritems():
            if not value:
                continue
            if key == 'superblock_version':
                array_status_dict_sanitizied[key] = float(value)
            else:
                array_status_dict_sanitizied[key] = int(value)

        if 'chunk_size' in array_status_dict_sanitizied:
            # convert chunk size from kBytes to Bytes
            array_status_dict_sanitizied['chunk_size'] *= 1024

        if 'rounding_factor' in array_status_dict_sanitizied:
            # convert rounding_factor from kBytes to Bytes
            array_status_dict_sanitizied['rounding_factor'] *= 1024

        return array_status_dict_sanitizied

    def parse_mdstat_array_bitmap(self, block):
        """
        Parses the bitmap status of the md array.

        >>> block = 'md0 : active raid1 sdd2[0] sdb2[2](S) sdc2[1]\n'
        >>>         '      100171776 blocks super 1.2 [2/2] [UU]\n'
        >>>         '      bitmap: 1/1 pages [4KB], 65536KB chunk\n\n'
        >>> print parse_mdstat_array_bitmap(block)
        {
            'total_pages': '1',
            'allocated_pages': '1',
            'page_size': 4096,
            'chunk_size': 67108864
        }

        :return: dictionary of status information
        :rtype: dict
        """
        array_bitmap_regexp = re.compile(
            '^ *bitmap: (?P<allocated_pages>[0-9]*)/'
            '(?P<total_pages>[0-9]*) pages '
            '\[(?P<page_size>[0-9]*)KB\], '
            '(?P<chunk_size>[0-9]*)KB chunk.*$',
            re.MULTILINE
        )

        regexp_res = array_bitmap_regexp.search(block)

        if not regexp_res:
            return None

        array_bitmap_dict = regexp_res.groupdict()

        array_bitmap_dict_sanitizied = {}

        # convert all values to int
        for key, value in array_bitmap_dict.iteritems():
                if not value:
                    continue
                array_bitmap_dict_sanitizied[key] = int(value)

        # scale page_size to bytes
        array_bitmap_dict_sanitizied['page_size'] *= 1024

        # scale chunk_size to bytes
        array_bitmap_dict_sanitizied['chunk_size'] *= 1024

        return array_bitmap_dict

    def parse_mdstat_array_recovery(self, block):
        """
        Parses the recovery progress of the md array.

        >>> block = 'md0 : active raid1 sdd2[0] sdb2[2](S) sdc2[1]\n'
        >>>         '      100171776 blocks super 1.2 [2/2] [UU]\n'
        >>>         '      [===================>.]  recovery = 99.5% '
        >>>         '(102272/102272) finish=13.37min speed=102272K/sec\n'
        >>>         '\n'
        >>> print parse_mdstat_array_recovery(block)
        {
            'percent': '99.5',
            'speed': 104726528,
            'remaining_time': 802199
        }

        :return: dictionary of recovery progress information
        :rtype: dict
        """
        array_recovery_regexp = re.compile(
            '^ *\[.*\] *recovery = (?P<percent>\d*\.?\d*)%'
            ' \(\d*/\d*\) finish=(?P<remaining_time>\d*\.?\d*)min '
            'speed=(?P<speed>\d*)K/sec$',
            re.MULTILINE
        )

        regexp_res = array_recovery_regexp.search(block)

        if not regexp_res:
            return None

        array_recovery_dict = regexp_res.groupdict()

        array_recovery_dict['percent'] = \
            float(array_recovery_dict['percent'])

        # scale speed to bits
        array_recovery_dict['speed'] = \
            int(array_recovery_dict['speed']) * 1024

        # scale minutes to milliseconds
        array_recovery_dict['remaining_time'] = \
            int(float(array_recovery_dict['remaining_time'])*60*1000)

        return array_recovery_dict
