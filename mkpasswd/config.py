# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2002-2020, Matthew Pounsett <matt@conundrum.com>
# ----------------------------------------------------------------------
"""Configuration for the application."""

import configparser
import logging
import os

config = {}     # pylint: disable=C0103
_LOG = logging.getLogger('config')


def get_config_paths(args, env):
    """
    Return a list of potential config files.

    Check the environment, and if MMINVITE_CONFIG is defined, return that
    value.  If it isn't, and a config path is defined in 'args', then return
    that.  If that isn't defined, then return a list of potential default
    config files to search the filesystem for.
    """
    env_name = 'MMINVITE_CONFIG'
    configs = ["mm_invite.cfg",
               os.path.expanduser("~/.mm_inviterc"),
               "/etc/mm_invite.cfg",
               "/usr/local/etc/mm_invite.cfg",
               ]
    if env.get(env_name, False):
        configs = [env.get(env_name)]
    if args and args.config:
        configs = [args.config]

    return configs


def load_config(args=None):
    """
    Return a configuration.

    If the config has already been loaded, return that config.  Otherwise,
    search the list of paths returned by get_config_paths() for the first
    file that actually exists.  Load and return that.  Otherwise, return an
    error.
    """
    global config   # pylint: disable=W0603,C0103

    if config:
        return config

    config = configparser.ConfigParser(interpolation=None)
    _LOG.debug("finding configuration")
    cfgs = config.read(get_config_paths(args, os.environ))
    if not cfgs:
        raise RuntimeError("no configuration loaded")

    _LOG.debug("loaded configuration %s", cfgs)
    return config
