#!/usr/bin/env python

import os
from glob import glob
import platform

if os.environ.get('USE_SETUPTOOLS'):
    from setuptools import setup
    setup_kwargs = dict(zip_safe=0)
else:
    from distutils.core import setup
    setup_kwargs = dict()

data_files = [
    ('share/diamond', ['LICENSE', 'README.md', 'version.txt']),
    ('share/diamond/user_scripts', []),
]

if os.getenv('VIRTUAL_ENV', False):
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

    if platform.dist()[0] == 'Ubuntu':
        data_files.append(('/etc/init',
                           ['debian/upstart/diamond.conf']))
    if platform.dist()[0] in ['centos', 'redhat']:
        data_files.append(('/etc/init.d',
                           ['bin/init.d/diamond']))
        data_files.append(('/var/log/diamond',
                           ['.keep']))
        if platform.dist()[1].split('.')[0] >= '6':
            data_files.append(('/etc/init',
                               ['rpm/upstart/diamond.conf']))

# Support packages being called differently on different distros
if platform.dist()[0] in ['centos', 'redhat']:
    install_requires=['python-configobj', 'psutil', ],
else:
    install_requires=['ConfigObj', 'psutil', ],

def get_version():
    f = open('version.txt')
    version = ''.join(f.readlines()).rstrip()
    f.close()
    return version

def pkgPath(root, path, rpath="/"):
    global data_files
    if not os.path.exists(path):
        return
    files = []
    for spath in os.listdir(path):
        subpath = os.path.join(path, spath)
        spath = os.path.join(rpath, spath)
        if os.path.isfile(subpath):
            files.append(subpath)

    data_files.append((root + rpath, files))
    for spath in os.listdir(path):
        subpath = os.path.join(path, spath)
        spath = os.path.join(rpath, spath)
        if os.path.isdir(subpath):
            pkgPath(root, subpath, spath)

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
