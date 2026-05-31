from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque

from src.graph.exceptions import EdgeNotFoundError, InvalidVertexError, SelfLoopError


class AbstractGraph(ABC):
    """Abstract directed simple graph with shared vertex metadata and validations."""

    def __init__(self, num_vertices: int) -> None:
        if num_vertices < 0:
            raise ValueError("num_vertices must be non-negative")
        self._num_vertices = num_vertices
        self._edge_count = 0
        self._vertex_weights = [0.0] * num_vertices
        self._vertex_labels = [str(index) for index in range(num_vertices)]

    def get_vertex_count(self) -> int:
        """Return the number of vertices in the graph."""

        return self._num_vertices

    def get_edge_count(self) -> int:
        """Return the number of directed edges in the graph."""

        return self._edge_count

    def set_vertex_weight(self, vertex: int, weight: float) -> None:
        """Assign a weight to a vertex."""

        self._validate_vertex(vertex)
        self._vertex_weights[vertex] = float(weight)

    def get_vertex_weight(self, vertex: int) -> float:
        """Return the weight of a vertex."""

        self._validate_vertex(vertex)
        return self._vertex_weights[vertex]

    def set_vertex_label(self, vertex: int, label: str) -> None:
        """Assign a display label to a vertex."""

        self._validate_vertex(vertex)
        self._vertex_labels[vertex] = str(label)

    def get_vertex_label(self, vertex: int) -> str:
        """Return the display label of a vertex."""

        self._validate_vertex(vertex)
        return self._vertex_labels[vertex]

    def is_successor(self, source: int, target: int) -> bool:
        """Return True when ``source -> target`` exists."""

        self._validate_vertex(source)
        self._validate_vertex(target)
        return self.has_edge(source, target)

    def is_predecessor(self, source: int, target: int) -> bool:
        """Return True when ``target -> source`` exists."""

        self._validate_vertex(source)
        self._validate_vertex(target)
        return self.has_edge(target, source)

    def is_divergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
        """Return True when two edges share the same source vertex."""

        self._validate_vertex(u1)
        self._validate_vertex(v1)
        self._validate_vertex(u2)
        self._validate_vertex(v2)
        return u1 == u2 and self.has_edge(u1, v1) and self.has_edge(u2, v2)

    def is_convergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
        """Return True when two edges share the same target vertex."""

        self._validate_vertex(u1)
        self._validate_vertex(v1)
        self._validate_vertex(u2)
        self._validate_vertex(v2)
        return v1 == v2 and self.has_edge(u1, v1) and self.has_edge(u2, v2)

    def is_incident(self, source: int, target: int, vertex: int) -> bool:
        """Return True when ``vertex`` is an endpoint of ``source -> target``."""

        self._validate_vertex(source)
        self._validate_vertex(target)
        self._validate_vertex(vertex)
        return vertex in {source, target}

    def is_empty_graph(self) -> bool:
        """Return True when the graph has no edges."""

        return self._edge_count == 0

    def is_complete_graph(self) -> bool:
        """Return True when every ordered pair of distinct vertices has an edge."""

        vertex_count = self._num_vertices
        if vertex_count <= 1:
            return True
        for source in range(vertex_count):
            for target in range(vertex_count):
                if source != target and not self.has_edge(source, target):
                    return False
        return True

    def is_connected(self) -> bool:
        """Return True when the graph is weakly connected."""

        vertex_count = self._num_vertices
        if vertex_count == 0:
            return True
        if self._edge_count == 0:
            return vertex_count == 1

        adjacency = [set[int]() for _ in range(vertex_count)]
        for source in range(vertex_count):
            for target in range(vertex_count):
                if source != target and self.has_edge(source, target):
                    adjacency[source].add(target)
                    adjacency[target].add(source)

        visited: set[int] = set()
        queue: deque[int] = deque([0])
        visited.add(0)
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return len(visited) == vertex_count

    def export_to_gephi(self, path: str) -> None:
        """Export the graph to a GEXF file consumable by Gephi."""

        from src.graph.gephi_exporter import export_to_gephi

        export_to_gephi(self, path)

    def iter_edges(self) -> list[tuple[int, int, float]]:
        """Return all edges as ``(source, target, weight)`` tuples."""

        edges: list[tuple[int, int, float]] = []
        for source in range(self._num_vertices):
            for target in range(self._num_vertices):
                if self.has_edge(source, target):
                    edges.append((source, target, self.get_edge_weight(source, target)))
        return edges

    def _validate_vertex(self, vertex: int) -> None:
        if vertex < 0 or vertex >= self._num_vertices:
            raise InvalidVertexError(vertex, self._num_vertices)

    def _validate_no_self_loop(self, source: int, target: int) -> None:
        if source == target:
            raise SelfLoopError(source)

    def _increment_edge_count(self) -> None:
        self._edge_count += 1

    def _decrement_edge_count(self) -> None:
        self._edge_count -= 1

    @abstractmethod
    def has_edge(self, source: int, target: int) -> bool:
        """Return True when a directed edge exists."""

    @abstractmethod
    def add_edge(self, source: int, target: int) -> None:
        """Add a directed edge.

        Idempotent: repeated calls do not duplicate edges or change weights.
        New edges start with weight ``0.0``.
        """

    @abstractmethod
    def remove_edge(self, source: int, target: int) -> None:
        """Remove a directed edge."""

    @abstractmethod
    def get_vertex_in_degree(self, vertex: int) -> int:
        """Return the in-degree of a vertex."""

    @abstractmethod
    def get_vertex_out_degree(self, vertex: int) -> int:
        """Return the out-degree of a vertex."""

    @abstractmethod
    def set_edge_weight(self, source: int, target: int, weight: float) -> None:
        """Assign a weight to an existing edge."""

    @abstractmethod
    def get_edge_weight(self, source: int, target: int) -> float:
        """Return the weight of an existing edge."""

    def _ensure_edge_exists(self, source: int, target: int) -> None:
        if not self.has_edge(source, target):
            raise EdgeNotFoundError(source, target)
