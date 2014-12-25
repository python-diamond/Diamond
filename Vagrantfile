# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  
  config.vm.define "centos5-build" do |c|
    c.vm.hostname = "centos-build"
    c.vm.box = "opscode_centos-5.10"
    c.vm.box_url = "http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_centos-5.10_chef-provisionerless.box"
  
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
    c.vm.box = "opscode_centos-6.5"
    c.vm.box_url = "http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_centos-6.5_chef-provisionerless.box"
  
    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python-configobj"
    c.vm.provision "shell", inline: "cp -rf /vagrant /tmp/Diamond"  
    c.vm.provision "shell", inline: "cd /tmp/Diamond && make rpm"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.src.rpm; do mv $f `basename $f .src.rpm`.el6.src.rpm; done;'"
    c.vm.provision "shell", inline: "cd /tmp/Diamond/dist && sudo bash -c 'for f in *.noarch.rpm; do mv $f `basename $f .noarch.rpm`.el6.noarch.rpm; done;'"
    c.vm.provision "shell", inline: "mkdir -p /vagrant/dist/el6 && (cp -f /tmp/Diamond/dist/* /vagrant/dist/el6/ || grep -v 'cannot stat')"
  end

  config.vm.define "ubuntu-build" do |c|
    c.vm.hostname = "ubuntu-build"
    c.vm.box = "opscode_ubuntu-12.04"
    c.vm.box_url = "http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_ubuntu-12.04_chef-provisionerless.box"
  
    c.vm.provision "shell", inline: "sudo apt-get update"  
    c.vm.provision "shell", inline: "sudo apt-get install -y make git pbuilder python-mock python-configobj python-support cdbs"
    c.vm.provision "shell", inline: "cp -rf /vagrant /tmp/Diamond"  
    c.vm.provision "shell", inline: "cd /tmp/Diamond && make deb"
    c.vm.provision "shell", inline: "mkdir -p /vagrant/dist/deb && (cp -f /tmp/Diamond/build/*.deb /vagrant/dist/deb/ || grep -v 'cannot stat')"
  end

  config.vm.define "centos6-devel" do |c|
    c.vm.hostname = "centos-devel"
    c.vm.box = "opscode_centos-6.5"
    c.vm.box_url = "http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_centos-6.5_chef-provisionerless.box"

    c.vm.provision "shell", inline: "sudo rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
    c.vm.provision "shell", inline: "sudo yum install -y git rpm-build python-configobj python-test python-mock tree vim-enhanced"
  end

end
