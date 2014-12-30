#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pkg_resources import ensure_directory
from setuptools import find_packages
from setuptools import setup


ensure_directory('/var/run/xas/xas.pid')
ensure_directory('/etc/xas/config.yml')


setup(
    name='xas',
    version='1.2',

    description='XiVO Acceptance Daemon',

    author='Avencall',
    author_email='dev@avencall.com',

    url='https://github.com/xivo-pbx/xas',

    packages=find_packages(),

    scripts=['bin/xas'],

    data_files=[
        # ('/etc/xas', ['etc/xas/config.yml'])
    ],
)
