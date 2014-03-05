#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

from setuptools import setup, find_packages

__docformat__ = "restructuredtext en"

setup(
    author = "Martin Ueding",
    author_email = "dev@martin-ueding.de",
    description = "Parses CSV-CAMT bank account balances into a SQLite DB, generates plots",
    license = "GPL2",
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python",

    ],
    name = "bank-statement-parser",
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'bank-statement-parser = bankstatement.__init__:main',
        ],
    },
    install_requires=[
    ],
    url = "https://github.com/martin-ueding/bank-statement-parser",
    download_url="http://martin-ueding.de/download/bank-statement-parser/",
    version = "1.0",
)
