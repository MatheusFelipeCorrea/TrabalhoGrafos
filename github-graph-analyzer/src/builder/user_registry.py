from __future__ import annotations

from src.builder.exceptions import UnknownIndexError, UnknownLoginError


class UserRegistry:
    """Deterministic bidirectional mapping between GitHub logins and vertex indices."""

    def __init__(self) -> None:
        self._login_to_index: dict[str, int] = {}
        self._index_to_login: list[str] = []

    def add_user(self, login: str) -> int:
        """Register a login and return its stable vertex index."""

        normalized = str(login or "").strip()
        if not normalized:
            raise ValueError("login is required")
        existing = self._login_to_index.get(normalized)
        if existing is not None:
            return existing
        index = len(self._index_to_login)
        self._login_to_index[normalized] = index
        self._index_to_login.append(normalized)
        return index

    def get_index(self, login: str) -> int:
        """Return the vertex index for a registered login."""

        normalized = str(login or "").strip()
        if not normalized or normalized not in self._login_to_index:
            raise UnknownLoginError(normalized or "<empty>")
        return self._login_to_index[normalized]

    def get_login(self, index: int) -> str:
        """Return the login mapped to a vertex index."""

        if index < 0 or index >= len(self._index_to_login):
            raise UnknownIndexError(index)
        return self._index_to_login[index]

    def __len__(self) -> int:
        return len(self._index_to_login)

    def logins(self) -> list[str]:
        """Return registered logins in index order."""

        return list(self._index_to_login)
