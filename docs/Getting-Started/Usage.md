Usage
=====

To install diamond:

    make install

To unit test diamond:

    make test

For testing, diamond can also be started directly in debug mode without installing:

    cp conf/diamond.conf.example conf/diamond.conf
    edit conf/diamond.conf
    make run

Make can also build packages for CentOS/RHEL, Ubuntu/Debian, or generate a tar ball.

    make buildrpm
    sudo yum localinstall --nogpgcheck dist/diamond-3.0.2-1.noarch.rpm

    make builddeb
    sudo dpkg -i dist/diamond-3.0.2-1.deb

    make tar
    tar -xzvf dist/diamond-3.0.2.tar.gz
