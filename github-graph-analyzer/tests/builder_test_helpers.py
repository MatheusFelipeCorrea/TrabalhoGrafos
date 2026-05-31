from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.mining.data_exporter import DataExporter


def write_users_csv(path: Path, logins: list[str]) -> Path:
    rows = [{"login": login, "user_id": "", "name": ""} for login in logins]
    frame = pd.DataFrame(rows, columns=DataExporter.USER_COLUMNS)
    frame.to_csv(path, index=False)
    return path


def write_interactions_csv(path: Path, rows: list[dict[str, object]]) -> Path:
    frame = pd.DataFrame(rows, columns=DataExporter.INTERACTION_COLUMNS)
    frame.to_csv(path, index=False)
    return path


SAMPLE_INTERACTIONS: list[dict[str, object]] = [
    {
        "src_login": "alice",
        "dst_login": "bob",
        "type": "comment_issue",
        "weight": 2,
        "timestamp": "2026-01-01T10:00:00Z",
        "source_id": "1",
    },
    {
        "src_login": "alice",
        "dst_login": "bob",
        "type": "comment_issue",
        "weight": 2,
        "timestamp": "2026-01-02T10:00:00Z",
        "source_id": "2",
    },
    {
        "src_login": "carol",
        "dst_login": "bob",
        "type": "close_issue",
        "weight": 3,
        "timestamp": "2026-01-03T10:00:00Z",
        "source_id": "3",
    },
    {
        "src_login": "dave",
        "dst_login": "bob",
        "type": "review_pr",
        "weight": 4,
        "timestamp": "2026-01-04T10:00:00Z",
        "source_id": "4",
    },
    {
        "src_login": "erin",
        "dst_login": "bob",
        "type": "merge_pr",
        "weight": 5,
        "timestamp": "2026-01-05T10:00:00Z",
        "source_id": "5",
    },
    {
        "src_login": "bob",
        "dst_login": "alice",
        "type": "open_issue_commented",
        "weight": 3,
        "timestamp": "2026-01-06T10:00:00Z",
        "source_id": "6",
    },
]
