from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from src.builder.graph1_comments_builder import Graph1CommentsBuilder
from src.builder.graph2_closures_builder import Graph2ClosuresBuilder
from src.builder.graph3_reviews_builder import Graph3ReviewsBuilder
from src.builder.graph4_integrated_builder import Graph4IntegratedBuilder


DEFAULT_REPOSITORY = "github/spec-kit"
DEFAULT_OUTPUT_DIR = Path("data/raw")
DEFAULT_GRAPH_OUTPUT_DIR = Path("output/graphs")
DEFAULT_REPORT_OUTPUT_DIR = Path("output/reports")


def run_mining(repo: str = DEFAULT_REPOSITORY, output_dir: Path = DEFAULT_OUTPUT_DIR) -> tuple[str, str, str]:
    from src.mining.data_exporter import DataExporter, users_from_interactions
    from src.mining.github_client import GitHubClient
    from src.mining.issue_miner import IssueMiner
    from src.mining.pr_miner import PRMiner

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


def run_build(
    users_csv: Path = DEFAULT_OUTPUT_DIR / "users.csv",
    interactions_csv: Path = DEFAULT_OUTPUT_DIR / "interactions.csv",
    output_dir: Path = DEFAULT_GRAPH_OUTPUT_DIR,
) -> list[str]:
    """Constrói os grafos G1..G4 a partir dos CSVs minerados e exporta arquivos GEXF (grafo lista primeiro)."""

    output_dir.mkdir(parents=True, exist_ok=True)
    builders = [
        Graph1CommentsBuilder(),
        Graph2ClosuresBuilder(),
        Graph3ReviewsBuilder(),
        Graph4IntegratedBuilder(),
    ]
    written_paths: list[str] = []
    for builder in builders:
        destination = output_dir / builder.OUTPUT_GEXF
        _, _, path = builder.build_and_export(
            str(interactions_csv),
            str(users_csv),
            str(destination),
        )
        written_paths.append(path)
        print(f"Built {builder.__class__.__name__}: {path}")
    return written_paths


def run_analysis(
    users_csv: Path = DEFAULT_OUTPUT_DIR / "users.csv",
    interactions_csv: Path = DEFAULT_OUTPUT_DIR / "interactions.csv",
    output_dir: Path = DEFAULT_REPORT_OUTPUT_DIR,
) -> list[str]:
    """Executa todas as métricas de análise nos quatro grafos e exporta relatórios."""

    from src.analysis.centrality import (
        betweenness_centrality,
        closeness_centrality,
        degree_centrality,
        pagerank,
    )
    from src.analysis.community import bridging_ties, detect_communities, modularity
    from src.analysis.structure import clustering_coefficient, degree_assortativity, density

    output_dir.mkdir(parents=True, exist_ok=True)

    builders = [
        ("G1", Graph1CommentsBuilder()),
        ("G2", Graph2ClosuresBuilder()),
        ("G3", Graph3ReviewsBuilder()),
        ("G4", Graph4IntegratedBuilder()),
    ]

    centrality_rows: list[dict[str, object]] = []
    structure_data: dict[str, object] = {}
    community_rows: list[dict[str, object]] = []

    for graph_name, builder in builders:
        print(f"Analyzing {graph_name}...")
        graph, registry = builder.build(str(interactions_csv), str(users_csv))

        # Centralidade
        dc = degree_centrality(graph)
        bc = betweenness_centrality(graph)
        cc = closeness_centrality(graph)
        pr = pagerank(graph)

        for vertex in range(graph.get_vertex_count()):
            login = registry.get_login(vertex)
            centrality_rows.append({
                "login": login,
                "graph": graph_name,
                "degree_in": round(dc[vertex]["in"], 6),
                "degree_out": round(dc[vertex]["out"], 6),
                "betweenness": round(bc[vertex], 6),
                "closeness": round(cc[vertex], 6),
                "pagerank": round(pr[vertex], 6),
            })

        # Estrutura
        d = density(graph)
        cc_coeff = clustering_coefficient(graph)
        assort = degree_assortativity(graph)

        structure_data[graph_name] = {
            "density": round(d, 6),
            "clustering_coefficient_global": round(cc_coeff["global"], 6),
            "clustering_coefficient_local": {
                registry.get_login(vertex): round(value, 6)
                for vertex, value in cc_coeff["local"].items()
            },
            "degree_assortativity": round(assort, 6),
        }

        # Comunidades
        partition = detect_communities(graph)
        mod = modularity(graph, partition)
        bridges = bridging_ties(graph, partition)

        for vertex in range(graph.get_vertex_count()):
            login = registry.get_login(vertex)
            community_rows.append({
                "login": login,
                "community_id": partition.get(vertex, vertex),
                "graph": graph_name,
            })

        structure_data[graph_name]["modularity"] = round(mod, 6)
        structure_data[graph_name]["num_communities"] = len(set(partition.values()))
        structure_data[graph_name]["num_bridging_ties"] = len(bridges)

        print(
            f"  {graph_name}: {graph.get_vertex_count()} vertices, "
            f"{graph.get_edge_count()} edges, "
            f"density={d:.4f}, "
            f"communities={len(set(partition.values()))}, "
            f"modularity={mod:.4f}"
        )

    # Escrita dos relatórios
    written: list[str] = []

    centrality_path = output_dir / "centrality.csv"
    with open(centrality_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["login", "graph", "degree_in", "degree_out", "betweenness", "closeness", "pagerank"],
        )
        writer.writeheader()
        writer.writerows(centrality_rows)
    written.append(str(centrality_path))

    structure_path = output_dir / "structure.json"
    with open(structure_path, "w", encoding="utf-8") as file:
        json.dump(structure_data, file, indent=2, ensure_ascii=False)
    written.append(str(structure_path))

    community_path = output_dir / "communities.csv"
    with open(community_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["login", "community_id", "graph"])
        writer.writeheader()
        writer.writerows(community_rows)
    written.append(str(community_path))

    return written


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GitHub graph analyzer")
    parser.add_argument("--mine", action="store_true", help="Executar mineração do GitHub")
    parser.add_argument("--build", action="store_true", help="Construir grafos G1..G4 a partir dos CSVs minerados")
    parser.add_argument("--analyze", action="store_true", help="Executar métricas de análise nos grafos construídos")
    parser.add_argument("--all", action="store_true", help="Executar pipeline completo: mineração → construção → análise")
    parser.add_argument("--repo", default=DEFAULT_REPOSITORY, help="Repositório para minerar, no formato dono/nome")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Diretório para saídas CSV brutas")
    parser.add_argument(
        "--graph-output-dir",
        default=str(DEFAULT_GRAPH_OUTPUT_DIR),
        help="Diretório para arquivos .gexf de grafos exportados",
    )
    parser.add_argument(
        "--report-output-dir",
        default=str(DEFAULT_REPORT_OUTPUT_DIR),
        help="Diretório para relatórios de análise",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    raw_dir = Path(args.output_dir)

    if args.all:
        users_path, interactions_path, events_path = run_mining(args.repo, raw_dir)
        print(f"Mining complete: {users_path} {interactions_path} {events_path}")
        written = run_build(
            users_csv=raw_dir / "users.csv",
            interactions_csv=raw_dir / "interactions.csv",
            output_dir=Path(args.graph_output_dir),
        )
        print(f"Build complete: {len(written)} graphs exported")
        reports = run_analysis(
            users_csv=raw_dir / "users.csv",
            interactions_csv=raw_dir / "interactions.csv",
            output_dir=Path(args.report_output_dir),
        )
        print(f"Analysis complete: {len(reports)} reports exported")
    elif args.mine:
        users_path, interactions_path, events_path = run_mining(args.repo, raw_dir)
        print(f"Mining complete: {users_path} {interactions_path} {events_path}")
    elif args.build:
        written = run_build(
            users_csv=raw_dir / "users.csv",
            interactions_csv=raw_dir / "interactions.csv",
            output_dir=Path(args.graph_output_dir),
        )
        print(f"Build complete: {len(written)} graphs exported")
    elif args.analyze:
        reports = run_analysis(
            users_csv=raw_dir / "users.csv",
            interactions_csv=raw_dir / "interactions.csv",
            output_dir=Path(args.report_output_dir),
        )
        print(f"Analysis complete: {len(reports)} reports exported")
    else:
        build_parser().print_help()


if __name__ == "__main__":
    main()
