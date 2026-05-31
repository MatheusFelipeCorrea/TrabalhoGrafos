from __future__ import annotations

import argparse
from pathlib import Path

from src.mining.data_exporter import DataExporter, users_from_interactions
from src.mining.github_client import GitHubClient
from src.mining.issue_miner import IssueMiner
from src.mining.pr_miner import PRMiner


DEFAULT_REPOSITORY = "github/spec-kit"
DEFAULT_OUTPUT_DIR = Path("data/raw")


def run_mining(repo: str = DEFAULT_REPOSITORY, output_dir: Path = DEFAULT_OUTPUT_DIR) -> tuple[str, str, str]:
    client = GitHubClient()
    issue_miner = IssueMiner(client)
    pr_miner = PRMiner(client)
    interactions = issue_miner.mine(repo)
    interactions.extend(pr_miner.mine(repo))
    events = issue_miner.events + pr_miner.events

    exporter = DataExporter()
    users_path = output_dir / "users.csv"
    interactions_path = output_dir / "interactions.csv"
    events_path = output_dir / "events.csv"
    exporter.export_users_csv(users_from_interactions(interactions, events), str(users_path))
    exporter.export_interactions_csv(interactions, str(interactions_path))
    exporter.export_events_csv(events, str(events_path))
    print(
        "Issue scan: "
        f"{issue_miner.stats['scanned_items']} issue-API items, "
        f"{issue_miner.stats['mined_issues']} real issues, "
        f"{issue_miner.stats['skipped_pull_requests']} pull requests skipped"
    )
    return str(users_path), str(interactions_path), str(events_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GitHub graph analyzer")
    parser.add_argument("--mine", action="store_true", help="Run GitHub mining")
    parser.add_argument("--repo", default=DEFAULT_REPOSITORY, help="Repository to mine, in owner/name format")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for raw CSV outputs")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.mine:
        users_path, interactions_path, events_path = run_mining(args.repo, Path(args.output_dir))
        print(f"Mining complete: {users_path} {interactions_path} {events_path}")
    else:
        build_parser().print_help()


if __name__ == "__main__":
    main()
