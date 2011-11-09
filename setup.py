#!/usr/bin/env python

import os
from glob import glob

if os.environ.get('USE_SETUPTOOLS'):
    from setuptools import setup
    setup_kwargs = dict(zip_safe=0)
else:
    from distutils.core import setup
    setup_kwargs = dict()

setup(
    name='diamond',
    version='0.2.0',
    url='https://github.com/sandello/Diamond',
    author='Ivan Pouzyrevsky',
    author_email='ivan.pouzyrevsky@gmail.com',
    license='MIT License',
    description='Smart producer for graphite graphing package',
    package_dir={'' : 'src'},
    packages=['diamond'],
    scripts=glob('bin/*'),
    data_files=[
        ('conf', glob('conf/*')),
        ('collectors', glob('src/collectors/*.py')),
        ('storage/log', []),
        ('storage/archive', []),
    ],
    **setup_kwargs
)
