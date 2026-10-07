"""A custom context manager that guarantees a resource is closed, even on error."""

import logging
from collections.abc import Iterator
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class ManagedResource:
    """Stand-in for something like a file handle or a connection."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.is_open = False

    def open(self) -> None:
        self.is_open = True
        logger.info("Opened resource: %s", self.name)

    def close(self) -> None:
        self.is_open = False
        logger.info("Closed resource: %s", self.name)

    def use(self) -> str:
        if not self.is_open:
            raise RuntimeError("Resource is not open")
        return f"using {self.name}"


@contextmanager
def managed_resource(name: str) -> Iterator[ManagedResource]:
    resource = ManagedResource(name)
    resource.open()
    try:
        yield resource
    finally:
        # This runs even if an exception happened inside the `with` block,
        # so the resource never gets left open accidentally.
        resource.close()