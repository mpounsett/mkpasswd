# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2002-2020, Matthew Pounsett <matt@conundrum.com>
# ----------------------------------------------------------------------
"""Manage command line interface."""

import argparse
import inspect
import logging
import sys

from .logging import setup_logging
from .passwd import gen_passwd

_LOG = logging.getLogger('cli')


def parse_args(args=None):
    """Parse command line arguments."""
    args = args or sys.argv[1:]

    parser = argparse.ArgumentParser(
        description=inspect.cleandoc(
            """
            This script generates one or more passwords according to the
            options selected on the command line.
            """
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '--loglevel',
        # help="Log level (DEBUG INFO WARNING ERROR CRITICAL)",
        help=argparse.SUPPRESS,
        type=str,
        metavar='LEVEL',
    )

    parser.add_argument(
        '-c', '--lower',
        help="Minimum number of lower-case characters",
        default=2,
        type=int,
        metavar="NUM",
    )

    parser.add_argument(
        '-C', '--upper',
        help="Minimum number of upper-case characters",
        default=2,
        type=int,
        metavar="NUM",
    )

    parser.add_argument(
        '-d', '--digits',
        help="Minimum number of digits",
        default=2,
        type=int,
        metavar="NUM",
    )

    parser.add_argument(
        '-s', '--special',
        help="Minimum number of special characters",
        default=1,
        type=int,
        metavar="NUM",
    )

    parser.add_argument(
        '-l', '--length',
        help="Length of the password(s) to generate.",
        default=12,
        type=int,
        metavar="LENGTH",
    )

    parser.add_argument(
        '-n', '--count',
        help="Number of passwords to generate.",
        default=1,
        type=int,
        metavar="COUNT",
    )

    parser.add_argument(
        '-2', '--alternate',
        help="Alternate left and right hands",
        action='store_true',
        default=False,
    )

    parser.add_argument(
        '-D', '--distinct',
        help=inspect.cleandoc(
            """
            Use only distinct characters.  Does not use anything in the set
            01IOl|
            """
        ),
        action='store_true',
        default=False,
    )

    parser.add_argument(
        '-S', '--skip-characters',
        help="Specify a list of charters to not use in passwords.",
        type=str,
        metavar='LIST',
        default=None,
    )

    parser.add_argument(
        '-H', '--hash',
        help="Also generate a hash suitable for use in a password file.",
        action='store_true',
        default=False,
    )

    args = parser.parse_args(args)

    # Any special arguments tests should go below this line.

    return args


def cli():
    """Set up the command line interface."""
    args = parse_args()
    setup_logging(args)

    passwords = []
    for _ in range(args.count):
        passwords.append(gen_passwd(args))

    for pw in passwords:
        print(pw)
