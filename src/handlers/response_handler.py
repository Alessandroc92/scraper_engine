"""A module that deals with handling HTTP responses."""

from typing import runtime_checkable


@runtime_checkable
class HttpResponse(Protocol):
    """Minimal interface that every adapter response must expose."""

    @property
    def status_code(self) -> int: ...
    @property
    def text(self) -> str: ...
    def json(self) -> Any: ...