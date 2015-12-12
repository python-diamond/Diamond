# What is Facet?

Facet is a cross platform abstraction layer providing APIs to collect basic system statistics from multiple platforms. Its designed to be plug-able and easy to add additional statistics and platforms. 

# How does Diamond use Facet?

Facet is designed to be used by the basic system collectors (e.g. cpu, loadavg, memory, etc...) to enable Diamond to collect data from any platform supported by Facet. 

# What platforms are supported by Facet?

Currently Linux and SunOS platforms are supported. 

# What modules are supported by Facet?

- LoadAverageModule
- CPUStatModule
- MemoryStatModule
- DiskSpaceModule
- DiskStatModule

# How do I use Facet?


    import facet
    f = facet.Facet()
    (1m, 5m, 15m, total_proc, running_proc) = f.loadavg.get_load_average()
