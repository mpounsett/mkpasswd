# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright 2002-2020, Matthew Pounsett <matt@conundrum.com>
#
# Reimplemented from the original Perl, September 2020.
# ----------------------------------------------------------------------
"""Password generation routines."""

import logging
import random


_LOG = logging.getLogger(__name__)


def gen_passwd(args):
    """
    Generate a random password.

    First, generate a text field that is MULT * the length of the required
    password.  In generating the field, either alternate the
    ALL_LEFT/ALL_RIGHT charsets or select from ALL.

    Create a window (slice) the length of the required password and pass it
    from left to right along the text field.  Beginning at the left, test
    whether the string in the window meets the password requirements. If yes,
    return that text.  If no, slide the window one character to the right and
    test again.

    Repeat until either a password is returned, or the window hits the right
    edge of the field.  If it makes it all the way to the right, start over.
    """

    # How many times longer than the requested password should the character
    # field be?
    MULT = 20

    # Generate all the various character sets that will be required for easy
    # character selection and testing.
    CHARSETS = {
        'LEFT_LOWER': [char for char in 'qwertasdfgzxvb'],
        'RIGHT_LOWER': [char for char in 'yuiophjklnm'],
        'LEFT_NUM': [char for char in '123456'],
        'RIGHT_NUM': [char for char in '7890'],
        'LEFT_SPECIAL': [char for char in '`!#$%@~'],
        'RIGHT_SPECIAL': [char for char in '"&\'()*+,-./:;<=>?[\\]^_{|}'],
        'INDISTINCT': [char for char in '01IOl|'],
    }
    CHARSETS['LEFT_UPPER'] = [char.upper() for char in CHARSETS['LEFT_LOWER']]
    CHARSETS['RIGHT_UPPER'] = [char.upper() for char in
                               CHARSETS['RIGHT_LOWER']]
    CHARSETS['ALL_LOWER'] = CHARSETS['LEFT_LOWER'] + CHARSETS['RIGHT_LOWER']
    CHARSETS['ALL_UPPER'] = CHARSETS['LEFT_UPPER'] + CHARSETS['RIGHT_UPPER']
    CHARSETS['ALL_NUM'] = CHARSETS['LEFT_NUM'] + CHARSETS['RIGHT_NUM']
    CHARSETS['ALL_SPECIAL'] = (CHARSETS['LEFT_SPECIAL'] +
                               CHARSETS['RIGHT_SPECIAL'])
    CHARSETS['ALL_LEFT'] = (CHARSETS['LEFT_LOWER'] +
                            CHARSETS['LEFT_UPPER'] +
                            CHARSETS['LEFT_NUM'] +
                            CHARSETS['LEFT_SPECIAL'])
    CHARSETS['ALL_RIGHT'] = (CHARSETS['RIGHT_LOWER'] +
                             CHARSETS['RIGHT_UPPER'] +
                             CHARSETS['RIGHT_NUM'] +
                             CHARSETS['RIGHT_SPECIAL'])

    CHARSETS['ALL'] = CHARSETS['ALL_LEFT'] + CHARSETS['ALL_RIGHT']

    skip_chars = ''
    if args.distinct:
        skip_chars += ''.join(CHARSETS['INDISTINCT'])
    if args.skip_characters:
        skip_chars += args.skip_characters

    skip_chars = ''.join(sorted(set(skip_chars)))

    passwd = ''
    attempt = 0

    while passwd == '':
        attempt += 1
        _LOG.debug('Generation attempt number %d', attempt)
        if skip_chars != '':
            _LOG.debug(" Using indistinct list '%s'", skip_chars)

        field_length = MULT * args.length
        char_field = ''
        next = ''
        next_is_left = random.choice([True, False])

        while len(char_field) < field_length:
            if not args.alternate:
                next = random.choice(CHARSETS['ALL'])
            elif next_is_left:
                next = random.choice(CHARSETS['ALL_LEFT'])
            else:
                next = random.choice(CHARSETS['ALL_RIGHT'])

            if next in skip_chars:
                _LOG.debug(" Skipping character '%s'", next)
                continue
            else:
                char_field += next
                next_is_left = not next_is_left

        left = 0
        right = args.length

        while passwd == '' and right < field_length:
            _LOG.debug(" Window number %d", (left + 1))
            success = True
            candidate = char_field[slice(left, right)]
            _LOG.debug("  Candidate is '%s'", candidate)

            # count lowercase
            lc_list = [char for char in candidate
                       if char in CHARSETS['ALL_LOWER']]
            if len(lc_list) < args.lower:
                success = False

            # count uppercase
            uc_list = [char for char in candidate
                       if char in CHARSETS['ALL_UPPER']]
            if len(uc_list) < args.upper:
                success = False

            # count numbers
            num_list = [char for char in candidate
                        if char in CHARSETS['ALL_NUM']]
            if len(num_list) < args.digits:
                success = False

            # count special
            special_list = [char for char in candidate
                            if char in CHARSETS['ALL_SPECIAL']]
            if len(special_list) < args.special:
                success = False

            _LOG.debug("  lc = %d, uc = %d, num = %d, spec = %d",
                       len(lc_list),
                       len(uc_list),
                       len(num_list),
                       len(special_list))

            if success:
                passwd = candidate
            else:
                left += 1
                right += 1

    return passwd
