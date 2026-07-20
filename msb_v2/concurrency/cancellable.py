"""Cancellable computation monad for the Sovereign Agent Runtime.

Every SAR action returns ``Cancellable<Output>`` so cancellation can
propagate automatically through bind/fmap without ad hoc checks.
"""

from __future__ import annotations

import dataclasses
from typing import Callable, Generic, Optional, TypeVar, Union

T = TypeVar("T")
U = TypeVar("U")


@dataclasses.dataclass
class Cancelled:
    """Zero element of the ``Cancellable`` monad."""

    reason: Optional[str] = None
    metadata: dict = dataclasses.field(default_factory=dict)

    def map(self, _: Callable[..., object]) -> Cancelled:
        return self

    def bind(self, _: Callable[..., object]) -> Cancelled:
        return self


@dataclasses.dataclass
class Done(Generic[T]):
    """Success element of the ``Cancellable`` monad."""

    value: T

    def map(self, fn: Callable[..., object]) -> Done:
        return Done(fn(self.value))

    def bind(self, fn: Callable[..., object]) -> object:
        return fn(self.value)


CancellableOutput = Union[Cancelled, Done[T]]


def is_cancelled(result: object) -> bool:
    return isinstance(result, Cancelled)


def cancel(reason: Optional[str] = None, **metadata: object) -> Cancelled:
    return Cancelled(reason=reason, metadata=dict(metadata))


def done(value: T) -> Done[T]:
    return Done(value=value)


def bind(result: CancellableOutput[T], fn: Callable[..., object]) -> CancellableOutput[object]:
    """Monadic bind with cancellation propagation."""
    if isinstance(result, Cancelled):
        return result
    return fn(result.value)


def fmap(result: CancellableOutput[T], fn: Callable[..., object]) -> CancellableOutput[object]:
    """Functor map."""
    if isinstance(result, Cancelled):
        return result
    return Done(fn(result.value))
