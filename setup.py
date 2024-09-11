#!/usr/bin/env python

from setuptools import setup

setup(
    entry_points={"console_scripts": ["videopack=videopack.cli:main"]}, name="videopack"
)
