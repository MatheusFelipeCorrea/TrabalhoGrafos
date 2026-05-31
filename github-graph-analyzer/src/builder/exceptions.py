from __future__ import annotations


class BuilderError(Exception):
    """Base error for graph builder domain failures."""


class UnknownLoginError(BuilderError):
    """Raised when a login is not registered."""

    def __init__(self, login: str) -> None:
        self.login = login
        super().__init__(f"Unknown login: {login}")


class UnknownIndexError(BuilderError):
    """Raised when a vertex index is not mapped to any login."""

    def __init__(self, index: int) -> None:
        self.index = index
        super().__init__(f"Unknown vertex index: {index}")


class InvalidCsvError(BuilderError):
    """Raised when a CSV file is missing required columns or rows."""

    def __init__(self, path: str, detail: str) -> None:
        self.path = path
        self.detail = detail
        super().__init__(f"Invalid CSV '{path}': {detail}")
