# -*- coding: utf-8 -*-
# -----------------------------------------------------------------
# Copyright 2002-2020, Matthew Pounsett <matt@conundrum.com>
# -----------------------------------------------------------------

import logging
import logging.config


def setup_logging(args):
    DEFAULT_LEVEL = 'WARNING'
    DEFAULT_FORMAT = '%(asctime)s %(levelname)s %(message)s'

    if args.loglevel:
        log_level = args.loglevel.strip().upper()
    else:
        log_level = DEFAULT_LEVEL

    log_format = DEFAULT_FORMAT

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': log_format
            },
        },
        'handlers': {
            'console': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': log_level,
        },

    }

    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger('setup_logging')
    logger.debug("logging configred")
