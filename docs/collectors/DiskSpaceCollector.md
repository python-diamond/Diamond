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


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte,</td><td>Default numeric output(s)</td><td>list</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>exclude_filters</td><td>^/export/home,</td><td>A list of regex patterns. Any filesystem matching any of these patterns will be excluded from disk space metrics collection</td><td>list</td></tr>
<tr><td>filesystems</td><td>ext2, ext3, ext4, xfs, glusterfs, nfs, nfs4,  ntfs, hfs, fat32, fat16, btrfs</td><td>filesystems to examine</td><td>str</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

