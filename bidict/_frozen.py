"""Implements the frozen (immutable, hashable) bidict types."""

from ._common import BidictBase, _marker
from ._ordered import OrderedBidictBase
from .compat import iteritems
from abc import abstractmethod
from collections import Hashable
from itertools import chain, islice


class FrozenBidictBase(Hashable):
    """
    Base class for frozen bidict types.

    .. py:attribute:: _HASH_NITEMS_MAX

        The maximum number of items that participate in influencing the hash
        value. Gives users the ability to bound the time and space complexity
        of an initial call to :attr:`__hash__` to a lower value than the total
        number of items, at the expense of a possible (but probably unlikely)
        increase in hash collisions for almost-equal instances.

        Defaults to ``None`` so that all items participate in influencing the
        hash value by default. This default may be reconsidered if it is shown
        that a different value is generally better. See discussion at
        <https://groups.google.com/d/topic/python-ideas/XcuC01a8SYs/discussion>.

        See :attr:`__hash__` for more information.

    """

    _HASH_NITEMS_MAX = None

    @abstractmethod
    def _compute_hash(self, items):
        """Abstract method to actually compute the hash of ``items``."""
        return NotImplemented

    def __hash__(self):
        """
        Return the hash of this frozen bidict from its contained items.

        The number of participating items may be limited by
        :attr:`_HASH_NITEMS_MAX`.

        Delegates to subclasses' :attr:`_compute_hash` implementations on the
        first call, then caches the result to make future calls O(1).

        Creates an iterable of items based on :attr:`_HASH_NITEMS_MAX`
        and passes it to :attr:`_compute_hash`.
        A marker item derived from the class name is also prepended, to
        canonicalize the resulting hash.
        """
        if hasattr(self, '_hashval'):  # Cached on the first call.
            return self._hashval
        marker = _marker(self.__class__.__name__)
        marker = (marker, marker)  # shaped like an item to allow flattening
        items = islice(iteritems(self), self._HASH_NITEMS_MAX)
        items = chain((marker,), items)
        self._hashval = hv = self._compute_hash(items)
        return hv


class frozenbidict(FrozenBidictBase, BidictBase):
    """Regular frozen bidict type."""

    def _compute_hash(self, items):
        """
        Because the items of a :class:`frozenbidict` have no guaranteed order,
        this could use the set hash algorithm provided by
        ``collections.Set._hash()`` to incrementally compute a hash from an
        iterable of items in constant space. However, instead this creates an
        ephemeral frozenset out of ``items`` which is passed to :func:`hash`.
        On CPython, this results in the faster ``frozenset_hash`` routine
        (implemented in ``setobject.c``) being used, trading space for time.
        Python does not expose a way to use the ``frozenset_hash`` algorithm
        with an iterable, so an ephemeral frozenset must be created to use it.

        Time and space complexity can be limited by setting
        :attr:`_HASH_NITEMS_MAX <FrozenBidictBase._HASH_NITEMS_MAX>`.
        """
        return hash(frozenset(items))


class frozenorderedbidict(FrozenBidictBase, OrderedBidictBase):
    """Ordered frozen bidict type."""

    def _compute_hash(self, items):
        """
        Because items are ordered, this uses Python's tuple hash algorithm to
        compute a hash from ``items``.

        Python does not expose its internal tuple hash algorithm so it can be
        used with any iterable. So to use CPython's fast ``tuplehash`` routine
        (implemented in ``tupleobject.c``), an ephemeral tuple must be created
        and passed to :func:`hash`.

        Time and space complexity can be limited by setting
        :attr:`_HASH_NITEMS_MAX <FrozenBidictBase._HASH_NITEMS_MAX>`.
        """
        # Flatten to avoid recursive calls to tuplehash. Noticeable speedup.
        items = chain.from_iterable(items)
        return hash(tuple(items))
