<!--This file was generated from the python source
Please edit the source to make changes
-->
DiskSpaceCollector
=====

Uses /proc/mounts and os.statvfs() to get disk space usage

#### Dependencies

 * /proc/mounts

#### Examples

    # no exclude filters at all
    exclude_filters =,

    # exclude everything that begins /boot or /mnt
    exclude_filters = ^/boot, ^/mnt

    # exclude everything that includes the letter 'm'
    exclude_filters = m,


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte, | Default numeric output(s) | list
enabled | False | Enable collecting these metrics | bool
exclude_filters | ^/export/home, | A list of regex patterns. Any filesystem matching any of these patterns will be excluded from disk space metrics collection | list
filesystems | ext2, ext3, ext4, xfs, glusterfs, nfs, nfs4,  ntfs, hfs, fat32, fat16, btrfs | filesystems to examine | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
servers.hostname.diskspace.root.gigabyte_avail (1020.962, 2)
servers.hostname.diskspace.root.gigabyte_free (1090.826, 2)
servers.hostname.diskspace.root.gigabyte_used (284.525, 2)
servers.hostname.diskspace.root.inodes_avail 91229495
servers.hostname.diskspace.root.inodes_free 91229495
servers.hostname.diskspace.root.inodes_used 348873
```

