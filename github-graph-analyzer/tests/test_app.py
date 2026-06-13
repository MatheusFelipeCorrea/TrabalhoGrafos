from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.app import api_demo
from src.app.main import build_parser, main, run_analysis, run_build, run_mining
from src.graph.adjacency_list_graph import AdjacencyListGraph
from src.mining.interaction_model import Interaction, MiningEvent
from tests.builder_test_helpers import SAMPLE_INTERACTIONS, write_interactions_csv, write_users_csv

TS = datetime(2026, 1, 15, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def synthetic_csv_dir(tmp_path: Path) -> tuple[Path, Path]:
    users_path = write_users_csv(tmp_path / "users.csv", ["alice", "bob", "carol", "dave", "erin"])
    interactions_path = write_interactions_csv(tmp_path / "interactions.csv", SAMPLE_INTERACTIONS)
    return users_path, interactions_path


def test_build_parser_accepts_pipeline_flags() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "--all",
            "--repo",
            "owner/repo",
            "--output-dir",
            "data/raw",
            "--graph-output-dir",
            "output/graphs",
            "--report-output-dir",
            "output/reports",
        ],
    )
    assert args.all is True
    assert args.repo == "owner/repo"
    assert args.output_dir == "data/raw"


def test_run_build_exports_four_graphs(synthetic_csv_dir: tuple[Path, Path], tmp_path: Path) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph_dir = tmp_path / "graphs"
    written = run_build(users_path, interactions_path, graph_dir)
    assert len(written) == 4
    assert all(Path(path).is_file() for path in written)


def test_run_analysis_exports_reports(synthetic_csv_dir: tuple[Path, Path], tmp_path: Path) -> None:
    users_path, interactions_path = synthetic_csv_dir
    report_dir = tmp_path / "reports"
    written = run_analysis(users_path, interactions_path, report_dir)
    assert len(written) == 3
    assert (report_dir / "centrality.csv").is_file()
    assert (report_dir / "structure.json").is_file()
    assert (report_dir / "communities.csv").is_file()


def test_run_mining_writes_csvs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    sample = [Interaction("bob", "alice", "comment_issue", 2, TS, "42")]

    class FakeIssueMiner:
        stats = {"scanned_items": 1, "mined_issues": 1, "skipped_pull_requests": 0}
        events = [MiningEvent("issue_comment", "bob", "alice", "issue", "42", TS)]

        def __init__(self, _client: object) -> None:
            pass

        def mine(self, _repo: str) -> list[Interaction]:
            return list(sample)

    class FakePRMiner:
        events: list[MiningEvent] = []

        def __init__(self, _client: object) -> None:
            pass

        def mine(self, _repo: str) -> list[Interaction]:
            return []

    monkeypatch.setattr("src.mining.github_client.GitHubClient", lambda: object())
    monkeypatch.setattr("src.mining.issue_miner.IssueMiner", FakeIssueMiner)
    monkeypatch.setattr("src.mining.pr_miner.PRMiner", FakePRMiner)

    users_path, interactions_path, events_path = run_mining("github/spec-kit", tmp_path)

    assert Path(users_path).is_file()
    assert Path(interactions_path).is_file()
    assert Path(events_path).is_file()
    assert "Issue scan" in capsys.readouterr().out


def test_main_without_flags_prints_help(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["main"])
    main()
    assert "usage" in capsys.readouterr().out.lower()


def test_main_mine_flag(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["main", "--mine", "--output-dir", str(tmp_path)])
    monkeypatch.setattr(
        "src.app.main.run_mining",
        lambda repo, output_dir: (str(tmp_path / "u.csv"), str(tmp_path / "i.csv"), str(tmp_path / "e.csv")),
    )
    main()
    assert "Mining complete" in capsys.readouterr().out


def test_main_build_flag(
    monkeypatch: pytest.MonkeyPatch,
    synthetic_csv_dir: tuple[Path, Path],
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    users_path, interactions_path = synthetic_csv_dir
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main",
            "--build",
            "--output-dir",
            str(users_path.parent),
            "--graph-output-dir",
            str(tmp_path / "graphs"),
        ],
    )
    main()
    assert "Build complete" in capsys.readouterr().out
    assert len(list((tmp_path / "graphs").glob("*.gexf"))) == 4


def test_main_analyze_flag(
    monkeypatch: pytest.MonkeyPatch,
    synthetic_csv_dir: tuple[Path, Path],
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    users_path, interactions_path = synthetic_csv_dir
    report_dir = tmp_path / "reports"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main",
            "--analyze",
            "--output-dir",
            str(users_path.parent),
            "--report-output-dir",
            str(report_dir),
        ],
    )
    main()
    assert "Analysis complete" in capsys.readouterr().out
    assert (report_dir / "centrality.csv").is_file()


def test_main_all_flag(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    graph_dir = tmp_path / "graphs"
    report_dir = tmp_path / "reports"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main",
            "--all",
            "--output-dir",
            str(tmp_path / "raw"),
            "--graph-output-dir",
            str(graph_dir),
            "--report-output-dir",
            str(report_dir),
        ],
    )
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    users = raw_dir / "users.csv"
    interactions = raw_dir / "interactions.csv"
    events = raw_dir / "events.csv"
    write_users_csv(users, ["alice", "bob", "carol", "dave", "erin"])
    write_interactions_csv(interactions, SAMPLE_INTERACTIONS)
    events.write_text("event_type,actor_login,target_login,source_kind,source_id,timestamp,state\n", encoding="utf-8")
    monkeypatch.setattr(
        "src.app.main.run_mining",
        lambda repo, output_dir: (
            str(users),
            str(interactions),
            str(events),
        ),
    )

    main()
    output = capsys.readouterr().out
    assert "Mining complete" in output
    assert "Build complete" in output
    assert "Analysis complete" in output


def test_api_demo_graph_operations(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.chdir(tmp_path)
    api_demo._demo_graph_operations("DemoGraph", AdjacencyListGraph(3))
    captured = capsys.readouterr().out
    assert "DemoGraph" in captured
    assert "get_vertex_count()" in captured
    assert (tmp_path / "output/demo/graph_demo.gexf").is_file()


def test_api_demo_main(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    def recorder(name: str, graph: object) -> None:
        calls.append(name)

    monkeypatch.setattr(api_demo, "_demo_graph_operations", recorder)
    api_demo.main()
    assert len(calls) == 2
