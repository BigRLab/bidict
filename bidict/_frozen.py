"""Implements :class:`bidict.frozenbidict`."""

from .compat import viewitems, iteritems
from ._common import BidictBase
from ._ordered import OrderedBidictBase
from functools import reduce


class frozenbidict(BidictBase):
    """Immutable, hashable bidict type."""

    def __hash__(self):
        """Return the hash of this frozenbidict."""
        if hasattr(self, '_hashval'):  # Computed lazily.
            return self._hashval
        # Use the _hash() implementation that our ItemsView provides (via collections.Set).
        self._hashval = hv = viewitems(self)._hash()
        return hv


class frozenorderedbidict(OrderedBidictBase):
    """Immutable, hashable ordered bidict type."""

    def __hash__(self):
        """Return the hash of this frozenorderedbidict."""
        if hasattr(self, '_hashval'):  # Computed lazily.
            return self._hashval

        hash_initial = hash(self.__class__)

        def hash_combine(hash_prev, item):
            key, val = item
            return hash((hash_prev, key, val))

        self._hashval = reduce(hash_combine, iteritems(self), hash_initial)

        return self._hashval
