StatsCollector
=====


This is a slightly unusual 'collector'. It collects and uploads stats to a
app engine instance run by Rob Smith. The stats collected are:

 * Per collector enabled or not
 * Per collector interval time
 * Global collector reload interval
 * Global handlers
 * Any custom collector set stats

These stats are stored anonymously (other then UUID), processed and the results
are at [http://diamond-stats.appspot.com/](http://diamond-stats.appspot.com/).

These values can help us know more about how Diamond is being used and can help
us target development efforts in the future.

#### Requirements

You can install Smolt and run it once or run the following from a terminal

Linux:

 * mkdir /etc/smolt
 * cd /etc/smolt
 * cat /proc/sys/kernel/random/uuid > hw-uuid

Others:

 * mkdir /etc/smolt
 * cd /etc/smolt
 * curl -Lo- http://utils.kormoc.com/uuid/get.php > hw-uuid

#### Dependencies

 * /etc/smolt/hw-uuid
 * urllib
 * json/simplejson


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
<tr><td>url</td><td>http://diamond-stats.appspot.com/submitstats</td><td>The url to post stats to.</td><td>str</td></tr>
<tr><td>uuidfile</td><td>/etc/smolt/hw-uuid</td><td>The path to the uuid file</td><td>str</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

