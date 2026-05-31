from __future__ import annotations

from src.graph.abstract_graph import AbstractGraph


class AdjacencyListGraph(AbstractGraph):
    """Directed simple graph backed by adjacency lists."""

    def __init__(self, num_vertices: int) -> None:
        super().__init__(num_vertices)
        self._adjacency: list[dict[int, float]] = [{} for _ in range(num_vertices)]

    def has_edge(self, source: int, target: int) -> bool:
        self._validate_vertex(source)
        self._validate_vertex(target)
        return target in self._adjacency[source]

    def add_edge(self, source: int, target: int) -> None:
        self._validate_vertex(source)
        self._validate_vertex(target)
        self._validate_no_self_loop(source, target)
        if target in self._adjacency[source]:
            return
        self._adjacency[source][target] = 0.0
        self._increment_edge_count()

    def remove_edge(self, source: int, target: int) -> None:
        self._validate_vertex(source)
        self._validate_vertex(target)
        self._ensure_edge_exists(source, target)
        del self._adjacency[source][target]
        self._decrement_edge_count()

    def get_vertex_in_degree(self, vertex: int) -> int:
        self._validate_vertex(vertex)
        return sum(1 for adjacency in self._adjacency if vertex in adjacency)

    def get_vertex_out_degree(self, vertex: int) -> int:
        self._validate_vertex(vertex)
        return len(self._adjacency[vertex])

    def set_edge_weight(self, source: int, target: int, weight: float) -> None:
        self._validate_vertex(source)
        self._validate_vertex(target)
        self._ensure_edge_exists(source, target)
        self._adjacency[source][target] = float(weight)

    def get_edge_weight(self, source: int, target: int) -> float:
        self._validate_vertex(source)
        self._validate_vertex(target)
        self._ensure_edge_exists(source, target)
        return float(self._adjacency[source][target])

    def iter_edges(self) -> list[tuple[int, int, float]]:
        """Return all edges as ``(source, target, weight)`` tuples."""

        edges: list[tuple[int, int, float]] = []
        for source, targets in enumerate(self._adjacency):
            for target, weight in targets.items():
                edges.append((source, target, weight))
        return edges
