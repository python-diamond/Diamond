<!--This file was generated from the python source
Please edit the source to make changes
-->
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


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
measure_collector_time | False | Collect the collector run time in ms | bool
memory_path | /sys/fs/cgroup/memory | The path to the kernel's CGroups memoryfilesystem. The auto-detected default is probably correct. | str
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType

#### Example Output

```
__EXAMPLESHERE__
```

