from __future__ import annotations

import numpy as np

from src.graph.abstract_graph import AbstractGraph


class AdjacencyMatrixGraph(AbstractGraph):
    """Directed simple graph backed by numpy adjacency and weight matrices."""

    def __init__(self, num_vertices: int) -> None:
        super().__init__(num_vertices)
        self._adjacency = np.zeros((num_vertices, num_vertices), dtype=bool)
        self._weights = np.zeros((num_vertices, num_vertices), dtype=float)

    def has_edge(self, source: int, target: int) -> bool:
        self._validate_vertex(source)
        self._validate_vertex(target)
        return bool(self._adjacency[source, target])

    def add_edge(self, source: int, target: int) -> None:
        self._validate_vertex(source)
        self._validate_vertex(target)
        self._validate_no_self_loop(source, target)
        if self._adjacency[source, target]:
            return
        self._adjacency[source, target] = True
        self._weights[source, target] = 0.0
        self._increment_edge_count()

    def remove_edge(self, source: int, target: int) -> None:
        self._validate_vertex(source)
        self._validate_vertex(target)
        self._ensure_edge_exists(source, target)
        self._adjacency[source, target] = False
        self._weights[source, target] = 0.0
        self._decrement_edge_count()

    def get_vertex_in_degree(self, vertex: int) -> int:
        self._validate_vertex(vertex)
        return int(self._adjacency[:, vertex].sum())

    def get_vertex_out_degree(self, vertex: int) -> int:
        self._validate_vertex(vertex)
        return int(self._adjacency[vertex, :].sum())

    def set_edge_weight(self, source: int, target: int, weight: float) -> None:
        self._validate_vertex(source)
        self._validate_vertex(target)
        self._ensure_edge_exists(source, target)
        self._weights[source, target] = float(weight)

    def get_edge_weight(self, source: int, target: int) -> float:
        self._validate_vertex(source)
        self._validate_vertex(target)
        self._ensure_edge_exists(source, target)
        return float(self._weights[source, target])

    def iter_edges(self) -> list[tuple[int, int, float]]:
        """Return all edges as ``(source, target, weight)`` tuples."""

        edges: list[tuple[int, int, float]] = []
        for source in range(self._num_vertices):
            for target in range(self._num_vertices):
                if self._adjacency[source, target]:
                    edges.append((source, target, float(self._weights[source, target])))
        return edges
