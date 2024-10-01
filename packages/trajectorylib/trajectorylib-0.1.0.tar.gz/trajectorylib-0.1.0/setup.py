#!/usr/bin/env python
# coding: utf-8

from setuptools import find_packages, setup
import os

# Package metadata
NAME = 'trajectorylib'
VERSION = '0.1.0'
DESSCRIPTION = 'A package for analyzing trajectory data from naturalistic driving'
LONG_DESCRIPTION = open('README.md').read()

AUTHOR = 'Rahul Bhadani, Richar Oppiyo'
AUTHOR_EMAIL = 'rahul.bhadani@uah.edu'
URL = 'https://github.com/AARC-lab/trajectorypy'
LICENSE = 'MIT'

INSTALL_REQUIRES = [
    'numpy',
    'scipy',
    'pandas'
]

# Package extras (optional)
EXTRAS_REQUIRE = {
    'dev': ['pytest', 'flake8']
    # 'docs': ['sphinx', 'sphinx_rtd_theme']
}

# Package structure
PACKAGES = find_packages(exclude=['tests', 'tests.*'])

# Package entry points (optional)
ENTRY_POINTS = {
    'console_scripts': [
        # Add entry points here, e.g.
        # 'trajectory = trajectory.cli: main',
    ],
}

# Setup
setup(
    name=NAME,
    version=VERSION,
    description=DESSCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points=ENTRY_POINTS,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    keywords='trajectory analysis machine learning autonomous vehicles transportation traffic',
    project_urls = {
        'Documentation': 'https://aarc-lab.github.io/trajectorypy',
        'Source Code': URL
    }
)