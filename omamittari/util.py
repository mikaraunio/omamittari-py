#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


def make_params(args, nmax=None):
    """Format GET parameters for the API endpoint.

    In particular, the endpoint requires that parameters be sorted
    alphabetically by name, and that filtering is done only on one
    parameter when multiple filters are offered.
    """

    if nmax and len(args) > nmax:
        raise ValueError("Too many parameters supplied")
    return [(k, stringify(args[k])) for k in sorted(args.keys())]


def stringify(arg):
    """Comma-separate (without spaces) tuples and lists,
    convert dates to "yyyy-mm-dd", and stringify everything else"""

    if isinstance(arg, (tuple, list)):
        s = ",".join((str(n) for n in arg))
    elif isinstance(arg, datetime):
        s = arg.strftime("%Y-%m-%d")
    else:
        s = str(arg)
    return s
