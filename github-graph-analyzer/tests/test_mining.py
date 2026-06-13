from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pandas as pd
import pytest

from src.mining.data_exporter import DataExporter, users_from_interactions
from src.mining.github_client import GitHubClient
from src.mining.interaction_model import Interaction, MiningEvent
from src.mining.issue_miner import IssueMiner
from src.mining.mining_cache import MiningCache
from src.mining.pr_miner import PRMiner


TS = datetime(2026, 1, 15, 12, 0, tzinfo=timezone.utc)


@dataclass
class User:
    login: str


@dataclass
class Comment:
    user: User
    created_at: datetime = TS


@dataclass
class Event:
    event: str
    actor: User
    created_at: datetime = TS


@dataclass
class Review:
    user: User
    state: str
    submitted_at: datetime = TS


class MockIssue:
    number = 42
    user = User("alice")
    pull_request = None

    def get_comments(self):
        return [Comment(User("bob")), Comment(User("alice"))]

    def get_events(self):
        return [Event("closed", User("carol")), Event("labeled", User("dave"))]


class MockIssueBackedPR:
    number = 43
    user = User("ignored-pr-author")
    pull_request = {"url": "https://api.github.com/repos/github/spec-kit/pulls/43"}

    def get_comments(self):
        raise AssertionError("Pull requests returned by get_issues must be skipped")

    def get_events(self):
        raise AssertionError("Pull requests returned by get_issues must be skipped")


class MockPR:
    number = 87
    user = User("diana")
    created_at = TS
    merged = True
    merged_by = User("erin")
    merged_at = TS

    def get_issue_comments(self):
        return [Comment(User("frank"))]

    def get_review_comments(self):
        return [Comment(User("georgia"))]

    def get_reviews(self):
        return [Review(User("helen"), "APPROVED"), Review(User("diana"), "COMMENTED")]


class MockRepo:
    def get_issues(self, state="all"):
        return [MockIssue(), MockIssueBackedPR()]

    def get_pulls(self, state="all"):
        return [MockPR()]


class MockClient:
    def __init__(self):
        self.repo = MockRepo()

    def get_repo(self, full_name: str):
        assert full_name == "github/spec-kit"
        return self.repo

    def request_with_retry(self, op_name, operation, max_retries=5, base_delay=0.5):
        return operation()


def test_cenario_feliz_mining():
    client = MockClient()

    issue_miner = IssueMiner(client)
    interactions = issue_miner.mine("github/spec-kit")
    pr_miner = PRMiner(client)
    interactions.extend(pr_miner.mine("github/spec-kit"))

    rows = [interaction.to_row() for interaction in interactions]
    event_rows = [event.to_row() for event in issue_miner.events + pr_miner.events]
    assert issue_miner.stats == {
        "scanned_items": 2,
        "mined_issues": 1,
        "skipped_pull_requests": 1,
        "skipped_cached_issues": 0,
    }
    event_types = {row["event_type"] for row in event_rows}
    assert {
        "issue_comment",
        "issue_closed",
        "pr_opened",
        "pr_comment",
        "pr_approval",
        "pr_merged",
    }.issubset(event_types)
    assert {"event_type": "pr_opened", "actor_login": "diana", "target_login": "", "source_kind": "pull_request", "source_id": "87", "timestamp": "2026-01-15T12:00:00Z", "state": ""} in event_rows
    assert {"src_login": "bob", "dst_login": "alice", "type": "comment_issue", "weight": 2, "timestamp": "2026-01-15T12:00:00Z", "source_id": "42"} in rows
    assert {"src_login": "alice", "dst_login": "bob", "type": "open_issue_commented", "weight": 3, "timestamp": "2026-01-15T12:00:00Z", "source_id": "42"} in rows
    assert {"src_login": "carol", "dst_login": "alice", "type": "close_issue", "weight": 3, "timestamp": "2026-01-15T12:00:00Z", "source_id": "42"} in rows
    assert {"src_login": "erin", "dst_login": "diana", "type": "merge_pr", "weight": 5, "timestamp": "2026-01-15T12:00:00Z", "source_id": "87"} in rows
    assert all(row["src_login"] != row["dst_login"] for row in rows)


def test_edge_case_mining():
    with pytest.raises(ValueError, match="Invalid interaction type"):
        Interaction("alice", "bob", "unknown", 1, TS, "1")

    with pytest.raises(ValueError, match="Self interactions"):
        Interaction("alice", "alice", "comment_issue", 1, TS, "1")

    with pytest.raises(ValueError, match="weight must be positive"):
        Interaction("alice", "bob", "comment_issue", 0, TS, "1")

    with pytest.raises(ValueError, match="src_login is required"):
        Interaction("", "bob", "comment_issue", 1, TS, "1")

    with pytest.raises(ValueError, match="timestamp is required"):
        Interaction("alice", "bob", "comment_issue", 1, "", "1")

    with pytest.raises(ValueError, match="Invalid mining event type"):
        MiningEvent("unknown", "alice", "bob", "issue", "1", TS)

    miner = IssueMiner(MockClient())
    assert miner._should_skip_self_interaction("alice", "alice")
    assert miner._should_skip_self_interaction("", "alice")


def test_resiliencia_retry_rate_limit(monkeypatch):
    sleeps = []
    attempts = {"count": 0}
    client = GitHubClient.__new__(GitHubClient)
    client._sleep = sleeps.append
    client.github = object()

    class RetryableError(Exception):
        status = 503
        headers = {}

    def operation():
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise RetryableError("temporary unavailable")
        return "ok"

    monkeypatch.setattr("src.mining.github_client.random.uniform", lambda _start, _end: 0)
    assert client.request_with_retry("temporary", operation, max_retries=2, base_delay=0.1) == "ok"
    assert attempts["count"] == 2
    assert sleeps == [0.1]


def test_github_client_carrega_token_e_busca_repo(monkeypatch):
    created_tokens = []

    class FakeGithub:
        def __init__(self, token=None):
            created_tokens.append(token)

        def get_repo(self, full_name):
            return {"full_name": full_name}

    monkeypatch.setenv("GITHUB_TOKEN", "token-from-env")
    monkeypatch.setattr("src.mining.github_client.Github", FakeGithub)

    client = GitHubClient()

    assert created_tokens == ["token-from-env"]
    assert client.get_repo("github/spec-kit") == {"full_name": "github/spec-kit"}


def test_github_client_falhas_nao_retornaveis_e_retry_exaurido():
    client = GitHubClient.__new__(GitHubClient)
    client._sleep = lambda _delay: None
    client.github = object()

    assert client._is_retryable_error(TimeoutError())
    assert not client._is_retryable_error(ValueError("bad input"))

    class PermanentError(Exception):
        status = 404
        headers = {}

    class TemporaryError(Exception):
        status = 503
        headers = {}

    with pytest.raises(PermanentError):
        client.request_with_retry("permanent", lambda: (_ for _ in ()).throw(PermanentError()), max_retries=2)

    with pytest.raises(TemporaryError):
        client.request_with_retry("temporary", lambda: (_ for _ in ()).throw(TemporaryError()), max_retries=1)


def test_rate_limit_delay_por_headers(monkeypatch):
    client = GitHubClient.__new__(GitHubClient)
    monkeypatch.setattr("src.mining.github_client.time.time", lambda: 100.0)

    class LimitedError(Exception):
        headers = {"x-ratelimit-remaining": "0", "x-ratelimit-reset": "109"}

    assert client._rate_limit_delay(LimitedError()) == 10.0


def test_exportacao_csv_idempotente(tmp_path):
    interactions = [
        Interaction("bob", "alice", "comment_issue", 2, TS, "42"),
        Interaction("bob", "alice", "comment_issue", 2, TS, "42"),
        Interaction("carol", "alice", "close_issue", 3, TS, "42"),
    ]
    exporter = DataExporter()

    users_path = tmp_path / "users.csv"
    interactions_path = tmp_path / "interactions.csv"
    events_path = tmp_path / "events.csv"
    exporter.export_users_csv(users_from_interactions(interactions), str(users_path))
    exporter.export_interactions_csv(interactions, str(interactions_path))
    exporter.export_events_csv(
        [
            MiningEvent("issue_comment", "bob", "alice", "issue", "42", TS),
            MiningEvent("issue_comment", "bob", "alice", "issue", "42", TS),
            MiningEvent("pr_opened", "diana", "", "pull_request", "87", TS),
        ],
        str(events_path),
    )

    users = pd.read_csv(users_path)
    exported = pd.read_csv(interactions_path)
    events = pd.read_csv(events_path)
    assert list(users.columns) == ["login", "user_id", "name"]
    assert list(exported.columns) == ["src_login", "dst_login", "type", "weight", "timestamp", "source_id"]
    assert list(events.columns) == ["event_type", "actor_login", "target_login", "source_kind", "source_id", "timestamp", "state"]
    assert users["login"].tolist() == ["alice", "bob", "carol"]
    assert len(exported) == 2
    assert len(events) == 2


def test_mineracao_incremental_pula_ids_processados():
    client = MockClient()

    issue_miner = IssueMiner(client)
    issue_interactions = issue_miner.mine("github/spec-kit", processed_issue_ids={"42"})
    pr_miner = PRMiner(client)
    pr_interactions = pr_miner.mine("github/spec-kit", processed_pull_request_ids={"87"})

    assert issue_interactions == []
    assert issue_miner.events == []
    assert issue_miner.processed_issue_ids == set()
    assert issue_miner.stats == {
        "scanned_items": 2,
        "mined_issues": 0,
        "skipped_pull_requests": 1,
        "skipped_cached_issues": 1,
    }
    assert pr_interactions == []
    assert pr_miner.events == []
    assert pr_miner.processed_pull_request_ids == set()
    assert pr_miner.stats == {
        "scanned_pull_requests": 1,
        "mined_pull_requests": 0,
        "skipped_cached_pull_requests": 1,
    }


def test_cache_inferido_dos_csvs_existentes(tmp_path):
    exporter = DataExporter()
    interactions_path = tmp_path / "interactions.csv"
    events_path = tmp_path / "events.csv"
    cache_path = tmp_path / "mining_cache.json"
    interactions = [
        Interaction("bob", "alice", "comment_issue", 2, TS, "42"),
        Interaction("erin", "diana", "merge_pr", 5, TS, "87"),
    ]
    events = [
        MiningEvent("issue_comment", "bob", "alice", "issue", "42", TS),
        MiningEvent("pr_opened", "diana", "", "pull_request", "87", TS),
    ]
    exporter.export_interactions_csv(interactions, str(interactions_path))
    exporter.export_events_csv(events, str(events_path))

    cache = MiningCache.load(cache_path, tmp_path, "github/spec-kit")

    assert cache.processed_issues == {"42"}
    assert cache.processed_pull_requests == {"87"}
    assert exporter.load_interactions_csv(str(interactions_path)) == interactions
    assert exporter.load_events_csv(str(events_path)) == events

    cache.mark_issues({"100"})
    cache.mark_pull_requests({"101"})
    cache.save(cache_path)
    reloaded = MiningCache.load(cache_path, tmp_path, "github/spec-kit")
    assert reloaded.processed_issues == {"42", "100"}
    assert reloaded.processed_pull_requests == {"87", "101"}


def test_get_repo_valida_formato():
    client = GitHubClient.__new__(GitHubClient)
    with pytest.raises(ValueError, match="owner/name"):
        client.get_repo("spec-kit")


def test_github_client_sem_token_usa_github_anonimo(monkeypatch):
    created: list[str | None] = []

    class FakeGithub:
        def __init__(self, token=None):
            created.append(token)

        def get_repo(self, full_name):
            return {"full_name": full_name}

    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setattr("src.mining.github_client.Github", FakeGithub)

    client = GitHubClient(token="")

    assert created == [None]
    assert client.get_repo("github/spec-kit") == {"full_name": "github/spec-kit"}


def test_github_client_exige_pygithub(monkeypatch):
    monkeypatch.setattr("src.mining.github_client.Github", None)
    with pytest.raises(RuntimeError, match="PyGithub is required"):
        GitHubClient()


def test_github_client_retry_status_codes_e_rate_limit():
    from github import RateLimitExceededException

    client = GitHubClient.__new__(GitHubClient)
    client._sleep = lambda _delay: None
    client.github = object()

    class ForbiddenError(Exception):
        status = 403
        headers = {}

    class TooManyRequests(Exception):
        status = 429
        headers = {}

    assert client._is_retryable_error(RateLimitExceededException(403, {}, None))
    assert client._is_retryable_error(ForbiddenError())
    assert client._is_retryable_error(TooManyRequests())
    assert client._is_retryable_error(ConnectionError())


def test_rate_limit_delay_via_get_rate_limit(monkeypatch):
    from github import RateLimitExceededException

    client = GitHubClient.__new__(GitHubClient)
    client.github = MagicMock()
    client.github.get_rate_limit.return_value.core.reset = datetime(1970, 1, 1, 0, 2, tzinfo=timezone.utc)
    monkeypatch.setattr("src.mining.github_client.time.time", lambda: 0.0)

    delay = client._rate_limit_delay(RateLimitExceededException(403, {}, None))
    assert delay == pytest.approx(121.0)


def test_rate_limit_delay_ignora_falha_em_get_rate_limit():
    from github import RateLimitExceededException

    client = GitHubClient.__new__(GitHubClient)
    client.github = MagicMock()
    client.github.get_rate_limit.side_effect = RuntimeError("api unavailable")

    assert client._rate_limit_delay(RateLimitExceededException(403, {}, None)) is None


def test_request_with_retry_falha_inesperada_sem_tentativas():
    client = GitHubClient.__new__(GitHubClient)
    client._sleep = lambda _delay: None
    client.github = object()

    with pytest.raises(RuntimeError, match="failed unexpectedly"):
        client.request_with_retry("noop", lambda: "ok", max_retries=-1)


def test_users_from_interactions_inclui_eventos():
    interactions = [Interaction("bob", "alice", "comment_issue", 2, TS, "42")]
    events = [MiningEvent("issue_comment", "bob", "alice", "issue", "42", TS)]
    users = users_from_interactions(interactions, events)
    assert {row["login"] for row in users} == {"alice", "bob"}


def test_issue_sem_autor_ignorada():
    class IssueWithoutAuthor:
        number = 99
        user = None
        pull_request = None

        def get_comments(self):
            return []

        def get_events(self):
            return []

    class RepoWithAnonymousIssue:
        def get_issues(self, state="all"):
            return [IssueWithoutAuthor()]

    class Client:
        def get_repo(self, full_name):
            return RepoWithAnonymousIssue()

        def request_with_retry(self, op_name, operation, max_retries=5, base_delay=0.5):
            return operation()

    miner = IssueMiner(Client())
    assert miner.mine("github/spec-kit") == []


def test_pr_sem_autor_ignorado():
    class PRWithoutAuthor:
        number = 100
        user = None
        created_at = TS
        merged = False
        merged_by = None

        def get_issue_comments(self):
            return []

        def get_review_comments(self):
            return []

        def get_reviews(self):
            return []

    class RepoWithAnonymousPR:
        def get_pulls(self, state="all"):
            return [PRWithoutAuthor()]

    class Client:
        def get_repo(self, full_name):
            return RepoWithAnonymousPR()

        def request_with_retry(self, op_name, operation, max_retries=5, base_delay=0.5):
            return operation()

    miner = PRMiner(Client())
    assert miner.mine("github/spec-kit") == []
