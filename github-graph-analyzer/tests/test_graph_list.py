from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from src.graph.adjacency_list_graph import AdjacencyListGraph
from src.graph.adjacency_matrix_graph import AdjacencyMatrixGraph
from src.graph.exceptions import SelfLoopError
from tests.graph_test_helpers import assert_graphs_equivalent, build_sample_graph


@pytest.mark.parametrize("factory", [AdjacencyListGraph])
class TestAdjacencyListGraphContract:
    def test_cenario_feliz_graph_list(self, factory, tmp_path: Path) -> None:
        graph = build_sample_graph(factory)
        assert graph.get_vertex_count() == 4
        assert graph.get_edge_count() == 4
        graph.export_to_gephi(str(tmp_path / "list.gexf"))
        ET.parse(tmp_path / "list.gexf")

    def test_idempotencia_add_edge_list(self, factory) -> None:
        graph = factory(3)
        graph.add_edge(0, 2)
        graph.set_edge_weight(0, 2, 9.0)
        graph.add_edge(0, 2)
        assert graph.get_edge_count() == 1
        assert graph.get_edge_weight(0, 2) == 9.0

    def test_excecao_self_loop_list(self, factory) -> None:
        graph = factory(2)
        with pytest.raises(SelfLoopError):
            graph.add_edge(1, 1)


def test_list_internal_adjacency_structure() -> None:
    graph = AdjacencyListGraph(3)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    assert graph._adjacency[0] == {1: 0.0, 2: 0.0}
    assert graph.get_vertex_out_degree(0) == 2


def test_list_and_matrix_remain_equivalent_after_removals() -> None:
    matrix_graph = AdjacencyMatrixGraph(5)
    list_graph = AdjacencyListGraph(5)
    operations = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4), (2, 4)]
    for source, target in operations:
        matrix_graph.add_edge(source, target)
        list_graph.add_edge(source, target)
        matrix_graph.set_edge_weight(source, target, float(source + target))
        list_graph.set_edge_weight(source, target, float(source + target))
    matrix_graph.remove_edge(1, 2)
    list_graph.remove_edge(1, 2)
    assert_graphs_equivalent(matrix_graph, list_graph)
