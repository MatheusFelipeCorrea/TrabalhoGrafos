from __future__ import annotations

from typing import Any

from tqdm import tqdm

from src.mining.github_client import GitHubClient
from src.mining.interaction_model import Interaction, MiningEvent


class PRMiner:
    """Mine pull request comments, reviews and merge interactions."""

    def __init__(self, client: GitHubClient) -> None:
        self.client = client
        self.events: list[MiningEvent] = []

    def mine(self, repo_full_name: str) -> list[Interaction]:
        self.events = []
        repo = self.client.get_repo(repo_full_name)
        pulls = self.client.request_with_retry("list_pulls", lambda: repo.get_pulls(state="all"))
        interactions: list[Interaction] = []
        for pr in tqdm(pulls, desc="Mining PRs", unit="pr"):
            interactions.extend(self._extract_pr_interactions(pr))
        return interactions

    def _extract_pr_interactions(self, pr: Any) -> list[Interaction]:
        author = self._login(getattr(pr, "user", None))
        if not author:
            return []

        interactions: list[Interaction] = []
        self.events.append(
            MiningEvent("pr_opened", author, "", "pull_request", str(pr.number), getattr(pr, "created_at", None))
        )
        for comment in self.client.request_with_retry(f"pr_{pr.number}_comments", pr.get_issue_comments):
            commenter = self._login(getattr(comment, "user", None))
            if commenter:
                self.events.append(
                    MiningEvent("pr_comment", commenter, author, "pull_request", str(pr.number), getattr(comment, "created_at", None))
                )
            if not self._should_skip_self_interaction(commenter, author):
                interactions.append(
                    Interaction(commenter, author, "comment_pr", 2, getattr(comment, "created_at", None), str(pr.number))
                )

        for comment in self.client.request_with_retry(f"pr_{pr.number}_review_comments", pr.get_review_comments):
            commenter = self._login(getattr(comment, "user", None))
            if commenter:
                self.events.append(
                    MiningEvent("pr_comment", commenter, author, "pull_request", str(pr.number), getattr(comment, "created_at", None))
                )
            if not self._should_skip_self_interaction(commenter, author):
                interactions.append(
                    Interaction(commenter, author, "comment_pr", 2, getattr(comment, "created_at", None), str(pr.number))
                )

        for review in self.client.request_with_retry(f"pr_{pr.number}_reviews", pr.get_reviews):
            review_type = self._map_review_type(getattr(review, "state", ""))
            reviewer = self._login(getattr(review, "user", None))
            review_state = str(getattr(review, "state", "") or "").upper()
            if reviewer and review_type:
                event_type = "pr_approval" if review_state == "APPROVED" else "pr_review"
                self.events.append(
                    MiningEvent(
                        event_type,
                        reviewer,
                        author,
                        "pull_request",
                        str(pr.number),
                        getattr(review, "submitted_at", None),
                        review_state,
                    )
                )
            if review_type and not self._should_skip_self_interaction(reviewer, author):
                interactions.append(
                    Interaction(reviewer, author, review_type, 4, getattr(review, "submitted_at", None), str(pr.number))
                )

        merged_by = self._login(getattr(pr, "merged_by", None))
        if getattr(pr, "merged", False) and merged_by:
            self.events.append(
                MiningEvent("pr_merged", merged_by, author, "pull_request", str(pr.number), getattr(pr, "merged_at", None))
            )
        if getattr(pr, "merged", False) and not self._should_skip_self_interaction(merged_by, author):
            interactions.append(
                Interaction(merged_by, author, "merge_pr", 5, getattr(pr, "merged_at", None), str(pr.number))
            )
        return interactions

    def _map_review_type(self, review_state: str) -> str:
        return "review_pr" if str(review_state).upper() in {"APPROVED", "CHANGES_REQUESTED", "COMMENTED"} else ""

    @staticmethod
    def _should_skip_self_interaction(src_login: str, dst_login: str) -> bool:
        return not src_login or not dst_login or src_login == dst_login

    @staticmethod
    def _login(user: Any) -> str:
        return str(getattr(user, "login", "") or "").strip()
