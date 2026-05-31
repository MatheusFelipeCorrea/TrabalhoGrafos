from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from pathlib import Path

import pandas as pd

from src.builder.exceptions import InvalidCsvError
from src.builder.user_registry import UserRegistry
from src.graph.abstract_graph import AbstractGraph
from src.graph.adjacency_list_graph import AdjacencyListGraph
from src.graph.adjacency_matrix_graph import AdjacencyMatrixGraph
from src.graph.gephi_exporter import export_to_gephi
from src.mining.data_exporter import DataExporter
from src.mining.interaction_model import Interaction

GraphFactory = Callable[[int], AbstractGraph]


class BaseBuilder(ABC):
    """Read mined CSVs, filter interactions, and populate a directed simple graph."""

    accumulate_edge_weights: bool = False

    def __init__(self, graph_factory: GraphFactory | None = None) -> None:
        self._graph_factory = graph_factory or AdjacencyListGraph

    @staticmethod
    def list_graph_factory(num_vertices: int) -> AbstractGraph:
        """Create an adjacency-list graph (preferred default)."""

        return AdjacencyListGraph(num_vertices)

    @staticmethod
    def matrix_graph_factory(num_vertices: int) -> AbstractGraph:
        """Create an adjacency-matrix graph."""

        return AdjacencyMatrixGraph(num_vertices)

    def build(self, interactions_csv: str, users_csv: str) -> tuple[AbstractGraph, UserRegistry]:
        """Load CSVs, register users, and return a populated graph plus registry."""

        registry = UserRegistry()
        self._load_users_csv(users_csv, registry)
        rows = self._load_interactions_csv(interactions_csv)
        filtered_rows = self._filter_interactions(rows)

        for row in filtered_rows:
            src_login = str(row["src_login"]).strip()
            dst_login = str(row["dst_login"]).strip()
            registry.add_user(src_login)
            registry.add_user(dst_login)

        graph = self._graph_factory(len(registry))
        for index, login in enumerate(registry.logins()):
            graph.set_vertex_label(index, login)

        for row in filtered_rows:
            self._apply_interaction(graph, row, registry)
        return graph, registry

    def build_and_export(
        self,
        interactions_csv: str,
        users_csv: str,
        output_path: str,
    ) -> tuple[AbstractGraph, UserRegistry, str]:
        """Build the graph and write a GEXF file."""

        graph, registry = self.build(interactions_csv, users_csv)
        written_path = export_to_gephi(graph, output_path)
        return graph, registry, written_path

    @abstractmethod
    def _filter_interactions(self, rows: list[dict[str, object]]) -> list[dict[str, object]]:
        """Return only the interaction rows relevant to this builder."""

    def _interaction_weight(self, row: dict[str, object]) -> float:
        """Return the weight applied when creating or updating an edge."""

        return float(row["weight"])

    def _apply_interaction(
        self,
        graph: AbstractGraph,
        row: dict[str, object],
        registry: UserRegistry,
    ) -> None:
        """Map logins to indices and add or update a directed edge."""

        src = registry.get_index(str(row["src_login"]).strip())
        dst = registry.get_index(str(row["dst_login"]).strip())
        if src == dst:
            return

        weight = self._interaction_weight(row)
        if not graph.has_edge(src, dst):
            graph.add_edge(src, dst)
            graph.set_edge_weight(src, dst, weight)
            return

        if self.accumulate_edge_weights:
            current = graph.get_edge_weight(src, dst)
            graph.set_edge_weight(src, dst, self._sum_weight(current, weight))

    @staticmethod
    def _sum_weight(current: float, increment: float) -> float:
        return float(current) + float(increment)

    def _load_users_csv(self, users_csv: str, registry: UserRegistry) -> None:
        path = Path(users_csv)
        if not path.is_file():
            raise InvalidCsvError(str(path), "file does not exist")

        frame = pd.read_csv(path)
        missing = [column for column in DataExporter.USER_COLUMNS if column not in frame.columns]
        if missing:
            raise InvalidCsvError(str(path), f"missing columns: {', '.join(missing)}")

        for login in frame["login"].astype(str):
            normalized = login.strip()
            if normalized:
                registry.add_user(normalized)

    def _load_interactions_csv(self, interactions_csv: str) -> list[dict[str, object]]:
        path = Path(interactions_csv)
        if not path.is_file():
            raise InvalidCsvError(str(path), "file does not exist")

        frame = pd.read_csv(path)
        missing = [column for column in DataExporter.INTERACTION_COLUMNS if column not in frame.columns]
        if missing:
            raise InvalidCsvError(str(path), f"missing columns: {', '.join(missing)}")

        rows: list[dict[str, object]] = []
        for record in frame.to_dict(orient="records"):
            row = {key: record[key] for key in DataExporter.INTERACTION_COLUMNS}
            self._validate_interaction_row(row, str(path))
            rows.append(row)
        return rows

    @staticmethod
    def _validate_interaction_row(row: dict[str, object], path: str) -> None:
        try:
            Interaction(
                src_login=str(row["src_login"]),
                dst_login=str(row["dst_login"]),
                type=str(row["type"]),
                weight=int(row["weight"]),
                timestamp=str(row["timestamp"]),
                source_id=str(row["source_id"]),
            )
        except ValueError as error:
            raise InvalidCsvError(path, str(error)) from error
