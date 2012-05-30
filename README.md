About
=====

Diamond is a python daemon that collects system metrics and publishes them to Graphite. It is
capable of collecting cpu, memory, network, i/o, load and disk metrics on Linux.  Additionally,
it features an API for implementing custom collectors for gathering metrics from almost any source.

The documentation can be found on our [wiki](https://github.com/BrightcoveOS/Diamond/wiki). For your
convenience the wiki is setup as a submodule of this checkout. You can get it via running

    git submodule init
    git submodule update
