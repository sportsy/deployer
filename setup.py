#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from setuptools import setup, find_packages
import re
import os
import codecs


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with open('requirements-dev.txt') as f:
    tests_require = f.read().splitlines()

print install_requires
print tests_require

setup(
    name='deployer',
    version=find_version("deployer", "__init__.py"),
    description='',
    url='https://github.com/sportsy/deployer',
    author='Sportsy',
    license='MIT',
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    test_suite='nose.collector',
    install_requires=install_requires,
    dependency_links=['https://github.com/ekulyk/PythonPusherClient.git#egg=pusherclient==0.2.0'],
    tests_require=tests_require,
    entry_points="""
    [console_scripts]
    deployer=deployer.main:main
    """,
)
