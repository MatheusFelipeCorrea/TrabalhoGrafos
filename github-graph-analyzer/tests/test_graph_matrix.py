from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pytest

from src.graph.adjacency_list_graph import AdjacencyListGraph
from src.graph.adjacency_matrix_graph import AdjacencyMatrixGraph
from src.graph.exceptions import EdgeNotFoundError, InvalidVertexError, SelfLoopError
from src.graph.gephi_exporter import export_to_gephi
from tests.graph_test_helpers import assert_graphs_equivalent, build_sample_graph


@pytest.mark.parametrize("factory", [AdjacencyMatrixGraph, AdjacencyListGraph])
class TestGraphContract:
    def test_cenario_feliz_graph_matrix(self, factory, tmp_path: Path) -> None:
        graph = build_sample_graph(factory)
        assert graph.get_vertex_count() == 4
        assert graph.get_edge_count() == 4
        assert graph.get_edge_weight(0, 1) == 2.0
        assert graph.get_vertex_weight(0) == 1.5
        assert graph.is_successor(0, 1)
        assert graph.is_predecessor(1, 0)
        assert graph.is_divergent(0, 1, 0, 3)
        assert graph.is_convergent(1, 2, 0, 3) is False
        assert graph.is_incident(0, 1, 0)
        assert graph.is_empty_graph() is False
        assert graph.is_connected() is True
        output = tmp_path / "sample.gexf"
        graph.export_to_gephi(str(output))
        assert output.exists()
        ET.parse(output)

    def test_idempotencia_add_edge_matrix(self, factory) -> None:
        graph = factory(3)
        graph.add_edge(0, 1)
        graph.set_edge_weight(0, 1, 7.0)
        graph.add_edge(0, 1)
        assert graph.get_edge_count() == 1
        assert graph.get_edge_weight(0, 1) == 7.0

    def test_excecao_indice_invalido_matrix(self, factory) -> None:
        graph = factory(2)
        with pytest.raises(InvalidVertexError):
            graph.add_edge(-1, 0)
        with pytest.raises(InvalidVertexError):
            graph.add_edge(0, 2)
        with pytest.raises(InvalidVertexError):
            graph.get_vertex_out_degree(5)

    def test_excecao_self_loop_list(self, factory) -> None:
        graph = factory(2)
        with pytest.raises(SelfLoopError):
            graph.add_edge(1, 1)

    def test_edge_not_found_on_remove_and_weight(self, factory) -> None:
        graph = factory(2)
        with pytest.raises(EdgeNotFoundError):
            graph.remove_edge(0, 1)
        graph.add_edge(0, 1)
        graph.remove_edge(0, 1)
        with pytest.raises(EdgeNotFoundError):
            graph.get_edge_weight(0, 1)
        with pytest.raises(EdgeNotFoundError):
            graph.set_edge_weight(0, 1, 1.0)

    def test_new_edge_default_weight_is_zero(self, factory) -> None:
        graph = factory(2)
        graph.add_edge(0, 1)
        assert graph.get_edge_weight(0, 1) == 0.0

    def test_vertex_label_roundtrip(self, factory) -> None:
        graph = factory(2)
        assert graph.get_vertex_label(0) == "0"
        graph.set_vertex_label(0, "alice")
        assert graph.get_vertex_label(0) == "alice"

    def test_empty_and_single_vertex_graph(self, factory) -> None:
        empty = factory(0)
        assert empty.get_vertex_count() == 0
        assert empty.is_empty_graph()
        assert empty.is_connected()
        assert empty.is_complete_graph()

        single = factory(1)
        assert single.is_empty_graph()
        assert single.is_complete_graph()
        assert single.is_connected()

    def test_complete_directed_graph(self, factory) -> None:
        graph = factory(3)
        for source in range(3):
            for target in range(3):
                if source != target:
                    graph.add_edge(source, target)
        assert graph.is_complete_graph()
        assert graph.get_edge_count() == 6

    def test_disconnected_graph_is_not_connected(self, factory) -> None:
        graph = factory(4)
        graph.add_edge(0, 1)
        graph.add_edge(2, 3)
        assert graph.is_connected() is False

    def test_is_convergent_true(self, factory) -> None:
        graph = factory(3)
        graph.add_edge(0, 2)
        graph.add_edge(1, 2)
        assert graph.is_convergent(0, 2, 1, 2)

    def test_relation_validations_reject_invalid_vertices(self, factory) -> None:
        graph = factory(2)
        graph.add_edge(0, 1)
        with pytest.raises(InvalidVertexError):
            graph.is_divergent(0, 1, 2, 0)
        with pytest.raises(InvalidVertexError):
            graph.is_convergent(0, 1, 0, 2)
        with pytest.raises(InvalidVertexError):
            graph.is_incident(0, 1, 3)

    def test_is_divergent_true(self, factory) -> None:
        graph = factory(3)
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        assert graph.is_divergent(0, 1, 0, 2)

    def test_is_divergent_requires_shared_source(self, factory) -> None:
        graph = factory(3)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        assert graph.is_divergent(0, 1, 1, 2) is False

    def test_is_incident_false_for_unrelated_vertex(self, factory) -> None:
        graph = factory(3)
        graph.add_edge(0, 1)
        assert graph.is_incident(0, 1, 2) is False

    def test_incomplete_graph_with_same_edge_count(self, factory) -> None:
        graph = factory(4)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        assert graph.get_edge_count() == 3
        assert graph.is_complete_graph() is False

    def test_is_divergent_true(self, factory) -> None:
        graph = factory(3)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        assert graph.get_vertex_out_degree(0) == 1
        assert graph.get_vertex_in_degree(1) == 1
        graph.remove_edge(0, 1)
        assert graph.get_vertex_out_degree(0) == 0
        assert graph.get_vertex_in_degree(1) == 0


class TestExceptions:
    def test_invalid_vertex_error_message(self) -> None:
        error = InvalidVertexError(4, 3)
        assert "Invalid vertex index 4" in str(error)

    def test_self_loop_error_message(self) -> None:
        error = SelfLoopError(2)
        assert "Self-loops are not allowed" in str(error)

    def test_edge_not_found_error_message(self) -> None:
        error = EdgeNotFoundError(0, 1)
        assert "Edge (0, 1) does not exist" in str(error)


class TestAdjacencyMatrixGraph:
    def test_zero_vertex_matrix(self) -> None:
        graph = AdjacencyMatrixGraph(0)
        assert graph.get_vertex_count() == 0

    def test_numpy_backing_arrays(self) -> None:
        graph = AdjacencyMatrixGraph(3)
        graph.add_edge(0, 1)
        assert graph._adjacency.shape == (3, 3)
        assert graph._adjacency[0, 1]
        assert graph._weights[0, 1] == 0.0
        assert isinstance(graph._adjacency, np.ndarray)


class TestMatrixListEquivalence:
    def test_same_operations_produce_same_graph(self) -> None:
        matrix_graph = build_sample_graph(AdjacencyMatrixGraph)
        list_graph = build_sample_graph(AdjacencyListGraph)
        assert_graphs_equivalent(matrix_graph, list_graph)

    def test_gexf_export_contains_nodes_edges_and_weights(self, tmp_path: Path) -> None:
        graph = build_sample_graph(AdjacencyMatrixGraph)
        output = Path(export_to_gephi(graph, str(tmp_path / "graph.gexf")))
        root = ET.parse(output).getroot()
        namespace = "{http://www.gexf.net/1.3}"
        nodes = root.find(f".//{namespace}nodes")
        edges = root.find(f".//{namespace}edges")
        assert nodes is not None
        assert edges is not None
        assert len(nodes.findall(f"{namespace}node")) == 4
        assert len(edges.findall(f"{namespace}edge")) == 4
        first_edge = edges.findall(f"{namespace}edge")[0]
        attvalue = first_edge.find(f".//{namespace}attvalue")
        assert attvalue is not None
        assert attvalue.get("for") == "0"

    def test_gexf_list_graph_export_is_valid_xml(self, tmp_path: Path) -> None:
        graph = build_sample_graph(AdjacencyListGraph)
        output = Path(export_to_gephi(graph, str(tmp_path / "list.gexf")))
        ET.parse(output)

    def test_negative_num_vertices_rejected(self) -> None:
        with pytest.raises(ValueError):
            AdjacencyMatrixGraph(-1)
        with pytest.raises(ValueError):
            AdjacencyListGraph(-1)
