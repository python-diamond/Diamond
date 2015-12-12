<!--This file was generated from the python source
Please edit the source to make changes
-->
DropwizardCollector
=====

Collect [dropwizard](http://dropwizard.codahale.com/) stats for the local node


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
byte_unit | byte | Default numeric output(s) | str
enabled | False | Enable collecting these metrics | bool
host | 127.0.0.1 |  | str
measure_collector_time | False | Collect the collector run time in ms | bool
metrics_blacklist | None | Regex to match metrics to block. Mutually exclusive with metrics_whitelist | NoneType
metrics_whitelist | None | Regex to match metrics to transmit. Mutually exclusive with metrics_blacklist | NoneType
port | 8081 |  | int

#### Example Output

```
servers.hostname.dropwizard.jvm.daemon_thread_count 10
servers.hostname.dropwizard.jvm.fd_usage 0.014892578125
servers.hostname.dropwizard.jvm.memory.code_cache 0.0382893880208
servers.hostname.dropwizard.jvm.memory.eden_space 0.191892438356
servers.hostname.dropwizard.jvm.memory.heapCommitted 115539968.0
servers.hostname.dropwizard.jvm.memory.heapInit 67108864.0
servers.hostname.dropwizard.jvm.memory.heapMax 954466304.0
servers.hostname.dropwizard.jvm.memory.heapUsed 83715232.0
servers.hostname.dropwizard.jvm.memory.heap_usage 0.0877089444113
servers.hostname.dropwizard.jvm.memory.non_heap_usage 0.249035531824
servers.hostname.dropwizard.jvm.memory.old_gen 0.0221274596894
servers.hostname.dropwizard.jvm.memory.perm_gen 0.328065335751
servers.hostname.dropwizard.jvm.memory.survivor_space 1.0
servers.hostname.dropwizard.jvm.memory.totalCommitted 162267136.0
servers.hostname.dropwizard.jvm.memory.totalInit 91422720.0
servers.hostname.dropwizard.jvm.memory.totalMax 1139015680.0
servers.hostname.dropwizard.jvm.memory.totalUsed 129674584.0
servers.hostname.dropwizard.jvm.thread_count 27
servers.hostname.dropwizard.jvm.thread_states.blocked 0.0
servers.hostname.dropwizard.jvm.thread_states.new 0.0
servers.hostname.dropwizard.jvm.thread_states.runnable 0.0
servers.hostname.dropwizard.jvm.thread_states.terminated 0.0
servers.hostname.dropwizard.jvm.thread_states.timed_waiting 0.518518518519
servers.hostname.dropwizard.jvm.thread_states.waiting 0.222222222222
```

