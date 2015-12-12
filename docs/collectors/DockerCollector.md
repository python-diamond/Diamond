DockerCollector
=====

The DockerCollector gathers some metrics about docker containers and images.

#### Dependencies

* docker -- Install via `pip install docker-py`.
  Source https://github.com/docker/docker-py

#### Config

Options:

* `memory_path` -- The path to the kernel's CGroups memory filesystem.
  The auto-detected default is probably correct.

Example config:

```
enabled=True
```

#### Stats

* `containers_running_count` -- Number of running containers.
* `containers_stopped_count` -- Number of stopped containers.
* `<container-name>/RSS` -- Resident Set Size memory.
* `<container-name>/cache` -- Memory used for caching.
* `<container-name>/swap` -- Swapped memory.
* `<container-name>/pagein_count` -- Number of page faults that bring a
  page into memory.
* `<container-name>/pageout_count` -- Number of page faults that push a
  page out of memory.


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>byte_unit</td><td>byte</td><td>Default numeric output(s)</td><td>str</td></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>measure_collector_time</td><td>False</td><td>Collect the collector run time in ms</td><td>bool</td></tr>
<tr><td>memory_path</td><td>/sys/fs/cgroup/memory</td><td>The path to the kernel's CGroups memoryfilesystem. The auto-detected default is probably correct.</td><td>str</td></tr>
<tr><td>metrics_blacklist</td><td>None</td><td>Regex to match metrics to block. Mutually exclusive with metrics_whitelist</td><td>NoneType</td></tr>
<tr><td>metrics_whitelist</td><td>None</td><td>Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist</td><td>NoneType</td></tr>
</table>

#### Example Output

```
__EXAMPLESHERE__
```

### This file was generated from the python source
### Please edit the source to make changes

