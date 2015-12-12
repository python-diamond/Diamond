ProcessMemoryCollector
=====

A Diamond collector that collects memory usage of each process defined in it's
config file by matching them with their executable filepath or the process name.
This collector can also be used to collect memory usage for the Diamond process.

Example config file ProcessMemoryCollector.conf

```
enabled=True
unit=kB
[process]
[[postgres]]
exe=^\/usr\/lib\/postgresql\/+d.+d\/bin\/postgres$
name=^postgres,^pg

[[diamond]]
selfmon=True
```

exe and name are both lists of comma-separated regexps.
#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>process</td><td></td><td>A subcategory of settings inside of which each collected process has it's configuration</td><td>str</td></tr>
<tr><td>unit</td><td>B</td><td>The unit in which memory data is collected.</td><td>str</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

