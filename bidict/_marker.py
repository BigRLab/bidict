# -*- coding: utf-8 -*-
# Copyright 2018 Joshua Bronson. All Rights Reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


"""Provides a convenient way of representing singletons for internal use.

>>> SENTINEL = _make_marker('SENTINEL')
>>> SENTINEL
<SENTINEL>
>>> SENTINEL()
Traceback (most recent call last):
    ...
TypeError: ...
"""


class _MarkerMeta(type):
    def __repr__(cls):  # noqa: N805 (first argument of a method should be named 'self')
        return '<%s>' % cls.__name__


class _SingletonClass(object):  # pylint: disable=too-few-public-methods
    def __init__(self):
        raise TypeError('Singleton class cannot be instantiated, use class object directly instead')


def _make_marker(name, type_=_MarkerMeta, bases=(_SingletonClass,), dict_=None):
    return type_(name, bases, {} if dict_ is None else dict_)
