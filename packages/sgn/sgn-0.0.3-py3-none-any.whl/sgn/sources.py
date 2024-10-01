"""Source elements for generating data streams.

New classes need not be subclassed from DequeSource, but should at least be ultimately a subclass of SourceElement.
"""

from collections import deque
from dataclasses import dataclass
from typing import Union, Iterator, Generator, Iterable, Any

from .base import Frame, SourceElement, SourcePad


@dataclass
class NullSource(SourceElement):
    """A source that does precisely nothing. It is useful for testing and debugging,
    and will always produce empty frames
    """

    frame_factory: callable = Frame

    def __post_init__(self):
        super().__post_init__()

    def new(self, pad: SourcePad) -> Frame:
        """New Frames are created on "pad" with an instance specific count and a
        name derived from the pad name. EOS is set if we have surpassed the
        requested number of Frames.

        Args:
            pad:
                SourcePad, the pad for which to produce a new Frame

        Returns:
            Frame, the Frame with optional data payload
        """
        return self.frame_factory(EOS=True, data=None)


@dataclass
class IterSource(SourceElement):
    """A source element that has one iterable per source pad. The
    end of stream is controlled by setting an optional limit on the number of
    times a deque can be empty before EOS is signaled.

    Args:
        iters:
            dict[str, Iterable[Any]], a mapping of source pads to iterables, where the key
            is the pad name and the value is the Iterable. These will be coerced to
            iterators, so they can be any iterable type.
        eos_on_empty:
            Union[dict[str, bool], bool], default True, a mapping of source pads to boolean values,
            where the key is the pad name and the value is the boolean. If a bool is given,
            the value is applied to all pads. If True, EOS is signaled when the iterator is empty.
    """

    iters: dict[str, Iterable[Any]] = None
    eos_on_empty: Union[dict[str, bool], bool] = True
    frame_factory: callable = Frame

    def __post_init__(self):
        """Post init checks for the DequeSource element."""
        super().__post_init__()
        # Setup pad counts
        self._setup_iters()
        self._setup_eos_on_empty()
        self._validate_iters()
        self._validate_eos_on_empty()

    def _setup_iters(self):
        # Setup the iter_map if not given
        if self.iters is None:
            self.iters = {
                pad.name: self._coerce_iterator([]) for pad in self.source_pads
            }
        else:
            self.iters = {
                name: self._coerce_iterator(iterable)
                for name, iterable in self.iters.items()
            }

    def _setup_eos_on_empty(self):
        # Setup the limits if not given
        if isinstance(self.eos_on_empty, bool):
            self.eos_on_empty = {
                pad.name: self.eos_on_empty for pad in self.source_pads
            }

    def _validate_iters(self):
        # Check that the deque_map has the correct number of deque s
        if not len(self.iters) == len(self.source_pads):
            raise ValueError("The number of deque s must match the number of pads")

        # Check that the deque_map has the correct pad names
        for pad_name in self.iters:
            if pad_name not in [pad.name for pad in self.source_pads]:
                raise ValueError(
                    f"DequeSource has a deque  for a pad that does not exist, got: {pad_name}, "
                    f"options are: {[pad.name for pad in self.source_pads]}"
                )

    def _validate_eos_on_empty(self):
        # Check that the limits has the correct number of limits
        if not len(self.eos_on_empty) == len(self.source_pads):
            raise ValueError("The number of eos on empty must match the number of pads")

        # Check that the limits has the correct pad names
        for pad_name in self.eos_on_empty:
            if pad_name not in [pad.name for pad in self.source_pads]:
                raise ValueError(
                    f"DequeSource has a eos on empty for a pad that does not exist, "
                    f"got: {pad_name}, options are: {self.source_pad_names}"
                )

    def _coerce_iterator(self, iterable):
        """Coerce the iterable to an iterator if it is not already one.

        Args:
            iterable:
                Iterable, the iterable to coerce

        Returns:
            Iterator, the iterator
        """
        # Check if already an iterator or generator
        if isinstance(iterable, (Iterator, Generator)):
            return iterable

        return iter(iterable)

    def _get_value(self, iterator):
        """Get the next value from the iterator.

        Args:
            iterator:
                Iterator, the iterator to get the value from

        Returns:
            Any, the next value from the iterator
        """
        try:
            return next(iterator)
        except StopIteration:
            return None

    def update(self, pad: SourcePad):
        """Update the iterator for the pad. This is a no-op for IterSource.
        For subclasses that need to update the iterator, this method should be overridden.
        Examples include reading from a file or network stream.

        Args:
            pad:
                SourcePad, the pad to update
        """
        pass

    def new(self, pad: SourcePad) -> Frame:
        """New Frames are created on "pad" with an instance specific count and a
        name derived from the pad name. EOS is set if we have surpassed the
        requested number of Frames.

        Args:
            pad:
                SourcePad, the pad for which to produce a new Frame

        Returns:
            Frame, the Frame with optional data payload
        """
        # Update the pad iterator
        self.update(pad=pad)

        # Get the pad iterator
        pad_iter = self.iters[pad.name]
        pad_eos_on_empty = self.eos_on_empty[pad.name]

        # Get data from the iterator
        data = self._get_value(pad_iter)

        # Return the frame
        return self.frame_factory(EOS=data is None and pad_eos_on_empty, data=data)


@dataclass
class DequeSource(IterSource):
    """A source element that has one double-ended-queue (deque ) per source pad. The
    end of stream is controlled by setting an optional limit on the number of
    times a deque can be empty before EOS is signaled.

    Args:
        iters:
            dict[str, deque ], a mapping of source pads to deque s, where the key
            is the pad name and the value is the deque
        eos_on_empty:
            Union[dict[str, bool], bool], default True, a mapping of source pads to boolean values,
            where the key is the pad name and the value is the boolean. If a bool is given,
            the value is applied to all pads. If True, EOS is signaled when the deque is empty.
    """

    def _coerce_iterator(self, iterable):
        """Coerce the iterable to an iterator if it is not already one.

        Args:
            iterable:
                Iterable, the iterable to coerce

        Returns:
            Iterator, the iterator
        """
        return deque(iterable)

    def _get_value(self, deque):
        """Get the next value from the deque.

        Args:
            deque :
                deque , the deque to get the value from

        Returns:
            Any, the next value from the deque
        """
        try:
            return deque.pop()
        except IndexError:
            return None

    @property
    def deques(self) -> dict[str, deque]:
        """Get the iters property with more explicit alias"""
        return self.iters
