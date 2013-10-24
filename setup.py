#!/usr/bin/env python
from setuptools import setup

setup(
    name='mm',
    version='1.0',
    install_requires=['Twisted', 'pyOpenSSL'],
    packages=['mm', 'mm.tests'],
    entry_points={
        'console_scripts': ['mm = mm:main']
    },
    url='http://bunnyman.info',
    license='BSD',
    author='bunnyman',
    author_email='WagThatTail@Me.com',
    description='An "ii" clone for mucks/telnet sessions'
)
