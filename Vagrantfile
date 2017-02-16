# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "centos5-build" do |c|
    c.vm.hostname = "centos-build"
    c.vm.box = "bento/centos-5.11"

    c.vm.provision "shell", inline: "rpm -qa | grep -qw epel-release  || (cd /tmp && wget http://dl.fedoraproject.org/pub/epel/5/x86_64/epel-release-5-4.noarch.rpm && sudo rpm -U epel-release-5*.noarch.rpm)"
    c.vm.provision "shell", inline: "rpm -qa | grep -qw 'git\|rpm-build\|python-configobj' || sudo yum install -y git rpm-build python-configobj"
    c.vm.provision "shell", inline: "cp -rf /vagrant /tmp/Diamond"
    c.vm.provision "shell", inline: "cd /tmp/Diamond && make rpm"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.src.rpm; do mv $f `basename $f .src.rpm`.el5.src.rpm; done;'"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.noarch.rpm; do mv $f `basename $f .noarch.rpm`.el5.noarch.rpm; done;'"
    c.vm.provision "shell", inline: "mkdir -p /vagrant/dist/el5 && (cp -f /tmp/Diamond/dist/* /vagrant/dist/el5/ || grep -v 'cannot stat')"
  end

  config.vm.define "centos6-build" do |c|
    c.vm.hostname = "centos-build"
    c.vm.box = "bento/centos-6.8"

    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python-configobj"
    c.vm.provision "shell", inline: "cp -rf /vagrant /tmp/Diamond"
    c.vm.provision "shell", inline: "cd /tmp/Diamond && make rpm"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.src.rpm; do mv $f `basename $f .src.rpm`.el6.src.rpm; done;'"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.noarch.rpm; do mv $f `basename $f .noarch.rpm`.el6.noarch.rpm; done;'"
    c.vm.provision "shell", inline: "mkdir -p /vagrant/dist/el6 && (cp -f /tmp/Diamond/dist/* /vagrant/dist/el6/ || grep -v 'cannot stat')"
  end

  config.vm.define "centos7-build" do |c|
    c.vm.hostname = "centos-build"
    c.vm.box = "bento/centos-7.2"

    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python-configobj"
    c.vm.provision "shell", inline: "cp -rf /vagrant /tmp/Diamond"
    c.vm.provision "shell", inline: "cd /tmp/Diamond && make rpm"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.src.rpm; do mv $f `basename $f .src.rpm`.el7.src.rpm; done;'"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.noarch.rpm; do mv $f `basename $f .noarch.rpm`.el7.noarch.rpm; done;'"
    c.vm.provision "shell", inline: "mkdir -p /vagrant/dist/el6 && (cp -f /tmp/Diamond/dist/* /vagrant/dist/el6/ || grep -v 'cannot stat')"
  end

  config.vm.define "ubuntu-build" do |c|
    c.vm.hostname = "ubuntu-build"
    c.vm.box = "bento/ubuntu-12.04"

    c.vm.provision "shell", inline: "sudo apt-get update"
    c.vm.provision "shell", inline: "sudo apt-get install -y make git pbuilder python-mock python-configobj python-support cdbs"
    c.vm.provision "shell", inline: "cp -rf /vagrant /tmp/Diamond"
    c.vm.provision "shell", inline: "cd /tmp/Diamond && make deb"
    c.vm.provision "shell", inline: "mkdir -p /vagrant/dist/deb && (cp -f /tmp/Diamond/build/*.deb /vagrant/dist/deb/ || grep -v 'cannot stat')"
  end

  config.vm.define "centos6-devel" do |c|
    c.vm.hostname = "centos-devel"
    c.vm.box = "bento/centos-6.8"

    c.vm.provision "shell", inline: "sudo rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python-configobj python-test python-mock tree vim-enhanced"
  end

  config.vm.define "centos7-devel" do |c|
    c.vm.hostname = "centos7-devel"
    c.vm.box = "bento/centos-7.2"

    c.vm.provision "shell", inline: "sudo rpm -ivh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-9.noarch.rpm"
    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python-configobj python-test python-mock tree vim-enhanced MySQL-python gcc"
  end

  config.vm.define "centos7-test" do |c|
    c.vm.hostname = "centos7-test"
    c.vm.box = "bento/centos-7.2"

    c.vm.provider "virtualbox" do |v|
      v.memory = 1024
      v.cpus = 2
    end

    c.vm.provision "shell", inline: "sudo rpm -ivh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-9.noarch.rpm"
    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python-configobj python-test python-mock tree vim-enhanced MySQL-python htop gcc"

    # Install python libraries needed by specific collectors
    c.vm.provision "shell", inline: "sudo yum install -y postgresql-devel" # req for psycopg2
    c.vm.provision "shell", inline: "sudo yum install -y Cython" # req for pyutmp
    c.vm.provision "shell", inline: "sudo yum install -y lm_sensors-devel lm_sensors python-devel" # req for pyutmp
    c.vm.provision "shell", inline: "sudo yum install -y python-pip"
    c.vm.provision "shell", inline: "sudo pip install -r /vagrant/.travis.requirements.txt"

    # Setup Diamond to run as a service
    c.vm.provision "shell", inline: "sudo yum install -y python-setuptools"
    c.vm.provision "shell", inline: "sudo mkdir /var/log/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/conf/vagrant /etc/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/bin/diamond /usr/bin/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/src/diamond /usr/lib/python2.7/site-packages/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/rpm/systemd/diamond.service /usr/lib/systemd/system/diamond.service"

    # Install other components to test with

    ## Redis
    c.vm.provision "shell", inline: "sudo yum install -y redis"
    c.vm.provision "shell", inline: "sudo systemctl start redis.service"

    # Build Diamond docs and run tests
    c.vm.provision "shell", inline: "sudo pip install pep8==1.5.7"
    c.vm.provision "shell", inline: "echo 'Build docs...' && python /vagrant/build_doc.py"
    c.vm.provision "shell", inline: "echo 'Running tests...' && python /vagrant/test.py"
    c.vm.provision "shell", inline: "echo 'Running pep8...' && pep8 --config=/vagrant/.pep8 /vagrant/src /vagrant/bin/diamond /vagrant/bin/diamond-setup /vagrant/build_doc.py /vagrant/setup.py /vagrant/test.py"

    # Start diamond
    c.vm.provision "shell", inline: "sudo systemctl start diamond.service"
  end
end
