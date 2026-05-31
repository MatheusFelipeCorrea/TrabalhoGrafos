from __future__ import annotations

from pathlib import Path

import pytest

from src.builder.base_builder import BaseBuilder
from src.builder.exceptions import InvalidCsvError, UnknownIndexError, UnknownLoginError
from src.builder.graph1_comments_builder import Graph1CommentsBuilder
from src.builder.graph2_closures_builder import Graph2ClosuresBuilder
from src.builder.graph3_reviews_builder import Graph3ReviewsBuilder
from src.builder.graph4_integrated_builder import Graph4IntegratedBuilder
from src.builder.interaction_weights import INTERACTION_WEIGHT_BY_TYPE, official_weight
from src.builder.user_registry import UserRegistry
from src.graph.adjacency_list_graph import AdjacencyListGraph
from src.graph.adjacency_matrix_graph import AdjacencyMatrixGraph
from tests.builder_test_helpers import SAMPLE_INTERACTIONS, write_interactions_csv, write_users_csv

GRAPH_FACTORIES = [
    pytest.param(BaseBuilder.list_graph_factory, id="list"),
    pytest.param(BaseBuilder.matrix_graph_factory, id="matrix"),
]

REPO_ROOT = Path(__file__).resolve().parents[1]
MINED_USERS = REPO_ROOT / "data" / "raw" / "users.csv"
MINED_INTERACTIONS = REPO_ROOT / "data" / "raw" / "interactions.csv"


@pytest.fixture
def synthetic_csv_dir(tmp_path: Path) -> tuple[Path, Path]:
    users_path = write_users_csv(tmp_path / "users.csv", ["alice", "bob", "carol", "dave", "erin"])
    interactions_path = write_interactions_csv(tmp_path / "interactions.csv", SAMPLE_INTERACTIONS)
    return users_path, interactions_path


# --- FEAT 3.1 UserRegistry ---


def test_3_1_1_cenario_feliz() -> None:
    registry = UserRegistry()
    assert registry.add_user("alice") == 0
    assert registry.add_user("bob") == 1
    assert registry.get_index("alice") == 0
    assert registry.get_login(1) == "bob"


def test_3_1_1_cenario_alternativo() -> None:
    registry = UserRegistry()
    for login in ("zara", "amy", "mike"):
        registry.add_user(login)
    assert registry.logins() == ["zara", "amy", "mike"]


def test_3_1_1_edge_case() -> None:
    registry = UserRegistry()
    with pytest.raises(UnknownLoginError):
        registry.get_index("missing")
    registry.add_user("alice")
    with pytest.raises(UnknownIndexError):
        registry.get_login(99)


def test_3_1_1_idempotencia_ou_invariante() -> None:
    registry = UserRegistry()
    first = registry.add_user("alice")
    second = registry.add_user("alice")
    assert first == second == 0
    assert len(registry) == 1


def test_3_1_2_cenario_feliz() -> None:
    registry = UserRegistry()
    registry.add_user("bob")
    assert registry.get_index("bob") == 0


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_1_2_cenario_alternativo(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph1CommentsBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    alice = registry.get_index("alice")
    assert graph.get_vertex_label(alice) == "alice"
    assert graph.has_edge(alice, registry.get_index("bob"))


def test_3_1_2_edge_case() -> None:
    with pytest.raises(ValueError, match="login is required"):
        UserRegistry().add_user("  ")


def test_3_1_2_idempotencia_ou_invariante() -> None:
    registry = UserRegistry()
    registry.add_user("a")
    registry.add_user("b")
    assert registry.get_login(registry.get_index("a")) == "a"


def test_3_1_3_cenario_feliz() -> None:
    registry = UserRegistry()
    registry.add_user("carol")
    assert registry.get_login(0) == "carol"


def test_3_1_3_cenario_alternativo() -> None:
    registry = UserRegistry()
    registry.add_user("x")
    registry.add_user("y")
    assert registry.get_login(1) == "y"


def test_3_1_3_edge_case() -> None:
    registry = UserRegistry()
    with pytest.raises(UnknownIndexError):
        registry.get_login(-1)


def test_3_1_3_idempotencia_ou_invariante() -> None:
    registry = UserRegistry()
    index = registry.add_user("login")
    assert registry.get_login(index) == "login"


# --- FEAT 3.2 BaseBuilder ---


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_2_1_cenario_feliz(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph1CommentsBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    assert len(registry) == 5
    assert graph.get_vertex_count() == 5


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_2_1_cenario_alternativo(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, _ = Graph2ClosuresBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    assert graph.get_edge_count() >= 1


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_2_1_edge_case(tmp_path: Path, graph_factory) -> None:
    users_path = write_users_csv(tmp_path / "users.csv", ["alice"])
    interactions_path = write_interactions_csv(
        tmp_path / "interactions.csv",
        [
            {
                "src_login": "alice",
                "dst_login": "bob",
                "type": "comment_issue",
                "weight": 2,
                "timestamp": "2026-01-01T10:00:00Z",
                "source_id": "1",
            }
        ],
    )
    with pytest.raises(InvalidCsvError, match="file does not exist"):
        Graph1CommentsBuilder(graph_factory=graph_factory).build(
            str(interactions_path),
            str(tmp_path / "missing_users.csv"),
        )
    builder = Graph1CommentsBuilder(graph_factory=graph_factory)
    builder._load_users_csv(str(users_path), UserRegistry())
    with pytest.raises(InvalidCsvError, match="Self interactions"):
        builder._load_interactions_csv(
            str(
                write_interactions_csv(
                    tmp_path / "self_loop.csv",
                    [
                        {
                            "src_login": "alice",
                            "dst_login": "alice",
                            "type": "comment_issue",
                            "weight": 2,
                            "timestamp": "2026-01-01T10:00:00Z",
                            "source_id": "9",
                        }
                    ],
                )
            )
        )


def test_3_2_1_edge_case_invalid_interactions(tmp_path: Path) -> None:
    users_path = write_users_csv(tmp_path / "users.csv", ["alice", "bob"])
    bad = tmp_path / "bad.csv"
    bad.write_text("src_login,dst_login,type,weight,timestamp\nalice,bob,comment_issue,2,2026\n", encoding="utf-8")
    with pytest.raises(InvalidCsvError, match="missing columns"):
        Graph1CommentsBuilder().build(str(bad), str(users_path))


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_2_1_idempotencia_ou_invariante(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    first_graph, first_registry = Graph3ReviewsBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    second_graph, second_registry = Graph3ReviewsBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    assert first_registry.logins() == second_registry.logins()
    assert first_graph.get_edge_count() == second_graph.get_edge_count()


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_2_2_cenario_feliz(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    builders = [
        Graph1CommentsBuilder(graph_factory=graph_factory),
        Graph2ClosuresBuilder(graph_factory=graph_factory),
        Graph3ReviewsBuilder(graph_factory=graph_factory),
        Graph4IntegratedBuilder(graph_factory=graph_factory),
    ]
    edge_counts = [builder.build(str(interactions_path), str(users_path))[0].get_edge_count() for builder in builders]
    assert edge_counts[3] >= max(edge_counts[0], edge_counts[1], edge_counts[2])


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_2_2_cenario_alternativo(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph4IntegratedBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    assert isinstance(graph, AdjacencyListGraph if graph_factory is BaseBuilder.list_graph_factory else AdjacencyMatrixGraph)


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_2_2_edge_case(tmp_path: Path, graph_factory) -> None:
    users_path = write_users_csv(tmp_path / "users.csv", ["alice"])
    interactions_path = tmp_path / "interactions.csv"
    interactions_path.write_text("wrong\n1\n", encoding="utf-8")
    with pytest.raises(InvalidCsvError):
        Graph1CommentsBuilder(graph_factory=graph_factory).build(str(interactions_path), str(users_path))


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_2_2_idempotencia_ou_invariante(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph_a, _ = Graph1CommentsBuilder(graph_factory=graph_factory).build(str(interactions_path), str(users_path))
    graph_b, _ = Graph1CommentsBuilder(graph_factory=graph_factory).build(str(interactions_path), str(users_path))
    assert graph_a.get_edge_count() == graph_b.get_edge_count()


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_2_3_cenario_feliz(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph1CommentsBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    alice = registry.get_index("alice")
    bob = registry.get_index("bob")
    assert graph.has_edge(alice, bob)
    assert graph.get_vertex_label(alice) == "alice"


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_2_3_cenario_alternativo(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph4IntegratedBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    assert graph.get_edge_count() > 0
    assert len(registry) >= 4


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_2_3_edge_case(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph1CommentsBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    alice = registry.get_index("alice")
    assert not graph.has_edge(alice, alice)


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_2_3_idempotencia_ou_invariante(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph1CommentsBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    alice = registry.get_index("alice")
    bob = registry.get_index("bob")
    assert graph.get_edge_weight(alice, bob) == 2.0


# --- FEAT 3.3 G1 ---


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_3_1_cenario_feliz(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    rows = Graph1CommentsBuilder(graph_factory=graph_factory)._load_interactions_csv(str(interactions_path))
    filtered = Graph1CommentsBuilder()._filter_interactions(rows)
    assert all(Graph1CommentsBuilder._is_comment_type(str(row["type"])) for row in filtered)
    assert {row["type"] for row in filtered} <= {"comment_issue", "comment_pr"}


def test_3_3_1_cenario_alternativo() -> None:
    assert Graph1CommentsBuilder._is_comment_type("comment_pr")
    assert not Graph1CommentsBuilder._is_comment_type("merge_pr")


def test_3_3_1_edge_case() -> None:
    assert not Graph1CommentsBuilder._is_comment_type("invalid")


def test_3_3_1_idempotencia_ou_invariante() -> None:
    assert Graph1CommentsBuilder._is_comment_type("comment_issue") == Graph1CommentsBuilder._is_comment_type(
        "comment_issue"
    )


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_3_2_cenario_feliz(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph1CommentsBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    assert graph.has_edge(registry.get_index("alice"), registry.get_index("bob"))


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_3_2_cenario_alternativo(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph1CommentsBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    assert not graph.has_edge(registry.get_index("carol"), registry.get_index("bob"))


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_3_2_edge_case(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, _ = Graph1CommentsBuilder(graph_factory=graph_factory).build(str(interactions_path), str(users_path))
    assert graph.get_edge_count() == 1


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_3_2_idempotencia_ou_invariante(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph1CommentsBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    alice, bob = registry.get_index("alice"), registry.get_index("bob")
    assert graph.get_edge_count() == 1
    assert graph.get_edge_weight(alice, bob) == 2.0


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_3_3_cenario_feliz(synthetic_csv_dir: tuple[Path, Path], tmp_path: Path, graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    output = tmp_path / Graph1CommentsBuilder.OUTPUT_GEXF
    _, _, written = Graph1CommentsBuilder(graph_factory=graph_factory).build_and_export(
        str(interactions_path),
        str(users_path),
        str(output),
    )
    assert Path(written).is_file()
    assert "weight" in Path(written).read_text(encoding="utf-8")


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_3_3_cenario_alternativo(synthetic_csv_dir: tuple[Path, Path], tmp_path: Path, graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, _ = Graph1CommentsBuilder(graph_factory=graph_factory).build(str(interactions_path), str(users_path))
    path = tmp_path / "manual.gexf"
    graph.export_to_gephi(str(path))
    assert path.exists()


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_3_3_edge_case(tmp_path: Path, graph_factory) -> None:
    users_path = write_users_csv(tmp_path / "users.csv", ["alice"])
    interactions_path = write_interactions_csv(tmp_path / "interactions.csv", [])
    output = tmp_path / Graph1CommentsBuilder.OUTPUT_GEXF
    _, _, written = Graph1CommentsBuilder(graph_factory=graph_factory).build_and_export(
        str(interactions_path),
        str(users_path),
        str(output),
    )
    assert Path(written).is_file()


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_3_3_idempotencia_ou_invariante(synthetic_csv_dir: tuple[Path, Path], tmp_path: Path, graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    builder = Graph1CommentsBuilder(graph_factory=graph_factory)
    path_a = tmp_path / "a.gexf"
    path_b = tmp_path / "b.gexf"
    graph_a, _, _ = builder.build_and_export(str(interactions_path), str(users_path), str(path_a))
    graph_b, _, _ = builder.build_and_export(str(interactions_path), str(users_path), str(path_b))
    assert graph_a.get_edge_count() == graph_b.get_edge_count()


# --- FEAT 3.4 G2 ---


def test_3_4_1_cenario_feliz() -> None:
    assert Graph2ClosuresBuilder._is_closure_type("close_issue")


def test_3_4_1_cenario_alternativo(synthetic_csv_dir: tuple[Path, Path]) -> None:
    users_path, interactions_path = synthetic_csv_dir
    rows = Graph2ClosuresBuilder()._load_interactions_csv(str(interactions_path))
    filtered = Graph2ClosuresBuilder()._filter_interactions(rows)
    assert len(filtered) == 1


def test_3_4_1_edge_case() -> None:
    assert not Graph2ClosuresBuilder._is_closure_type("comment_issue")


def test_3_4_1_idempotencia_ou_invariante() -> None:
    assert Graph2ClosuresBuilder._is_closure_type("close_issue")


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_4_2_cenario_feliz(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph2ClosuresBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    assert graph.has_edge(registry.get_index("carol"), registry.get_index("bob"))


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_4_2_cenario_alternativo(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph2ClosuresBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    assert not graph.has_edge(registry.get_index("alice"), registry.get_index("bob"))


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_4_2_edge_case(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph2ClosuresBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    assert graph.get_edge_weight(registry.get_index("carol"), registry.get_index("bob")) == 3.0


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_4_2_idempotencia_ou_invariante(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, _ = Graph2ClosuresBuilder(graph_factory=graph_factory).build(str(interactions_path), str(users_path))
    assert graph.get_edge_count() == 1


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_4_3_cenario_feliz(synthetic_csv_dir: tuple[Path, Path], tmp_path: Path, graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    output = tmp_path / Graph2ClosuresBuilder.OUTPUT_GEXF
    _, _, written = Graph2ClosuresBuilder(graph_factory=graph_factory).build_and_export(
        str(interactions_path),
        str(users_path),
        str(output),
    )
    assert Path(written).name == Graph2ClosuresBuilder.OUTPUT_GEXF


def test_3_4_3_cenario_alternativo() -> None:
    assert Graph2ClosuresBuilder.OUTPUT_GEXF.endswith(".gexf")


def test_3_4_3_edge_case(tmp_path: Path) -> None:
    users_path = write_users_csv(tmp_path / "users.csv", ["a", "b"])
    interactions_path = write_interactions_csv(
        tmp_path / "interactions.csv",
        [
            {
                "src_login": "a",
                "dst_login": "b",
                "type": "close_issue",
                "weight": 3,
                "timestamp": "2026-01-01T10:00:00Z",
                "source_id": "1",
            }
        ],
    )
    output = tmp_path / Graph2ClosuresBuilder.OUTPUT_GEXF
    Graph2ClosuresBuilder().build_and_export(str(interactions_path), str(users_path), str(output))
    assert output.exists()


def test_3_4_3_idempotencia_ou_invariante(synthetic_csv_dir: tuple[Path, Path], tmp_path: Path) -> None:
    users_path, interactions_path = synthetic_csv_dir
    path = tmp_path / Graph2ClosuresBuilder.OUTPUT_GEXF
    Graph2ClosuresBuilder().build_and_export(str(interactions_path), str(users_path), str(path))
    assert path.read_text(encoding="utf-8").count("<edge ") >= 1


# --- FEAT 3.5 G3 ---


def test_3_5_1_cenario_feliz() -> None:
    assert Graph3ReviewsBuilder._is_review_type("review_pr")
    assert Graph3ReviewsBuilder._is_review_type("merge_pr")


def test_3_5_1_cenario_alternativo(synthetic_csv_dir: tuple[Path, Path]) -> None:
    users_path, interactions_path = synthetic_csv_dir
    rows = Graph3ReviewsBuilder()._load_interactions_csv(str(interactions_path))
    filtered = Graph3ReviewsBuilder()._filter_interactions(rows)
    assert len(filtered) == 2


def test_3_5_1_edge_case() -> None:
    assert not Graph3ReviewsBuilder._is_review_type("close_issue")


def test_3_5_1_idempotencia_ou_invariante() -> None:
    assert Graph3ReviewsBuilder._is_review_type("merge_pr")


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_5_2_cenario_feliz(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph3ReviewsBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    bob = registry.get_index("bob")
    assert graph.has_edge(registry.get_index("dave"), bob)
    assert graph.has_edge(registry.get_index("erin"), bob)


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_5_2_cenario_alternativo(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph3ReviewsBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    assert not graph.has_edge(registry.get_index("alice"), registry.get_index("bob"))


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_5_2_edge_case(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, _ = Graph3ReviewsBuilder(graph_factory=graph_factory).build(str(interactions_path), str(users_path))
    assert graph.get_edge_count() == 2


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_5_2_idempotencia_ou_invariante(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph3ReviewsBuilder(graph_factory=graph_factory).build(
        str(interactions_path),
        str(users_path),
    )
    assert graph.get_edge_weight(registry.get_index("dave"), registry.get_index("bob")) == 4.0


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_5_3_cenario_feliz(synthetic_csv_dir: tuple[Path, Path], tmp_path: Path, graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    output = tmp_path / Graph3ReviewsBuilder.OUTPUT_GEXF
    Graph3ReviewsBuilder(graph_factory=graph_factory).build_and_export(
        str(interactions_path),
        str(users_path),
        str(output),
    )
    assert output.exists()


def test_3_5_3_cenario_alternativo() -> None:
    assert Graph3ReviewsBuilder.OUTPUT_GEXF == "graph3_reviews.gexf"


def test_3_5_3_edge_case(tmp_path: Path) -> None:
    users_path = write_users_csv(tmp_path / "users.csv", ["a", "b"])
    interactions_path = write_interactions_csv(tmp_path / "interactions.csv", [])
    Graph3ReviewsBuilder().build_and_export(
        str(interactions_path),
        str(users_path),
        str(tmp_path / Graph3ReviewsBuilder.OUTPUT_GEXF),
    )


def test_3_5_3_idempotencia_ou_invariante(synthetic_csv_dir: tuple[Path, Path], tmp_path: Path) -> None:
    users_path, interactions_path = synthetic_csv_dir
    path = tmp_path / Graph3ReviewsBuilder.OUTPUT_GEXF
    Graph3ReviewsBuilder().build_and_export(str(interactions_path), str(users_path), str(path))
    assert "directed" in path.read_text(encoding="utf-8")


# --- FEAT 3.6 G4 ---


def test_3_6_1_cenario_feliz(synthetic_csv_dir: tuple[Path, Path]) -> None:
    users_path, interactions_path = synthetic_csv_dir
    rows = Graph4IntegratedBuilder()._load_interactions_csv(str(interactions_path))
    filtered = Graph4IntegratedBuilder()._filter_interactions(rows)
    assert len(filtered) == len(SAMPLE_INTERACTIONS)


def test_3_6_1_cenario_alternativo() -> None:
    assert set(INTERACTION_WEIGHT_BY_TYPE) == {
        "comment_issue",
        "comment_pr",
        "open_issue_commented",
        "review_pr",
        "merge_pr",
        "close_issue",
    }


def test_3_6_1_edge_case() -> None:
    with pytest.raises(ValueError):
        official_weight("unknown")


def test_3_6_1_idempotencia_ou_invariante() -> None:
    assert official_weight("merge_pr") == 5.0


def test_3_6_2_cenario_feliz(synthetic_csv_dir: tuple[Path, Path]) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph4IntegratedBuilder().build(str(interactions_path), str(users_path))
    alice = registry.get_index("alice")
    bob = registry.get_index("bob")
    assert graph.get_edge_weight(alice, bob) == 4.0


def test_3_6_2_cenario_alternativo() -> None:
    assert Graph4IntegratedBuilder()._sum_weight(2.0, 3.0) == 5.0


def test_3_6_2_edge_case(synthetic_csv_dir: tuple[Path, Path]) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph4IntegratedBuilder().build(str(interactions_path), str(users_path))
    assert graph.has_edge(registry.get_index("bob"), registry.get_index("alice"))


def test_3_6_2_idempotencia_ou_invariante(synthetic_csv_dir: tuple[Path, Path]) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, _ = Graph4IntegratedBuilder().build(str(interactions_path), str(users_path))
    assert graph.get_edge_count() == 5


def test_3_6_3_cenario_feliz() -> None:
    assert official_weight("comment_pr") == 2.0
    assert official_weight("close_issue") == 3.0


def test_3_6_3_cenario_alternativo(synthetic_csv_dir: tuple[Path, Path]) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph4IntegratedBuilder().build(str(interactions_path), str(users_path))
    assert graph.get_edge_weight(registry.get_index("erin"), registry.get_index("bob")) == 5.0


def test_3_6_3_edge_case() -> None:
    with pytest.raises(ValueError, match="Invalid interaction type"):
        official_weight("not-a-type")


def test_3_6_3_idempotencia_ou_invariante() -> None:
    assert Graph4IntegratedBuilder.accumulate_edge_weights is True


# --- FEAT 3.7 aggregate tests ---


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_filtro_por_tipo_interacao(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    g1, _ = Graph1CommentsBuilder(graph_factory=graph_factory).build(str(interactions_path), str(users_path))
    g2, _ = Graph2ClosuresBuilder(graph_factory=graph_factory).build(str(interactions_path), str(users_path))
    g3, _ = Graph3ReviewsBuilder(graph_factory=graph_factory).build(str(interactions_path), str(users_path))
    g4, _ = Graph4IntegratedBuilder(graph_factory=graph_factory).build(str(interactions_path), str(users_path))
    assert g1.get_edge_count() == 1
    assert g2.get_edge_count() == 1
    assert g3.get_edge_count() == 2
    assert g4.get_edge_count() == 5


def test_agregacao_pesos_g4(synthetic_csv_dir: tuple[Path, Path]) -> None:
    users_path, interactions_path = synthetic_csv_dir
    graph, registry = Graph4IntegratedBuilder().build(str(interactions_path), str(users_path))
    assert graph.get_edge_weight(registry.get_index("alice"), registry.get_index("bob")) == 4.0


@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_cenario_feliz_builder(synthetic_csv_dir: tuple[Path, Path], graph_factory) -> None:
    users_path, interactions_path = synthetic_csv_dir
    for builder_cls in (
        Graph1CommentsBuilder,
        Graph2ClosuresBuilder,
        Graph3ReviewsBuilder,
        Graph4IntegratedBuilder,
    ):
        graph, registry = builder_cls(graph_factory=graph_factory).build(
            str(interactions_path),
            str(users_path),
        )
        assert graph.get_vertex_count() == len(registry) > 0


@pytest.mark.skipif(not MINED_USERS.is_file(), reason="mined users.csv not available")
@pytest.mark.parametrize("graph_factory", GRAPH_FACTORIES)
def test_3_7_1_cenario_feliz_mined_data(graph_factory) -> None:
    g1, _ = Graph1CommentsBuilder(graph_factory=graph_factory).build(str(MINED_INTERACTIONS), str(MINED_USERS))
    g2, _ = Graph2ClosuresBuilder(graph_factory=graph_factory).build(str(MINED_INTERACTIONS), str(MINED_USERS))
    assert g1.get_vertex_count() > 0
    assert g2.get_edge_count() >= 0


@pytest.mark.skipif(not MINED_USERS.is_file(), reason="mined data not available")
def test_3_7_2_cenario_feliz_mined_g4() -> None:
    graph, _ = Graph4IntegratedBuilder().build(str(MINED_INTERACTIONS), str(MINED_USERS))
    assert graph.get_edge_count() > 0


def test_apply_interaction_skips_self_loop_on_graph() -> None:
    graph = AdjacencyListGraph(2)
    registry = UserRegistry()
    registry.add_user("alice")
    registry.add_user("bob")
    builder = Graph1CommentsBuilder()
    builder._apply_interaction(
        graph,
        {
            "src_login": "alice",
            "dst_login": "alice",
            "type": "comment_issue",
            "weight": 2,
            "timestamp": "2026-01-01T10:00:00Z",
            "source_id": "1",
        },
        registry,
    )
    assert graph.get_edge_count() == 0


def test_load_users_csv_missing_columns(tmp_path: Path) -> None:
    bad_users = tmp_path / "users.csv"
    bad_users.write_text("login\nalice\n", encoding="utf-8")
    with pytest.raises(InvalidCsvError, match="missing columns"):
        Graph1CommentsBuilder()._load_users_csv(str(bad_users), UserRegistry())


def test_load_interactions_csv_missing_file(tmp_path: Path) -> None:
    with pytest.raises(InvalidCsvError, match="file does not exist"):
        Graph1CommentsBuilder()._load_interactions_csv(str(tmp_path / "missing.csv"))


def test_graph_factory_helpers() -> None:
    list_graph = BaseBuilder.list_graph_factory(3)
    matrix_graph = BaseBuilder.matrix_graph_factory(3)
    assert isinstance(list_graph, AdjacencyListGraph)
    assert isinstance(matrix_graph, AdjacencyMatrixGraph)
    assert list_graph.get_vertex_count() == matrix_graph.get_vertex_count() == 3


@pytest.mark.skipif(not MINED_USERS.is_file(), reason="mined data not available")
def test_3_7_3_export_all_graphs(tmp_path: Path) -> None:
    builders = [
        Graph1CommentsBuilder(),
        Graph2ClosuresBuilder(),
        Graph3ReviewsBuilder(),
        Graph4IntegratedBuilder(),
    ]
    for builder in builders:
        output = tmp_path / builder.OUTPUT_GEXF
        _, _, written = builder.build_and_export(
            str(MINED_INTERACTIONS),
            str(MINED_USERS),
            str(output),
        )
        assert Path(written).is_file()
