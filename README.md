[![Build Status](https://travis-ci.org/python-diamond/Diamond.svg?branch=master)](https://travis-ci.org/python-diamond/Diamond)
About
=====

Diamond is a python daemon that collects system metrics and publishes them to
[Graphite](https://github.com/python-diamond/Diamond/wiki/handler-GraphiteHandler)
(and [others](https://github.com/python-diamond/Diamond/wiki/Handlers)). It is
capable of collecting cpu, memory, network, i/o, load and disk metrics.  Additionally,
it features an API for implementing custom collectors for gathering metrics from almost any source.

The documentation can be found on our [wiki](https://github.com/python-diamond/Diamond/wiki). For your
convenience the wiki is setup as a submodule of this checkout. You can get it via running

    git submodule init
    git submodule update

Getting Started
=====

Steps to getting started:

  * Read the [documentation on the Wiki](https://github.com/python-diamond/Diamond/wiki)
  * Install via "pip install diamond".  The releases on github are not recommended for use.  Use
  "pypi-install diamond" on Debian/Ubuntu systems with python-stdeb installed to build packages.
  * Copy the "diamond.conf.example" file to "diamond.conf".
  * Optional: Run "diamond-setup" to help set collectors in "diamond.conf".
  * Modify "diamond.conf" for your needs.
  * Run diamond with one of: "diamond" or "initctl start diamond" or "/etc/init.d/diamond restart".

Success Stories
=====

 * Diamond has successfully been deployed to a cluster of 1000 machines pushing [3 million points per minute](https://answers.launchpad.net/graphite/+question/178969).
 * Have a story? Please share!

Repos
=====

Historically Diamond was a brightcove project and hosted at [BrightcoveOS](https://github.com/brightcoveos/Diamond).
However none of the active developers are brightcove employees and so the development
has moved to [python-diamond](https://github.com/python-diamond/Diamond). We request
that any new pull requests and issues be cut against python-diamond. We will keep
BrightcoveOS updated and still honor issues/tickets cut on that repo.

Diamond Related Projects
=====
 * [Related Projects](https://github.com/python-diamond/Diamond/wiki/Related-Projects)
 
Contact
=====
 * IRC [#python-diamond](irc://chat.freenode.net:6667/%23python-diamond) on [freenode](http://www.freenode.net). [Webchat](http://webchat.freenode.net/?channels=python-diamond)
 * Mailing List [diamond@librelist.com](mailto:diamond@librelist.com) - Email the list and you will automatically subscribe. [Archive](http://librelist.com/browser/diamond/)
