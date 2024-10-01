from _typeshed import StrPath
from collections.abc import Iterable, Sequence
from datetime import datetime, timedelta, tzinfo
from typing import Any, Protocol
from typing_extensions import Self

__all__ = ["ZoneInfo", "reset_tzpath", "available_timezones", "TZPATH", "ZoneInfoNotFoundError", "InvalidTZPathWarning"]

class _IOBytes(Protocol):
    def read(self, size: int, /) -> bytes: ...
    def seek(self, size: int, whence: int = ..., /) -> Any: ...

class ZoneInfo(tzinfo):
    @property
    def key(self) -> str: ...
    def __init__(self, key: str) -> None: ...
    @classmethod
    def no_cache(cls, key: str) -> Self:
        """Get a new instance of ZoneInfo, bypassing the cache."""
        ...
    @classmethod
    def from_file(cls, fobj: _IOBytes, /, key: str | None = None) -> Self:
        """Create a ZoneInfo file from a file object."""
        ...
    @classmethod
    def clear_cache(cls, *, only_keys: Iterable[str] | None = None) -> None:
        """Clear the ZoneInfo cache."""
        ...
    def tzname(self, dt: datetime | None, /) -> str | None:
        """Retrieve a string containing the abbreviation for the time zone that applies in a zone at a given datetime."""
        ...
    def utcoffset(self, dt: datetime | None, /) -> timedelta | None:
        """Retrieve a timedelta representing the UTC offset in a zone at the given datetime."""
        ...
    def dst(self, dt: datetime | None, /) -> timedelta | None:
        """Retrieve a timedelta representing the amount of DST applied in a zone at the given datetime."""
        ...

# Note: Both here and in clear_cache, the types allow the use of `str` where
# a sequence of strings is required. This should be remedied if a solution
# to this typing bug is found: https://github.com/python/typing/issues/256
def reset_tzpath(to: Sequence[StrPath] | None = None) -> None: ...
def available_timezones() -> set[str]: ...

TZPATH: tuple[str, ...]

class ZoneInfoNotFoundError(KeyError): ...
class InvalidTZPathWarning(RuntimeWarning): ...

def __dir__() -> list[str]: ...
