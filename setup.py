# -*- coding: utf-8 -*-
# -----------------------------------------------------------------
# Copyright 2020, Matthew Pounsett <matt@conundrum.com>
# -----------------------------------------------------------------
"""
mkpasswd

Generate a random password, with various options for directing randomness.
"""

from setuptools import setup, find_packages

import mkpasswd

setup(
    name="mkpasswd",
    version=mkpasswd.__version__,
    description=mkpasswd.__doc__,
    long_description=__doc__,
    keywords="password commandline CLI",

    author="Matthew Pounsett",
    author_email="matt@conundrum.com",
    license="TBD",

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'mkpasswd = mkpasswd.cli:cli',
        ],
    },
)
