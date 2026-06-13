from __future__ import annotations

from typing import Any

from tqdm import tqdm

from src.mining.github_client import GitHubClient
from src.mining.interaction_model import Interaction, MiningEvent


class IssueMiner:
    """Mine issue comments and close events from a GitHub repository."""

    def __init__(self, client: GitHubClient) -> None:
        self.client = client
        self.events: list[MiningEvent] = []
        self.processed_issue_ids: set[str] = set()
        self.stats = {
            "scanned_items": 0,
            "mined_issues": 0,
            "skipped_pull_requests": 0,
            "skipped_cached_issues": 0,
        }

    def mine(self, repo_full_name: str, processed_issue_ids: set[str] | None = None) -> list[Interaction]:
        self.events = []
        self.processed_issue_ids = set()
        cached_issue_ids = processed_issue_ids or set()
        self.stats = {
            "scanned_items": 0,
            "mined_issues": 0,
            "skipped_pull_requests": 0,
            "skipped_cached_issues": 0,
        }
        repo = self.client.get_repo(repo_full_name)
        issues = self.client.request_with_retry(
            "list_issues",
            lambda: repo.get_issues(state="all"),
        )
        interactions: list[Interaction] = []
        for issue in tqdm(issues, desc="Scanning issues API", unit="item"):
            self.stats["scanned_items"] += 1
            if getattr(issue, "pull_request", None):
                self.stats["skipped_pull_requests"] += 1
                continue
            issue_id = str(issue.number)
            if issue_id in cached_issue_ids:
                self.stats["skipped_cached_issues"] += 1
                continue
            self.stats["mined_issues"] += 1
            self.processed_issue_ids.add(issue_id)
            interactions.extend(self._extract_issue_interactions(issue))
        return interactions

    def _extract_issue_interactions(self, issue: Any) -> list[Interaction]:
        author = self._login(getattr(issue, "user", None))
        if not author:
            return []

        interactions: list[Interaction] = []
        comments = self.client.request_with_retry(
            f"issue_{getattr(issue, 'number', 'unknown')}_comments",
            issue.get_comments,
        )
        for comment in comments:
            commenter = self._login(getattr(comment, "user", None))
            created_at = getattr(comment, "created_at", None)
            if commenter:
                self.events.append(
                    MiningEvent("issue_comment", commenter, author, "issue", str(issue.number), created_at)
                )
            if not self._should_skip_self_interaction(commenter, author):
                interactions.append(
                    Interaction(commenter, author, "comment_issue", 2, created_at, str(issue.number))
                )
            if not self._should_skip_self_interaction(author, commenter):
                interactions.append(
                    Interaction(author, commenter, "open_issue_commented", 3, created_at, str(issue.number))
                )

        events = self.client.request_with_retry(
            f"issue_{getattr(issue, 'number', 'unknown')}_events",
            issue.get_events,
        )
        for event in events:
            if getattr(event, "event", "") != "closed":
                continue
            actor = self._login(getattr(event, "actor", None))
            if actor:
                self.events.append(
                    MiningEvent("issue_closed", actor, author, "issue", str(issue.number), getattr(event, "created_at", None))
                )
            if not self._should_skip_self_interaction(actor, author):
                interactions.append(
                    Interaction(actor, author, "close_issue", 3, getattr(event, "created_at", None), str(issue.number))
                )
        return interactions

    def _should_skip_self_interaction(self, src_login: str, dst_login: str) -> bool:
        return not src_login or not dst_login or src_login == dst_login

    @staticmethod
    def _login(user: Any) -> str:
        return str(getattr(user, "login", "") or "").strip()
