"""Weak-reference support module."""

import sys
from collections.abc import Callable
from typing import Any, Generic, TypeVar, final, overload
from typing_extensions import Self

if sys.version_info >= (3, 9):
    from types import GenericAlias

_C = TypeVar("_C", bound=Callable[..., Any])
_T = TypeVar("_T")

@final
class CallableProxyType(Generic[_C]):  # "weakcallableproxy"
    def __eq__(self, value: object, /) -> bool:
        """Return self==value."""
        ...
    def __getattr__(self, attr: str) -> Any: ...
    __call__: _C

@final
class ProxyType(Generic[_T]):  # "weakproxy"
    def __eq__(self, value: object, /) -> bool:
        """Return self==value."""
        ...
    def __getattr__(self, attr: str) -> Any: ...

class ReferenceType(Generic[_T]):
    __callback__: Callable[[Self], Any]
    def __new__(cls, o: _T, callback: Callable[[Self], Any] | None = ..., /) -> Self: ...
    def __init__(self, o: _T, callback: Callable[[Self], Any] | None = ..., /) -> None: ...
    def __call__(self) -> _T | None:
        """Call self as a function."""
        ...
    def __eq__(self, value: object, /) -> bool:
        """Return self==value."""
        ...
    def __hash__(self) -> int:
        """Return hash(self)."""
        ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any, /) -> GenericAlias:
            """See PEP 585"""
            ...

ref = ReferenceType

def getweakrefcount(object: Any, /) -> int:
    """Return the number of weak references to 'object'."""
    ...
def getweakrefs(object: Any, /) -> list[Any]:
    """Return a list of all weak reference objects pointing to 'object'."""
    ...

# Return CallableProxyType if object is callable, ProxyType otherwise
@overload
def proxy(object: _C, callback: Callable[[_C], Any] | None = None, /) -> CallableProxyType[_C]:
    """
    Create a proxy object that weakly references 'object'.

    'callback', if given, is called with a reference to the
    proxy when 'object' is about to be finalized.
    """
    ...
@overload
def proxy(object: _T, callback: Callable[[_T], Any] | None = None, /) -> Any:
    """
    Create a proxy object that weakly references 'object'.

    'callback', if given, is called with a reference to the
    proxy when 'object' is about to be finalized.
    """
    ...
