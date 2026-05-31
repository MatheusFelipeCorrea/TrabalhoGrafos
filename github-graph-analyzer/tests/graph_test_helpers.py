from __future__ import annotations

from typing import Callable, TypeVar

import pytest

from src.graph.abstract_graph import AbstractGraph
from src.graph.adjacency_list_graph import AdjacencyListGraph
from src.graph.adjacency_matrix_graph import AdjacencyMatrixGraph
from src.graph.exceptions import EdgeNotFoundError, InvalidVertexError, SelfLoopError

GraphFactory = TypeVar("GraphFactory", bound=Callable[[int], AbstractGraph])


@pytest.fixture(params=[AdjacencyMatrixGraph, AdjacencyListGraph])
def graph_factory(request: pytest.FixtureRequest) -> GraphFactory:
    return request.param


def build_sample_graph(factory: GraphFactory) -> AbstractGraph:
    graph = factory(4)
    graph.set_vertex_label(0, "alice")
    graph.set_vertex_label(1, "bob")
    graph.set_vertex_label(2, "carol")
    graph.set_vertex_label(3, "dave")
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(0, 3)
    graph.set_edge_weight(0, 1, 2.0)
    graph.set_edge_weight(1, 2, 4.0)
    graph.set_edge_weight(2, 3, 5.0)
    graph.set_edge_weight(0, 3, 3.0)
    graph.set_vertex_weight(0, 1.5)
    return graph


def assert_graphs_equivalent(first: AbstractGraph, second: AbstractGraph) -> None:
    assert first.get_vertex_count() == second.get_vertex_count()
    assert first.get_edge_count() == second.get_edge_count()
    vertex_count = first.get_vertex_count()
    for vertex in range(vertex_count):
        assert first.get_vertex_weight(vertex) == second.get_vertex_weight(vertex)
        assert first.get_vertex_label(vertex) == second.get_vertex_label(vertex)
        assert first.get_vertex_in_degree(vertex) == second.get_vertex_in_degree(vertex)
        assert first.get_vertex_out_degree(vertex) == second.get_vertex_out_degree(vertex)
    for source in range(vertex_count):
        for target in range(vertex_count):
            assert first.has_edge(source, target) == second.has_edge(source, target)
            if first.has_edge(source, target):
                assert first.get_edge_weight(source, target) == second.get_edge_weight(source, target)
