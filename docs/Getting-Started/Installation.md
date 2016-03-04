Installation
=====

### Installation/Building Dependencies 

- make
- rpm-build

### Core Dependencies

- CentOS or Ubuntu
- Python 2.4+
- python-configobj
- [Python Psutil](http://code.google.com/p/psutil/) for non linux system metrics

### Unit Test Dependencies 

- [Mock 0.8](http://www.voidspace.org.uk/python/mock/)


Debian Squeeze / Ubuntu Precise
====

```sh
$ sudo apt-get update
$ sudo apt-get install make pbuilder python-mock python-configobj python-support cdbs devscripts build-essential
$ git clone https://github.com/python-diamond/Diamond
$ cd Diamond
$ make builddeb
$ sudo dpkg -i build/diamond_3.5.8_all.deb #(check version number properly)
$ sudo cp /etc/diamond/diamond.conf.example /etc/diamond/diamond.conf
$ edit /etc/diamond/diamond.conf
$ sudo /etc/init.d/diamond start or sudo service diamond start/stop
```