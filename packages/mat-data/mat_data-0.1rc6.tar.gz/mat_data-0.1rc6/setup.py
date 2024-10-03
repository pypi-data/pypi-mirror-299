# -*- coding: utf-8 -*-
"""
MAT-Tools: Python Framework for Multiple Aspect Trajectory Data Mining

The present application offers a tool, to support the user in the preprocessing of multiple aspect trajectory data. It integrates into a unique framework for multiple aspects trajectories and in general for multidimensional sequence data mining methods.
Copyright (C) 2022, MIT license (this portion of code is subject to licensing from source project distribution)

Created on Dec, 2023
Copyright (C) 2023, License GPL Version 3 or superior (see LICENSE file)

@author: Tarlis Portela
"""
import setuptools

import configparser
config = configparser.ConfigParser()
config.read('pyproject.toml')
VERSION = config['project']['version'].strip('"')
PACKAGE_NAME = config['project']['name'].strip('"')
DEV_VERSION = "0.1b0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
#    version=DEV_VERSION,
    author="Tarlis Portela",
    author_email="tarlis@tarlis.com.br",
    description="MAT-data: Data Preprocessing for Multiple Aspect Trajectory Data Mining",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mat-analysis/mat-data",
#    packages=setuptools.find_packages(include=[PACKAGE_NAME, PACKAGE_NAME+'.*']),
    packages=setuptools.find_packages(),
#    include_package_data=True,
    scripts=[
         'scripts/MAT-GetData.py',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    keywords='data mining, python, trajectory classification, trajectory analysis, movelets',
    license='GPL Version 3 or superior (see LICENSE file)',
)
