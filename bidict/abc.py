"""Provides :class:`BidirectionalMapping`."""

from __future__ import absolute_import
from .compat import iteritems
from abc import abstractproperty
from collections import Mapping


class BidirectionalMapping(Mapping):
    """Abstract base class for bidirectional mappings.
    Extends :class:`collections.abc.Mapping`.

    .. py:attribute:: _subclsattrs

        The attributes that :attr:`__subclasshook__` checks for to determine
        whether a class is a subclass of :class:`BidirectionalMapping`.

    """

    __slots__ = ()

    @abstractproperty
    def inv(self):
        """The inverse bidict."""
        raise NotImplementedError  # pragma: no cover

    def __inverted__(self):
        """Get an iterator over the items in :attr:`inv`."""
        return iteritems(self.inv)

    _subclsattrs = frozenset({
        'inv', '__inverted__',
        # see "Mapping" in the table at
        # https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes
        '__getitem__', '__iter__', '__len__',  # abstract methods
        '__contains__', 'keys', 'items', 'values', 'get', '__eq__', '__ne__',  # mixin methods
    })

    @classmethod
    def __subclasshook__(cls, C):
        """Check if C provides all the attributes in :attr:`_subclsattrs`.

        Causes conforming classes to be virtual subclasses automatically.
        """
        if cls is BidirectionalMapping:
            mro = C.__mro__
            return all(any(B.__dict__.get(i) for B in mro) for i in cls._subclsattrs)
        return NotImplemented
