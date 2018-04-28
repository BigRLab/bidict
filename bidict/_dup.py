# -*- coding: utf-8 -*-
# Copyright 2018 Joshua Bronson. All Rights Reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


"""Provides bidict duplication policies and the :class:`_OnDup` class."""


from collections import namedtuple

from ._marker import _MarkerMeta, _make_marker


_OnDup = namedtuple('_OnDup', 'key val kv')


class DuplicationPolicy(_MarkerMeta):
    """Metaclass for bidict's duplication policies.

    *See also* :ref:`basic-usage:Values Must Be Unique`
    """
    def __repr__(cls):  # noqa: N805 (first argument of a method should be named 'self')
        return '<DUP_POLICY.%s>' % cls.__name__


RAISE = _make_marker('RAISE', type_=DuplicationPolicy, dict_={'__doc__': """\
Raise an exception when a duplication is encountered.
"""})

OVERWRITE = _make_marker('OVERWRITE', type_=DuplicationPolicy, dict_={'__doc__': """\
Overwrite an existing item when a duplication is encountered.
"""})

IGNORE = _make_marker('IGNORE', type_=DuplicationPolicy, dict_={'__doc__': """\
Keep the existing item and ignore the new item when a duplication is encountered.
"""})
