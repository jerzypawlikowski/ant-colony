#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


def read_readme():
    with open("README.rst") as file:
        return file.read()


def read_license():
    with open("LICENSE") as file:
        return file.read()

setup(
    name="ant_colony",
    author="Jerzy Pawlikowski",
    author_email="me@jerzypawlikowski.pl",
    version="0.1.2",
    url="https://github.com/jurekpawlikowski/ant-colony",
    package_dir={"ant_colony": "ant_colony"},
    packages=["ant_colony"],
    license=read_license(),
    description="Implementation of the Ant Colony system",
    long_description=read_readme()
)
