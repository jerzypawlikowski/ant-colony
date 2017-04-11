#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="ant_colony",
    author="Jerzy Pawlikowski",
    author_email="me@jerzypawlikowski.pl",
    version="0.1.0",
    url="https://github.com/jurekpawlikowski/ant-colony",
    package_dir={"ant_colony": "ant_colony"},
    packages=["ant_colony"],
    license=open("LICENSE").read(),
    description="Implementation of the Ant Colony system",
    long_description=open("README.rst").read()
)
