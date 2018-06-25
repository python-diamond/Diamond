# Installation

## Dependencies
### Core

- CentOS or Ubuntu
- Python 2.7
- python-configobj
- python-setuptools
- make
- [Python Psutil](http://code.google.com/p/psutil/) for non linux system metrics

### Unit Test

- [Mock 0.8](http://www.voidspace.org.uk/python/mock/)


## Installation From Package
### RHEL / CentOS

```sh
$ yum install make rpm-build python-configobj python-setuptools
$ git clone https://github.com/python-diamond/Diamond
$ cd Diamond
$ make buildrpm
```

Then use the package you built like this:

```sh
$ yum localinstall --nogpgcheck dist/diamond-4.0.449-0.noarch.rpm
$ cp /etc/diamond/{diamond.conf.example,diamond.conf}
$ $EDITOR /etc/diamond/diamond.conf
# Start Diamond service via service manager.
```

### Debian / Ubuntu

```sh
$ apt-get update
$ apt-get install make pbuilder python-mock python-configobj python-support cdbs devscripts build-essential
$ git clone https://github.com/python-diamond/Diamond
$ cd Diamond
$ make builddeb
```

Then use the package you built like this:

```sh
$ dpkg -i dist/diamond_3.5.8_all.deb #(check version number properly)
$ cp /etc/diamond/{diamond.conf.example,diamond.conf}
$ $EDITOR /etc/diamond/diamond.conf
# Start Diamond service via service manager.
```

## Installation From Source

To install diamond:

```sh
$ make install
```

To unit test diamond:

```sh
$ make test
```

For testing, diamond can also be started directly in debug mode without installing:

```sh
$ cp conf/diamond.conf.example conf/diamond.conf
$ $EDITOR conf/diamond.conf
$ make run
```
