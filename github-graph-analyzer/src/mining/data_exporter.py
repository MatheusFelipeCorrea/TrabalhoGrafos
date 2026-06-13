from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.mining.interaction_model import Interaction, MiningEvent


class DataExporter:
    """Persist mined users and interactions as idempotent CSV files."""

    USER_COLUMNS = ["login", "user_id", "name"]
    INTERACTION_COLUMNS = ["src_login", "dst_login", "type", "weight", "timestamp", "source_id"]
    EVENT_COLUMNS = ["event_type", "actor_login", "target_login", "source_kind", "source_id", "timestamp", "state"]

    def export_users_csv(self, users: list[dict], output_path: str) -> str:
        self._ensure_output_dir(output_path)
        rows = []
        for user in users:
            login = str(user.get("login", "")).strip()
            if login:
                rows.append(
                    {
                        "login": login,
                        "user_id": user.get("user_id", ""),
                        "name": user.get("name", ""),
                    }
                )
        frame = pd.DataFrame(rows, columns=self.USER_COLUMNS)
        if not frame.empty:
            frame = frame.drop_duplicates(subset=["login"]).sort_values("login")
        frame.to_csv(output_path, index=False)
        return output_path

    def export_interactions_csv(self, interactions: list[Interaction], output_path: str) -> str:
        self._ensure_output_dir(output_path)
        rows = [interaction.to_row() for interaction in interactions]
        frame = pd.DataFrame(rows, columns=self.INTERACTION_COLUMNS)
        if not frame.empty:
            frame = frame.drop_duplicates().sort_values(["source_id", "type", "src_login", "dst_login", "timestamp"])
        frame.to_csv(output_path, index=False)
        return output_path

    def load_interactions_csv(self, input_path: str) -> list[Interaction]:
        path = Path(input_path)
        if not path.exists():
            return []
        frame = pd.read_csv(path, keep_default_na=False)
        if frame.empty:
            return []
        return [
            Interaction(
                row["src_login"],
                row["dst_login"],
                row["type"],
                int(row["weight"]),
                row["timestamp"],
                row["source_id"],
            )
            for _, row in frame.iterrows()
        ]

    def export_events_csv(self, events: list[MiningEvent], output_path: str) -> str:
        self._ensure_output_dir(output_path)
        rows = [event.to_row() for event in events]
        frame = pd.DataFrame(rows, columns=self.EVENT_COLUMNS)
        if not frame.empty:
            frame = frame.drop_duplicates().sort_values(["source_kind", "source_id", "event_type", "timestamp"])
        frame.to_csv(output_path, index=False)
        return output_path

    def load_events_csv(self, input_path: str) -> list[MiningEvent]:
        path = Path(input_path)
        if not path.exists():
            return []
        frame = pd.read_csv(path, keep_default_na=False)
        if frame.empty:
            return []
        return [
            MiningEvent(
                row["event_type"],
                row["actor_login"],
                row["target_login"],
                row["source_kind"],
                row["source_id"],
                row["timestamp"],
                row.get("state", ""),
            )
            for _, row in frame.iterrows()
        ]

    def _ensure_output_dir(self, output_path: str) -> None:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)


def users_from_interactions(
    interactions: list[Interaction],
    events: list[MiningEvent] | None = None,
) -> list[dict[str, str]]:
    """Build the minimal users.csv payload from interactions and raw event actors."""

    logins = sorted({item.src_login for item in interactions} | {item.dst_login for item in interactions})
    if events:
        logins = sorted(set(logins) | {event.actor_login for event in events} | {event.target_login for event in events if event.target_login})
    return [{"login": login, "user_id": "", "name": ""} for login in logins]
