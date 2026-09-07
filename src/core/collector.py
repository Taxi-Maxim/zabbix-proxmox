"""Base interface for monitoring collectors."""

from abc import ABC, abstractmethod
from typing import Any


class Collector(ABC):
    """Collect one monitoring payload without writing to stdout."""

    @abstractmethod
    def collect(self) -> dict[str, Any]:
        """Return the collector payload as a JSON-compatible dictionary."""
        raise NotImplementedError