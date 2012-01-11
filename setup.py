#!/usr/bin/env python

import os
from glob import glob

if os.environ.get('USE_SETUPTOOLS'):
    from setuptools import setup
    setup_kwargs = dict(zip_safe=0)
else:
    from distutils.core import setup
    setup_kwargs = dict()

if os.getenv('VIRTUAL_ENV', False):
    data_files=[
        ('etc/diamond',                        glob('conf/*.conf.*') ),
        ('etc/diamond/collectors',             glob('conf/collectors/*') ),
        ('share/diamond',                      ['LICENSE', 'README.md'] ),
        ('share/diamond/user_scripts',         [] ),
    ]
else:
    data_files=[
        ('/etc/diamond',                       glob('conf/*.conf.*') ),
        ('/etc/diamond/collectors',            glob('conf/collectors/*') ),
        ('share/diamond',                      ['LICENSE', 'README.md'] ),
        ('share/diamond/user_scripts',         [] ),
    ]

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
            
    data_files.append((root+rpath, files))
    for spath in os.listdir(path):
        subpath = os.path.join(path, spath)
        spath = os.path.join(rpath, spath)
        if os.path.isdir(subpath):
            pkgPath(root, subpath, spath)
            
pkgPath('share/diamond/collectors', 'src/collectors')

setup(
    name            = 'diamond',
    version         = '0.2.0',
    url             = 'https://github.com/BrightcoveOS/Diamond',
    author          = 'The Diamond Team',
    author_email    = 'https://github.com/BrightcoveOS/Diamond',
    license         = 'MIT License',
    description     = 'Smart data producer for graphite graphing package',
    package_dir     = {'' : 'src'},
    packages        = ['diamond'],
    scripts         = glob('bin/*'),
    data_files      = data_files,
    test_suite      = 'test.main',
    **setup_kwargs
)
