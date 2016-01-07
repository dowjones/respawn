#!/usr/bin/env python

""" Setup script. Used by easy_install and pip. """

import os
from setuptools import setup, find_packages
from setuptools.command.test import test
import sys


class PyTest(test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = ['respawn']

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def get_version():
    try:
        # get version from './VERSION'
        src_root = os.path.dirname(__file__)
        if not src_root:
            src_root = '.'

        with open(src_root + '/VERSION', 'r') as f:
            version = f.readline ().strip()

        return version

    except Exception as e:
        raise RuntimeError('Could not extract version: %s' % e)

# Check Python version. Required > 2.7, <3.x
if  sys.hexversion < 0x02070000 or sys.hexversion >= 0x03000000:
    raise RuntimeError("respawn requires Python 2.x (2.7 or higher)")

setup_args = {
    'name': 'respawn',
    'version': get_version(),
    'description': 'AWS CloudFormation Template generator from Yaml specifications.',
    'url': 'https://github.com/dowjones/respawn/',
    'license': 'ISC',
    'keywords': 'aws cloudformation yaml',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: System :: Systems Administration',
        'Operating System :: OS Independent'
    ],
    'packages': find_packages(),
    'package_data': {'respawn': ['VERSION']},
    'entry_points': {
        'console_scripts': [
            'respawn=respawn.cli:generate',
        ],
    },
    'install_requires': [
        'cfn-pyplates',
        'Jinja2',
        'boto3',
        'botocore'
    ],
    'tests_require': ['pytest'],
    'cmdclass': {'test': PyTest},
    'zip_safe': False,
}

setup(**setup_args)

