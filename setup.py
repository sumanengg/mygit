#!/usr/bin/env python3

from setuptools import setup

setup (
    name = "mygit",
    version = '1.0.0',
    packages = ['mygit'],
    entry_points = {
        'console_scripts' : [
            'mygit = mygit.cli:main'
        ]
    }
)