
from __future__ import annotations

import logging
import os
import random
import time
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from dotenv import load_dotenv

try:
    from github import Github, GithubException, RateLimitExceededException
except ImportError:  # pragma: no cover - exercised only when deps are missing.
    Github = None  # type: ignore[assignment]
    GithubException = Exception  # type: ignore[misc,assignment]
    RateLimitExceededException = Exception  # type: ignore[misc,assignment]


logger = logging.getLogger(__name__)


class GitHubClient:
    """Authenticated PyGithub facade with retry and rate-limit handling."""

    def __init__(self, token: str | None = None, sleep: Callable[[float], None] = time.sleep) -> None:
        load_dotenv()
        if Github is None:
            raise RuntimeError("PyGithub is required. Install dependencies with: pip install -r requirements.txt")
        self.token = token if token is not None else os.getenv("GITHUB_TOKEN", "")
        self.github = Github(self.token) if self.token else Github()
        self._sleep = sleep

    def get_repo(self, full_name: str) -> Any:
        """Return a GitHub repository by owner/name."""

        repo_name = str(full_name or "").strip()
        if "/" not in repo_name:
            raise ValueError("Repository name must use the 'owner/name' format")
        return self.request_with_retry("get_repo", lambda: self.github.get_repo(repo_name))

    def request_with_retry(
        self,
        op_name: str,
        operation: Callable[[], Any],
        max_retries: int = 5,
        base_delay: float = 0.5,
    ) -> Any:
        """Run an API operation with exponential backoff and jitter."""

        attempts = max_retries + 1
        for attempt in range(attempts):
            try:
                return operation()
            except Exception as error:
                if not self._is_retryable_error(error) or attempt == max_retries:
                    raise

                delay = self._rate_limit_delay(error)
                if delay is None:
                    delay = base_delay * (2**attempt) + random.uniform(0, base_delay)
                logger.warning("Retrying GitHub operation %s after %.2fs: %s", op_name, delay, error)
                self._sleep(delay)
        raise RuntimeError(f"GitHub operation failed unexpectedly: {op_name}")

    def _is_retryable_error(self, error: Exception) -> bool:
        """Return true for GitHub/network failures that can safely be retried."""

        if isinstance(error, RateLimitExceededException):
            return True
        status = getattr(error, "status", None)
        if status in {403, 429, 500, 502, 503, 504}:
            return True
        return isinstance(error, (TimeoutError, ConnectionError))

    def _rate_limit_delay(self, error: Exception) -> float | None:
        reset_epoch = None
        headers = getattr(error, "headers", {}) or {}
        if str(headers.get("x-ratelimit-remaining", "")) == "0":
            reset_epoch = headers.get("x-ratelimit-reset")

        if reset_epoch is None and isinstance(error, RateLimitExceededException):
            try:
                rate_limit = self.github.get_rate_limit()
                reset_at = rate_limit.core.reset
                if isinstance(reset_at, datetime):
                    reset_epoch = reset_at.replace(tzinfo=timezone.utc).timestamp()
            except Exception:
                reset_epoch = None

        if reset_epoch is None:
            return None
        return max(0.0, float(reset_epoch) - time.time()) + 1.0
