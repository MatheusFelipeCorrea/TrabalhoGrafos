from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd


ISSUE_INTERACTION_TYPES = {"comment_issue", "open_issue_commented", "close_issue"}
PR_INTERACTION_TYPES = {"comment_pr", "review_pr", "merge_pr"}


@dataclass
class MiningCache:
    """Track already processed GitHub issue and pull request numbers."""

    repository: str
    processed_issues: set[str] = field(default_factory=set)
    processed_pull_requests: set[str] = field(default_factory=set)

    @classmethod
    def load(cls, cache_path: Path, output_dir: Path, repository: str) -> "MiningCache":
        cache = cls(repository=repository)
        if cache_path.exists():
            payload = json.loads(cache_path.read_text(encoding="utf-8"))
            if payload.get("repository") == repository:
                cache.processed_issues.update(str(item) for item in payload.get("processed_issues", []))
                cache.processed_pull_requests.update(
                    str(item) for item in payload.get("processed_pull_requests", [])
                )

        cache._hydrate_from_existing_csvs(output_dir)
        return cache

    def save(self, cache_path: Path) -> str:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "repository": self.repository,
            "processed_issues": sorted(self.processed_issues, key=self._sort_key),
            "processed_pull_requests": sorted(self.processed_pull_requests, key=self._sort_key),
        }
        cache_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return str(cache_path)

    def mark_issues(self, issue_ids: set[str]) -> None:
        self.processed_issues.update(str(item) for item in issue_ids)

    def mark_pull_requests(self, pull_request_ids: set[str]) -> None:
        self.processed_pull_requests.update(str(item) for item in pull_request_ids)

    def _hydrate_from_existing_csvs(self, output_dir: Path) -> None:
        events_path = output_dir / "events.csv"
        if events_path.exists():
            events = pd.read_csv(events_path, keep_default_na=False)
            if {"source_kind", "source_id"}.issubset(events.columns):
                self.processed_issues.update(
                    str(item) for item in events.loc[events["source_kind"] == "issue", "source_id"]
                )
                self.processed_pull_requests.update(
                    str(item) for item in events.loc[events["source_kind"] == "pull_request", "source_id"]
                )

        interactions_path = output_dir / "interactions.csv"
        if interactions_path.exists():
            interactions = pd.read_csv(interactions_path, keep_default_na=False)
            if {"type", "source_id"}.issubset(interactions.columns):
                self.processed_issues.update(
                    str(item)
                    for item in interactions.loc[interactions["type"].isin(ISSUE_INTERACTION_TYPES), "source_id"]
                )
                self.processed_pull_requests.update(
                    str(item)
                    for item in interactions.loc[interactions["type"].isin(PR_INTERACTION_TYPES), "source_id"]
                )

    @staticmethod
    def _sort_key(value: str) -> tuple[int, int | str]:
        return (0, int(value)) if str(value).isdigit() else (1, str(value))
