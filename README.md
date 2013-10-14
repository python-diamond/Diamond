About
=====

Diamond is a python daemon that collects system metrics and publishes them to
[Graphite](https://github.com/BrightcoveOS/Diamond/wiki/handler-GraphiteHandler)
(and [others](https://github.com/BrightcoveOS/Diamond/wiki/Handlers)). It is
capable of collecting cpu, memory, network, i/o, load and disk metrics.  Additionally,
it features an API for implementing custom collectors for gathering metrics from almost any source.

The documentation can be found on our [wiki](https://github.com/BrightcoveOS/Diamond/wiki). For your
convenience the wiki is setup as a submodule of this checkout. You can get it via running

    git submodule init
    git submodule update

Success Stories
=====

 * Diamond has successfully been deployed to a cluster of 1000 machines pushing [3 million points per minute](https://answers.launchpad.net/graphite/+question/178969).
 * Have a story? Please share!

Diamond Related Projects
=====
 * [Related Projects](https://github.com/BrightcoveOS/Diamond/wiki/Related-Projects)
 
Contact
=====
 * IRC [#python-diamond](irc://chat.freenode.net:6667/%23python-diamond) on [freenode](http://www.freenode.net). [Webchat](http://webchat.freenode.net/?channels=python-diamond)


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/BrightcoveOS/diamond/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

