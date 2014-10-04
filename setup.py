#!/usr/bin/env python
# coding=utf-8

import sys
import os
from glob import glob
import platform


def running_under_virtualenv():
    if hasattr(sys, 'real_prefix'):
        return True
    elif sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return True
    if os.getenv('VIRTUAL_ENV', False):
        return True
    return False


if os.environ.get('USE_SETUPTOOLS'):
    from setuptools import setup
    setup_kwargs = dict(zip_safe=0)
else:
    from distutils.core import setup
    setup_kwargs = dict()

if os.name == 'nt':
    pgm_files = os.environ["ProgramFiles"]
    base_files = os.path.join(pgm_files, 'diamond')
    data_files = [
        (base_files, ['LICENSE', 'README.md', 'version.txt']),
        (os.path.join(base_files, 'user_scripts'), []),
        (os.path.join(base_files, 'conf'), glob('conf/*.conf.*')),
        (os.path.join(base_files, 'collectors'), glob('conf/collectors/*')),
        (os.path.join(base_files, 'handlers'), glob('conf/handlers/*')),
    ]
    install_requires = ['ConfigObj', 'psutil', ],

else:
    data_files = [
        ('share/diamond', ['LICENSE', 'README.md', 'version.txt']),
        ('share/diamond/user_scripts', []),
    ]

    distro = platform.dist()[0]
    distro_major_version = platform.dist()[1].split('.')[0]

    if running_under_virtualenv():
        data_files.append(('etc/diamond',
                           glob('conf/*.conf.*')))
        data_files.append(('etc/diamond/collectors',
                           glob('conf/collectors/*')))
        data_files.append(('etc/diamond/handlers',
                           glob('conf/handlers/*')))
    else:
        data_files.append(('/etc/diamond',
                           glob('conf/*.conf.*')))
        data_files.append(('/etc/diamond/collectors',
                           glob('conf/collectors/*')))
        data_files.append(('/etc/diamond/handlers',
                           glob('conf/handlers/*')))

        if distro == 'Ubuntu':
            data_files.append(('/etc/init',
                               ['debian/upstart/diamond.conf']))
        if distro in ['centos', 'redhat', 'debian', 'fedora']:
            data_files.append(('/etc/init.d',
                               ['bin/init.d/diamond']))
            data_files.append(('/var/log/diamond',
                               ['.keep']))
            if distro_major_version >= '7' and not distro == 'debian':
                data_files.append(('/usr/lib/systemd/system',
                                   ['rpm/systemd/diamond.service']))
            elif distro_major_version >= '6' and not distro == 'debian':
                data_files.append(('/etc/init',
                                   ['rpm/upstart/diamond.conf']))

    # Support packages being called differently on different distros

    # Are we in a virtenv?
    if running_under_virtualenv():
        install_requires = ['ConfigObj', 'psutil', ]
    else:
        if distro == ['debian', 'ubuntu']:
            install_requires = ['python-configobj', 'python-psutil', ]
        # Default back to pip style requires
        else:
            install_requires = ['ConfigObj', 'psutil', ]


def get_version():
    """
        Read the version.txt file to get the new version string
        Generate it if version.txt is not available. Generation
        is required for pip installs
    """
    try:
        f = open('version.txt')
    except IOError:
        os.system("./version.sh > version.txt")
        f = open('version.txt')
    version = ''.join(f.readlines()).rstrip()
    f.close()
    return version


def pkgPath(root, path, rpath="/"):
    """
        Package up a path recursively
    """
    global data_files
    if not os.path.exists(path):
        return
    files = []
    for spath in os.listdir(path):
        if spath == 'test':
            # ignore test directories
            continue
        subpath = os.path.join(path, spath)
        spath = os.path.join(rpath, spath)
        if os.path.isfile(subpath):
            files.append(subpath)
        if os.path.isdir(subpath):
            pkgPath(root, subpath, spath)
    data_files.append((root + rpath, files))

if os.name == 'nt':
    pkgPath(os.path.join(base_files, 'collectors'), 'src/collectors', '\\')
else:
    pkgPath('share/diamond/collectors', 'src/collectors')

version = get_version()

setup(
    name='diamond',
    version=version,
    url='https://github.com/BrightcoveOS/Diamond',
    author='The Diamond Team',
    author_email='https://github.com/BrightcoveOS/Diamond',
    license='MIT License',
    description='Smart data producer for graphite graphing package',
    package_dir={'': 'src'},
    packages=['diamond', 'diamond.handler'],
    scripts=['bin/diamond', 'bin/diamond-setup'],
    data_files=data_files,
    install_requires=install_requires,
    #test_suite='test.main',
    ** setup_kwargs
)
