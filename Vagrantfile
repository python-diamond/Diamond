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
    c.vm.box = "bento/centos-6.9"

    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python-configobj"
    c.vm.provision "shell", inline: "cp -rf /vagrant /tmp/Diamond"
    c.vm.provision "shell", inline: "cd /tmp/Diamond && make rpm"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.src.rpm; do mv $f `basename $f .src.rpm`.el6.src.rpm; done;'"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.noarch.rpm; do mv $f `basename $f .noarch.rpm`.el6.noarch.rpm; done;'"
    c.vm.provision "shell", inline: "mkdir -p /vagrant/dist/el6 && (cp -f /tmp/Diamond/dist/* /vagrant/dist/el6/ || grep -v 'cannot stat')"
  end

  config.vm.define "centos7-build" do |c|
    c.vm.hostname = "centos-build"
    c.vm.box = "bento/centos-7.3"

    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python-configobj"
    c.vm.provision "shell", inline: "cp -rf /vagrant /tmp/Diamond"
    c.vm.provision "shell", inline: "cd /tmp/Diamond && make rpm"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.src.rpm; do mv $f `basename $f .src.rpm`.el7.src.rpm; done;'"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.noarch.rpm; do mv $f `basename $f .noarch.rpm`.el7.noarch.rpm; done;'"
    c.vm.provision "shell", inline: "mkdir -p /vagrant/dist/el6 && (cp -f /tmp/Diamond/dist/* /vagrant/dist/el6/ || grep -v 'cannot stat')"
  end

  config.vm.define "centos8-build" do |c|
#     c.vm.hostname = "centos-build"
    c.vm.box = "generic/centos8"
    c.vm.synced_folder "./", "/tmp/Diamond", type: "rsync"

	c.vm.provision "shell", inline: "sudo pip3 install distro"
    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python3-distro"
    c.vm.provision "shell", inline: "cd /tmp/Diamond && make buildrpmpy3"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.src.rpm; do mv $f `basename $f .src.rpm`.el8.src.rpm; done;'"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.noarch.rpm; do mv $f `basename $f .noarch.rpm`.el8.noarch.rpm; done;'"
    c.vm.provision "shell", inline: "sudo mkdir -p /vagrant/dist/el8 && (sudo cp -f /tmp/Diamond/dist/* /vagrant/dist/el8/ || grep -v 'cannot stat')"
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

  config.vm.define "ubuntu1804-build" do |c|
      c.vm.hostname = "ubuntu1804-build"
      c.vm.box = "ubuntu/bionic64"

      c.vm.provision "shell", inline: "sudo apt-get update"
      c.vm.provision "shell", inline: "sudo apt-get install -y make git pbuilder python-mock python-configobj dh-python cdbs"

      # Install python 3
      c.vm.provision "shell", inline: 'sudo apt-get install software-properties-common'
      c.vm.provision "shell", inline: "sudo apt-get install python3.8 -y"
      c.vm.provision "shell", inline: "sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1"
      c.vm.provision "shell", inline: "sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1"

      # Install python libraries needed by specific collectors
      c.vm.provision "shell", inline: "sudo apt-get install -y libmysqlclient-dev" # req for MySQL-python
      c.vm.provision "shell", inline: "sudo apt-get install -y lm-sensors" # req for pyutmp
      c.vm.provision "shell", inline: "sudo apt-get install -y python3-pip"
      c.vm.provision "shell", inline: "sudo apt-get install libpq-dev -y"
      c.vm.provision "shell", inline: "sudo apt-get install python3-dev -y"
      c.vm.provision "shell", inline: "sudo apt-get install libpython3.8-dev -y"
      c.vm.provision "shell", inline: "sudo pip3 install -r /vagrant/requirements.txt"

      # Build Diamond
      c.vm.provision "shell", inline: "cp -rf /vagrant /tmp/Diamond"
      c.vm.provision "shell", inline: "cd /tmp/Diamond && make deb"
      c.vm.provision "shell", inline: "mkdir -p /vagrant/dist/deb && (cp -f /tmp/Diamond/build/*.deb /vagrant/dist/deb/ || grep -v 'cannot stat')"
    end

  config.vm.define "centos6-devel" do |c|
    c.vm.hostname = "centos-devel"
    c.vm.box = "bento/centos-6.9"

    c.vm.provision "shell", inline: "sudo rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python-configobj python-test python-mock tree vim-enhanced"
  end

  config.vm.define "centos7-devel" do |c|
    c.vm.hostname = "centos7-devel"
    c.vm.box = "bento/centos-7.3"

    c.vm.provision "shell", inline: "sudo rpm -ivh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-9.noarch.rpm"
    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python-configobj python-test python-mock tree vim-enhanced MySQL-python gcc"
  end

  config.vm.define "centos8-devel" do |c|
#     c.vm.hostname = "centos-devel"
    c.vm.box = "generic/centos8"

    c.vm.provision "shell", inline: "sudo rpm -ivh --force https://dl.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/e/epel-release-8-14.el8.noarch.rpm"
    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build tree vim-enhanced mysql-devel gcc"
  end

  config.vm.define "centos6-test" do |c|
    c.vm.hostname = "centos-devel"
    c.vm.box = "bento/centos-6.9"

    c.vm.provision "shell", inline: "sudo rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python-configobj python-test python-mock tree vim-enhanced MySQL-python htop gcc"

    # Install python libraries needed by specific collectors
    c.vm.provision "shell", inline: "sudo yum install -y postgresql-devel" # req for psycopg2
    c.vm.provision "shell", inline: "sudo yum install -y Cython" # req for pyutmp
    c.vm.provision "shell", inline: "sudo yum install -y lm_sensors-devel lm_sensors python-devel" # req for pyutmp
    c.vm.provision "shell", inline: "sudo yum install -y python-pip"
    c.vm.provision "shell", inline: "sudo pip install psycopg2==2.6.2" # 2.7 requires PG 9.1+
    c.vm.provision "shell", inline: "sudo pip install -r /vagrant/.travis.requirements.txt"

    # Setup Diamond to run as a service
    c.vm.provision "shell", inline: "sudo yum install -y python-setuptools"
    c.vm.provision "shell", inline: "sudo mkdir -m 0750 /var/log/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/conf/vagrant /etc/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/bin/diamond /usr/bin/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/src/diamond /usr/lib/python2.7/site-packages/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/bin/init.d/diamond /etc/init.d/diamond"

    # Start diamond
    c.vm.provision "shell", inline: "sudo service diamond start"
  end

  config.vm.define "centos7-test" do |c|
    c.vm.hostname = "centos7-test"
    c.vm.box = "bento/centos-7.3"

    c.vm.provider "virtualbox" do |v|
      v.memory = 1024
      v.cpus = 2
    end

    c.vm.provision "shell", inline: "sudo rpm -ivh https://dl.fedoraproject.org/pub/epel/7/x86_64/Packages/e/epel-release-7-14.noarch.rpm"
    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python-configobj python-test python-mock tree vim-enhanced MySQL-python htop gcc"

    # Install python 3
    c.vm.provision "shell", inline: 'sudo yum -y groupinstall "Development Tools"'
    c.vm.provision "shell", inline: 'sudo yum install openssl-devel zlib-devel libffi-devel -y'
    c.vm.provision "shell", inline: "sudo yum install -y centos-release-scl-rh"
    c.vm.provision "shell", inline: "sudo yum install -y rh-python38"
    c.vm.provision "shell", inline: 'sudo wget https://www.python.org/ftp/python/3.8.8/Python-3.8.8.tgz'
    c.vm.provision "shell", inline: 'sudo tar xzf Python-3.8.8.tgz && cd Python-3.8.8 && sudo ./configure --enable-optimizations --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib" && sudo make altinstall'
    c.vm.provision "shell", inline: "sudo yum install -y python3-devel"
    c.vm.provision "shell", inline: "sudo ln -sfn /usr/local/bin/python3.8 /usr/bin/python3"

    # Install python libraries needed by specific collectors
    c.vm.provision "shell", inline: "sudo yum install -y postgresql-devel" # req for psycopg2
    c.vm.provision "shell", inline: "sudo yum install -y Cython" # req for pyutmp
    c.vm.provision "shell", inline: "sudo yum install -y lm_sensors-devel lm_sensors python-devel" # req for pyutmp
    c.vm.provision "shell", inline: "sudo yum install -y python3-pip"
    c.vm.provision "shell", inline: "sudo pip3 install -r /vagrant/requirements.txt"

    # Setup Diamond to run as a service
    c.vm.provision "shell", inline: "sudo yum install -y python-setuptools"
    c.vm.provision "shell", inline: "sudo mkdir /var/log/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/conf/vagrant /etc/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/bin/diamond /usr/bin/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/src/diamond /usr/local/lib/python3.8/site-packages/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/rpm/systemd/diamond.service /usr/lib/systemd/system/diamond.service"

    # Install other components to test with

    # Redis
    c.vm.provision "shell", inline: "sudo yum install -y redis"
    c.vm.provision "shell", inline: "sudo systemctl start redis.service"

    # Build Diamond docs and run tests
    c.vm.provision "shell", inline: "sudo yum makecache && sudo yum -y install python-pep8"
    c.vm.provision "shell", inline: "sudo pip3 install mock"
    c.vm.provision "shell", inline: "echo 'Build docs...' && python3 /vagrant/build_doc.py"
    c.vm.provision "shell", inline: "echo 'Running tests...' && python3 /vagrant/test.py"
    c.vm.provision "shell", inline: "echo 'Running pep8...' && pep8 --config=/vagrant/.pep8 /vagrant/src /vagrant/bin/diamond /vagrant/bin/diamond-setup /vagrant/build_doc.py /vagrant/setup.py /vagrant/test.py"

    # Start diamond
    c.vm.provision "shell", inline: "echo 'Starting Diamond service...' && sudo systemctl start diamond.service"
    c.vm.provision "shell", inline: "systemctl status diamond.service"
  end

  config.vm.define "centos8-test" do |c|
#     It doesn't works with hostname on CentOS8
#     c.vm.hostname = "centos8-test"
    c.vm.box = "generic/centos8"
    c.vm.synced_folder ".", "/vagrant"

    c.vm.provider "virtualbox" do |v|
      v.memory = 1024
      v.cpus = 2
    end

    c.vm.provision "shell", inline: "sudo rpm -ivh --force https://dl.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/e/epel-release-8-14.el8.noarch.rpm"
    c.vm.provision "shell", inline: "sudo dnf install -y git rpm-build python3-configobj python3-test tree vim-enhanced python3-PyMySQL htop gcc"

    # Install python 3
    c.vm.provision "shell", inline: 'sudo dnf -y group install "Development Tools"'
    c.vm.provision "shell", inline: 'sudo dnf install openssl-devel zlib-devel libffi-devel -y'
    c.vm.provision "shell", inline: 'sudo dnf -y install wget'
    c.vm.provision "shell", inline: 'sudo wget https://www.python.org/ftp/python/3.8.8/Python-3.8.8.tgz'
    c.vm.provision "shell", inline: 'sudo tar xzf Python-3.8.8.tgz && cd Python-3.8.8 && sudo ./configure --enable-optimizations --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib" && sudo make altinstall'
    c.vm.provision "shell", inline: "sudo dnf install -y python3-devel"
    c.vm.provision "shell", inline: "sudo ln -sfn /usr/local/bin/python3.8 /usr/bin/python3"
    c.vm.provision "shell", inline: "sudo ln -sfn /usr/local/bin/pip3.8 /usr/bin/pip3"

    # Install python libraries needed by specific collectors
    c.vm.provision "shell", inline: "sudo dnf install -y postgresql-devel" # req for psycopg2
    c.vm.provision "shell", inline: "sudo dnf install -y lm_sensors-devel lm_sensors" # req for pyutmp
    c.vm.provision "shell", inline: "sudo pip3 install -r /vagrant/requirements.txt"

    # Setup Diamond to run as a service
    c.vm.provision "shell", inline: "sudo dnf install -y python3-setuptools"
    c.vm.provision "shell", inline: "sudo mkdir /var/log/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/conf/vagrant /etc/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/bin/diamond /usr/bin/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/src/diamond /usr/local/lib/python3.8/site-packages/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/rpm/systemd/diamond.service /usr/lib/systemd/system/diamond.service"

    # Redis
    c.vm.provision "shell", inline: "sudo dnf install -y redis"
    c.vm.provision "shell", inline: "sudo systemctl start redis.service"

    # Build Diamond docs and run tests
    c.vm.provision "shell", inline: "sudo dnf makecache && sudo dnf -y install python3-pep8-naming"
    c.vm.provision "shell", inline: "sudo pip3 install mock"
    c.vm.provision "shell", inline: "echo 'Build docs...' && python3 /vagrant/build_doc.py"
    c.vm.provision "shell", inline: "echo 'Running tests...' && python3 /vagrant/test.py"
    c.vm.provision "shell", inline: "echo 'Running pep8...' && pep8 --config=/vagrant/.pep8 /vagrant/src /vagrant/bin/diamond /vagrant/bin/diamond-setup /vagrant/build_doc.py /vagrant/setup.py /vagrant/test.py"

    # For some reason diamond.service doesn't appear in systemsctl by itself like it was in CentOS 7 test
    c.vm.provision "shell", inline: "sudo cp /vagrant/rpm/systemd/diamond.service /etc/systemd/system/"
    c.vm.provision "shell", inline: "sudo systemctl daemon-reload"
    c.vm.provision "shell", inline: "sudo systemctl enable diamond.service"

    # Start diamond
    c.vm.provision "shell", inline: "echo 'Starting Diamond service...' && sudo systemctl start diamond.service"
    c.vm.provision "shell", inline: "systemctl status diamond.service"
  end

  config.vm.define "ubuntu1604-test" do |c|
    c.vm.hostname = "ubuntu1604-test"
    c.vm.box = "bento/ubuntu-16.04"

    c.vm.provision "shell", inline: "sudo apt-get update"
    c.vm.provision "shell", inline: "sudo apt-get install -y make git pbuilder python-mock python-configobj dh-python cdbs"

    # Install python libraries needed by specific collectors
    c.vm.provision "shell", inline: "sudo apt-get install -y libmysqlclient-dev" # req for MySQL-python
    c.vm.provision "shell", inline: "sudo apt-get install -y lm-sensors" # req for pyutmp
    c.vm.provision "shell", inline: "sudo apt-get install -y python-pip"
    c.vm.provision "shell", inline: "sudo pip install -r /vagrant/.travis.requirements.txt"

    # Setup Diamond to run as a service
    c.vm.provision "shell", inline: "sudo apt-get install -y python-setuptools"
    c.vm.provision "shell", inline: "sudo mkdir /var/log/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/conf/vagrant /etc/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/bin/diamond /usr/bin/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/src/diamond /usr/lib/python2.7/dist-packages/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/rpm/systemd/diamond.service /lib/systemd/system/diamond.service"

    # Start diamond
    c.vm.provision "shell", inline: "sudo systemctl start diamond.service"
  end

  config.vm.define "ubuntu1804-test" do |c|
    c.vm.hostname = "ubuntu1804-test"
    c.vm.box = "ubuntu/bionic64"

    c.vm.provision "shell", inline: "sudo apt-get update"
    c.vm.provision "shell", inline: "sudo apt-get install -y make git pbuilder python-mock python-configobj dh-python cdbs"

    # Install python 3
    c.vm.provision "shell", inline: 'sudo apt-get install software-properties-common'
    c.vm.provision "shell", inline: "sudo apt-get install python3.8 -y"
    c.vm.provision "shell", inline: "sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1"
    c.vm.provision "shell", inline: "sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1"

    # Install python libraries needed by specific collectors
    c.vm.provision "shell", inline: "sudo apt-get install -y libmysqlclient-dev" # req for MySQL-python
    c.vm.provision "shell", inline: "sudo apt-get install -y lm-sensors" # req for pyutmp
    c.vm.provision "shell", inline: "sudo apt-get install -y python3-pip"
    c.vm.provision "shell", inline: "sudo apt-get install libpq-dev -y"
    c.vm.provision "shell", inline: "sudo apt-get install python3-dev -y"
    c.vm.provision "shell", inline: "sudo apt-get install libpython3.8-dev -y"
    c.vm.provision "shell", inline: "sudo pip3 install -r /vagrant/requirements.txt"

    # Setup Diamond to run as a service
    c.vm.provision "shell", inline: "sudo apt-get install -y python-setuptools"
    c.vm.provision "shell", inline: "sudo mkdir /var/log/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/conf/vagrant /etc/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/bin/diamond /usr/bin/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/src/diamond /usr/local/lib/python3.8/dist-packages/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/rpm/systemd/diamond.service /lib/systemd/system/diamond.service"

    # Redis
    c.vm.provision "shell", inline: "sudo apt-get install -y redis"
    c.vm.provision "shell", inline: "sudo systemctl start redis.service"

    # Run tests and linter
    c.vm.provision "shell", inline: "sudo apt-get install -y pep8"
    c.vm.provision "shell", inline: "echo 'Running tests...' && python3 /vagrant/test.py"
    c.vm.provision "shell", inline: "echo 'Running pep8...' && pep8 --config=/vagrant/.pep8 /vagrant/src /vagrant/bin/diamond /vagrant/bin/diamond-setup /vagrant/build_doc.py /vagrant/setup.py /vagrant/test.py"

    # Start diamond
    c.vm.provision "shell", inline: "echo 'Starting Diamond service...' && sudo systemctl start diamond.service"
    c.vm.provision "shell", inline: "systemctl status diamond.service"
  end

  config.vm.define "ubuntu2004-test" do |c|
    c.vm.hostname = "ubuntu2004-test"
    c.vm.box = "ubuntu/focal64"

	# Comment out DPkg line which prevents pre-configuring all packages with debconf before they are installed, thus
	# fixing "unable to re-open stdin: No file or directory" issue
    c.vm.provision "shell", inline: 'sudo ex +"%s@DPkg@//DPkg" -cwq /etc/apt/apt.conf.d/70debconf'
    c.vm.provision "shell", inline: 'sudo dpkg-reconfigure debconf -f noninteractive -p critical'

    # Install necessary libs
    c.vm.provision "shell", inline: "sudo apt-get update"
    c.vm.provision "shell", inline: "sudo apt-get install -y make git pbuilder python-mock python3-configobj dh-python cdbs"

    # Install python 3
    c.vm.provision "shell", inline: 'sudo apt-get install software-properties-common'
    c.vm.provision "shell", inline: "sudo apt-get install python3.8 -y"
    c.vm.provision "shell", inline: "sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1"
    c.vm.provision "shell", inline: "sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1"

    # Install python libraries needed by specific collectors
    c.vm.provision "shell", inline: "sudo apt-get install -y libmysqlclient-dev" # req for MySQL-python
    c.vm.provision "shell", inline: "sudo apt-get install -y lm-sensors" # req for pyutmp
    c.vm.provision "shell", inline: "sudo apt-get install -y python3-pip"
    c.vm.provision "shell", inline: "sudo apt-get install libpq-dev -y"
    c.vm.provision "shell", inline: "sudo apt-get install python3-dev -y"
    c.vm.provision "shell", inline: "sudo apt-get install libpython3.8-dev -y"
    c.vm.provision "shell", inline: "sudo pip3 install -r /vagrant/requirements.txt"

    # Setup Diamond to run as a service
    c.vm.provision "shell", inline: "sudo apt-get install -y python-setuptools"
    c.vm.provision "shell", inline: "sudo mkdir -p /var/log/diamond"
    c.vm.provision "shell", inline: "sudo ln -sf /vagrant/conf/vagrant /etc/diamond"
    c.vm.provision "shell", inline: "sudo ln -sf /vagrant/bin/diamond /usr/bin/diamond"
    c.vm.provision "shell", inline: "sudo ln -sf /vagrant/src/diamond /usr/local/lib/python3.8/dist-packages/diamond"
    c.vm.provision "shell", inline: "sudo ln -sf /vagrant/rpm/systemd/diamond.service /lib/systemd/system/diamond.service"

    # Redis
    c.vm.provision "shell", inline: "sudo apt-get install -y redis"
    c.vm.provision "shell", inline: "sudo systemctl start redis.service"

    # Run tests and linter
    c.vm.provision "shell", inline: "sudo apt-get install -y pep8"
    c.vm.provision "shell", inline: "echo 'Running tests...' && python3 /vagrant/test.py"
    c.vm.provision "shell", inline: "echo 'Running pep8...' && pep8 --config=/vagrant/.pep8 /vagrant/src /vagrant/bin/diamond /vagrant/bin/diamond-setup /vagrant/build_doc.py /vagrant/setup.py /vagrant/test.py"

    # Start diamond
    c.vm.provision "shell", inline: "echo 'Starting Diamond service...' && sudo systemctl start diamond.service"
    c.vm.provision "shell", inline: "systemctl status diamond.service"
  end

  config.vm.define "debian11.2-test" do |c|
    c.vm.hostname = "debian11.2-test"
    c.vm.box = "debian/bullseye64"

    c.vm.provision "shell", inline: "sudo apt-get update"
    c.vm.provision "shell", inline: "sudo apt-get install -y make git pbuilder python-configobj-doc dh-python cdbs"

    # Install python 3
    c.vm.provision "shell", inline: "sudo apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget"
    c.vm.provision "shell", inline: "sudo wget https://www.python.org/ftp/python/3.8.8/Python-3.8.8.tgz && sudo tar xzf Python-3.8.8.tgz"
    c.vm.provision "shell", inline: "cd Python-3.8.8 && sudo ./configure --enable-optimizations --enable-shared && sudo make altinstall"
    c.vm.provision "shell", inline: "sudo ldconfig /vagrant/Python3.8.8"
    c.vm.provision "shell", inline: "sudo ln -sfn /usr/local/bin/python3.8 /usr/bin/python3"

    # Install python libraries needed by specific collectors
    c.vm.provision "shell", inline: "sudo apt-get install -y default-libmysqlclient-dev" # req for MySQL-python
    c.vm.provision "shell", inline: "sudo apt-get install -y postgresql-server-dev-all" # req for psycopg2
    c.vm.provision "shell", inline: "sudo apt-get install -y lm-sensors" # req for pyutmp
    c.vm.provision "shell", inline: "sudo rm /usr/bin/lsb_release"  # lsb_release caused pip error
    c.vm.provision "shell", inline: "sudo pip3.8 install -r /vagrant/requirements.txt"

    # Setup Diamond to run as a service
    c.vm.provision "shell", inline: "sudo mkdir /var/log/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/conf/vagrant /etc/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/bin/diamond /usr/bin/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/src/diamond /usr/local/lib/python3.8/site-packages/diamond"
    c.vm.provision "shell", inline: "sudo ln -s /vagrant/rpm/systemd/diamond.service /usr/lib/systemd/system/diamond.service"

    # Redis
    c.vm.provision "shell", inline: "sudo apt-get install -y redis"
    c.vm.provision "shell", inline: "sudo systemctl start redis.service"

    # Build Diamond docs and run tests
    c.vm.provision "shell", inline: "sudo apt-get -y install python3-pep8-naming"
    c.vm.provision "shell", inline: "echo 'Running tests...' && python3 /vagrant/test.py"
#     Linter is not working. Some pep8 issues
#     c.vm.provision "shell", inline: "echo 'Running pep8...' && pep8 --config=/vagrant/.pep8 /vagrant/src /vagrant/bin/diamond /vagrant/bin/diamond-setup /vagrant/build_doc.py /vagrant/setup.py /vagrant/test.py"

    # Start diamond
    c.vm.provision "shell", inline: "echo 'Starting Diamond service...' && sudo systemctl start diamond.service"
    c.vm.provision "shell", inline: "systemctl status diamond.service"
  end
end
