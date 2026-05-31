from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, ClassVar


@dataclass(frozen=True)
class Interaction:
    """Normalized interaction exported to the graph builders."""

    src_login: str
    dst_login: str
    type: str
    weight: int
    timestamp: str
    source_id: str

    ALLOWED_TYPES: ClassVar[set[str]] = {
        "comment_issue",
        "comment_pr",
        "open_issue_commented",
        "review_pr",
        "merge_pr",
        "close_issue",
    }

    def __post_init__(self) -> None:
        src_login = self._normalize_login(self.src_login, "src_login")
        dst_login = self._normalize_login(self.dst_login, "dst_login")
        interaction_type = str(self.type).strip()
        if interaction_type not in self.ALLOWED_TYPES:
            raise ValueError(f"Invalid interaction type: {interaction_type}")
        if src_login == dst_login:
            raise ValueError("Self interactions are not allowed")
        if int(self.weight) <= 0:
            raise ValueError("weight must be positive")

        object.__setattr__(self, "src_login", src_login)
        object.__setattr__(self, "dst_login", dst_login)
        object.__setattr__(self, "type", interaction_type)
        object.__setattr__(self, "weight", int(self.weight))
        object.__setattr__(self, "timestamp", self._normalize_timestamp(self.timestamp))
        object.__setattr__(self, "source_id", str(self.source_id).strip())

    def to_row(self) -> dict[str, Any]:
        """Return the CSV row using the official mining schema."""

        return {
            "src_login": self.src_login,
            "dst_login": self.dst_login,
            "type": self.type,
            "weight": self.weight,
            "timestamp": self.timestamp,
            "source_id": self.source_id,
        }

    @staticmethod
    def _normalize_login(value: str, field_name: str) -> str:
        login = str(value or "").strip()
        if not login:
            raise ValueError(f"{field_name} is required")
        return login

    @staticmethod
    def _normalize_timestamp(value: object) -> str:
        if isinstance(value, datetime):
            dt = value.astimezone(timezone.utc) if value.tzinfo else value.replace(tzinfo=timezone.utc)
            return dt.isoformat().replace("+00:00", "Z")
        timestamp = str(value or "").strip()
        if not timestamp:
            raise ValueError("timestamp is required")
        return timestamp


@dataclass(frozen=True)
class MiningEvent:
    """Raw mined event that does not need to be a graph edge."""

    event_type: str
    actor_login: str
    target_login: str
    source_kind: str
    source_id: str
    timestamp: str
    state: str = ""

    ALLOWED_EVENT_TYPES: ClassVar[set[str]] = {
        "issue_comment",
        "issue_closed",
        "pr_opened",
        "pr_comment",
        "pr_review",
        "pr_approval",
        "pr_merged",
    }

    def __post_init__(self) -> None:
        event_type = str(self.event_type).strip()
        if event_type not in self.ALLOWED_EVENT_TYPES:
            raise ValueError(f"Invalid mining event type: {event_type}")
        actor_login = Interaction._normalize_login(self.actor_login, "actor_login")

        object.__setattr__(self, "event_type", event_type)
        object.__setattr__(self, "actor_login", actor_login)
        object.__setattr__(self, "target_login", str(self.target_login or "").strip())
        object.__setattr__(self, "source_kind", str(self.source_kind or "").strip())
        object.__setattr__(self, "source_id", str(self.source_id).strip())
        object.__setattr__(self, "timestamp", Interaction._normalize_timestamp(self.timestamp))
        object.__setattr__(self, "state", str(self.state or "").strip())

    def to_row(self) -> dict[str, Any]:
        """Return the CSV row for raw mining events."""

        return {
            "event_type": self.event_type,
            "actor_login": self.actor_login,
            "target_login": self.target_login,
            "source_kind": self.source_kind,
            "source_id": self.source_id,
            "timestamp": self.timestamp,
            "state": self.state,
        }
