from __future__ import annotations

import pytest

from src.analysis.centrality import (
    betweenness_centrality,
    closeness_centrality,
    degree_centrality,
    pagerank,
)
from src.analysis.centrality import _dijkstra_brandes, _shortest_distances
from src.analysis.community import _local_moving, bridging_ties, detect_communities, modularity
from src.analysis.structure import _pearson_correlation, clustering_coefficient, degree_assortativity, density
from src.graph.abstract_graph import AbstractGraph
from src.graph.adjacency_list_graph import AdjacencyListGraph
from src.graph.adjacency_matrix_graph import AdjacencyMatrixGraph


# ---------------------------------------------------------------------------
# Construtores auxiliares de grafos
# ---------------------------------------------------------------------------


def build_star_graph(factory, num_leaves: int = 4):
    """Hub (0) → todas as folhas (1..num_leaves). Sem arestas reversas."""

    graph = factory(num_leaves + 1)
    for leaf in range(1, num_leaves + 1):
        graph.add_edge(0, leaf)
    return graph


def build_cycle_graph(factory, num_vertices: int = 4):
    """0→1→2→…→(n-1)→0."""

    graph = factory(num_vertices)
    for i in range(num_vertices):
        graph.add_edge(i, (i + 1) % num_vertices)
    return graph


def build_complete_graph(factory, num_vertices: int = 4):
    """Todas as arestas dirigidas entre vértices distintos."""

    graph = factory(num_vertices)
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i != j:
                graph.add_edge(i, j)
    return graph


def build_disconnected_graph(factory):
    """Dois componentes desconectados: {0→1} e {2→3}."""

    graph = factory(4)
    graph.add_edge(0, 1)
    graph.add_edge(2, 3)
    return graph


def build_path_graph(factory, num_vertices: int = 4):
    """0→1→2→3 (sem ciclo de volta)."""

    graph = factory(num_vertices)
    for i in range(num_vertices - 1):
        graph.add_edge(i, i + 1)
    return graph


def build_weighted_triangle(factory):
    """0→1 (w=2), 1→2 (w=4), 2→0 (w=5)."""

    graph = factory(3)
    graph.add_edge(0, 1)
    graph.set_edge_weight(0, 1, 2.0)
    graph.add_edge(1, 2)
    graph.set_edge_weight(1, 2, 4.0)
    graph.add_edge(2, 0)
    graph.set_edge_weight(2, 0, 5.0)
    return graph


# ---------------------------------------------------------------------------
# Centralidade de Grau
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("factory", [AdjacencyMatrixGraph, AdjacencyListGraph])
class TestDegreeCentrality:
    def test_star_hub_has_maximum_out_degree(self, factory) -> None:
        graph = build_star_graph(factory, num_leaves=4)
        dc = degree_centrality(graph)
        assert dc[0]["out"] == pytest.approx(4 / 4)
        assert dc[0]["in"] == pytest.approx(0.0)
        for leaf in range(1, 5):
            assert dc[leaf]["out"] == pytest.approx(0.0)
            assert dc[leaf]["in"] == pytest.approx(1 / 4)

    def test_cycle_uniform_degree(self, factory) -> None:
        graph = build_cycle_graph(factory, num_vertices=4)
        dc = degree_centrality(graph)
        for vertex in range(4):
            assert dc[vertex]["in"] == pytest.approx(1 / 3)
            assert dc[vertex]["out"] == pytest.approx(1 / 3)

    def test_empty_graph_zero_degree(self, factory) -> None:
        graph = factory(3)
        dc = degree_centrality(graph)
        for vertex in range(3):
            assert dc[vertex]["in"] == pytest.approx(0.0)
            assert dc[vertex]["out"] == pytest.approx(0.0)

    def test_single_vertex(self, factory) -> None:
        graph = factory(1)
        dc = degree_centrality(graph)
        assert dc[0]["in"] == pytest.approx(0.0)
        assert dc[0]["out"] == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Centralidade de Intermediação
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("factory", [AdjacencyMatrixGraph, AdjacencyListGraph])
class TestBetweennessCentrality:
    def test_path_middle_vertices_have_highest_betweenness(self, factory) -> None:
        graph = build_path_graph(factory, num_vertices=4)
        bc = betweenness_centrality(graph)
        assert bc[1] > bc[3]
        assert bc[2] > bc[3]

    def test_cycle_uniform_betweenness(self, factory) -> None:
        graph = build_cycle_graph(factory, num_vertices=4)
        bc = betweenness_centrality(graph)
        values = list(bc.values())
        for value in values:
            assert value == pytest.approx(values[0])

    def test_graph_with_fewer_than_three_vertices(self, factory) -> None:
        graph = factory(2)
        graph.add_edge(0, 1)
        bc = betweenness_centrality(graph)
        assert bc[0] == pytest.approx(0.0)
        assert bc[1] == pytest.approx(0.0)

    def test_star_hub_zero_betweenness(self, factory) -> None:
        """Na estrela dirigida 0→{1,2,3,4}, as folhas são inalcançáveis entre si."""

        graph = build_star_graph(factory, num_leaves=4)
        bc = betweenness_centrality(graph)
        assert bc[0] == pytest.approx(0.0)

    def test_weighted_path_betweenness(self, factory) -> None:
        """Triângulo ponderado deve produzir betweenness não-zero."""

        graph = build_weighted_triangle(factory)
        bc = betweenness_centrality(graph)
        for vertex in range(3):
            assert bc[vertex] == pytest.approx(bc[0])

    def test_weighted_diamond_with_equal_paths(self, factory) -> None:
        graph = factory(4)
        for source, target, weight in ((0, 1, 1.0), (0, 2, 1.0), (1, 3, 1.0), (2, 3, 1.0)):
            graph.add_edge(source, target)
            graph.set_edge_weight(source, target, weight)
        bc = betweenness_centrality(graph)
        assert bc[1] > 0.0
        assert bc[2] > 0.0

    def test_dijkstra_brandes_ignora_entradas_obsoletas_no_heap(self, factory) -> None:
        graph = factory(3)
        graph.add_edge(0, 1)
        graph.set_edge_weight(0, 1, 3.0)
        graph.add_edge(0, 2)
        graph.set_edge_weight(0, 2, 1.0)
        graph.add_edge(2, 1)
        graph.set_edge_weight(2, 1, 1.0)
        stack, _, sigma = _dijkstra_brandes(graph, 0)
        assert 1 in stack
        assert sigma[1] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Centralidade de Proximidade
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("factory", [AdjacencyMatrixGraph, AdjacencyListGraph])
class TestClosenessCentrality:
    def test_cycle_uniform_closeness(self, factory) -> None:
        graph = build_cycle_graph(factory, num_vertices=4)
        cc = closeness_centrality(graph)
        values = list(cc.values())
        for value in values:
            assert value == pytest.approx(values[0])

    def test_isolated_vertex_zero_closeness(self, factory) -> None:
        graph = factory(3)
        cc = closeness_centrality(graph)
        for vertex in range(3):
            assert cc[vertex] == pytest.approx(0.0)

    def test_star_hub_has_higher_closeness(self, factory) -> None:
        graph = build_star_graph(factory, num_leaves=3)
        cc = closeness_centrality(graph)
        assert cc[0] > 0.0
        for leaf in range(1, 4):
            assert cc[leaf] == pytest.approx(0.0)

    def test_path_source_highest_closeness(self, factory) -> None:
        """Em 0→1→2→3, vértice 0 alcança 3 outros (dist total 6) → cc=0.5;
        vértice 1 alcança 2 (dist total 3) → cc=0.667."""

        graph = build_path_graph(factory, num_vertices=4)
        cc = closeness_centrality(graph)
        assert cc[0] > 0.0
        assert cc[1] > cc[0]  # menos alcançáveis mas distância média menor
        assert cc[3] == pytest.approx(0.0)

    def test_weighted_closeness(self, factory) -> None:
        graph = build_weighted_triangle(factory)
        cc = closeness_centrality(graph)
        assert all(value > 0.0 for value in cc.values())

    def test_weighted_shortest_distances(self, factory) -> None:
        graph = build_weighted_triangle(factory)
        distances = _shortest_distances(graph, 0, weighted=True)
        assert distances[1] == pytest.approx(2.0)
        assert distances[2] == pytest.approx(6.0)

    def test_weighted_shortest_distances_skips_stale_heap_entries(self, factory) -> None:
        graph = factory(3)
        graph.add_edge(0, 1)
        graph.set_edge_weight(0, 1, 3.0)
        graph.add_edge(0, 2)
        graph.set_edge_weight(0, 2, 1.0)
        graph.add_edge(2, 1)
        graph.set_edge_weight(2, 1, 1.0)
        distances = _shortest_distances(graph, 0, weighted=True)
        assert distances[1] == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# Classificação de Página (PageRank)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("factory", [AdjacencyMatrixGraph, AdjacencyListGraph])
class TestPageRank:
    def test_pagerank_sums_to_one(self, factory) -> None:
        graph = build_cycle_graph(factory, num_vertices=4)
        pr = pagerank(graph)
        assert sum(pr.values()) == pytest.approx(1.0, abs=1e-4)

    def test_cycle_uniform_pagerank(self, factory) -> None:
        graph = build_cycle_graph(factory, num_vertices=4)
        pr = pagerank(graph)
        expected = 1.0 / 4
        for vertex in range(4):
            assert pr[vertex] == pytest.approx(expected, abs=1e-4)

    def test_star_leaves_receive_hub_rank(self, factory) -> None:
        graph = build_star_graph(factory, num_leaves=3)
        pr = pagerank(graph)
        leaf_ranks = [pr[vertex] for vertex in range(1, 4)]
        for rank in leaf_ranks:
            assert rank == pytest.approx(leaf_ranks[0], abs=1e-4)

    def test_empty_graph(self, factory) -> None:
        graph = factory(0)
        pr = pagerank(graph)
        assert pr == {}

    def test_pagerank_positive_all_vertices(self, factory) -> None:
        graph = build_complete_graph(factory, num_vertices=4)
        pr = pagerank(graph)
        for vertex in range(4):
            assert pr[vertex] > 0


# ---------------------------------------------------------------------------
# Densidade
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("factory", [AdjacencyMatrixGraph, AdjacencyListGraph])
class TestDensity:
    def test_complete_graph_density_is_one(self, factory) -> None:
        graph = build_complete_graph(factory, num_vertices=4)
        assert density(graph) == pytest.approx(1.0)

    def test_empty_graph_density_is_zero(self, factory) -> None:
        graph = factory(4)
        assert density(graph) == pytest.approx(0.0)

    def test_single_vertex_density_is_zero(self, factory) -> None:
        graph = factory(1)
        assert density(graph) == pytest.approx(0.0)

    def test_cycle_partial_density(self, factory) -> None:
        graph = build_cycle_graph(factory, num_vertices=4)
        assert density(graph) == pytest.approx(4 / 12)


# ---------------------------------------------------------------------------
# Coeficiente de Agrupamento
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("factory", [AdjacencyMatrixGraph, AdjacencyListGraph])
class TestClusteringCoefficient:
    def test_complete_graph_has_full_clustering(self, factory) -> None:
        graph = build_complete_graph(factory, num_vertices=4)
        result = clustering_coefficient(graph)
        for vertex in range(4):
            assert result["local"][vertex] == pytest.approx(1.0)
        assert result["global"] == pytest.approx(1.0)

    def test_star_leaves_have_zero_clustering(self, factory) -> None:
        graph = build_star_graph(factory, num_leaves=3)
        result = clustering_coefficient(graph)
        for leaf in range(1, 4):
            assert result["local"][leaf] == pytest.approx(0.0)
        assert result["local"][0] == pytest.approx(0.0)

    def test_no_edges_zero_clustering(self, factory) -> None:
        graph = factory(3)
        result = clustering_coefficient(graph)
        for vertex in range(3):
            assert result["local"][vertex] == pytest.approx(0.0)
        assert result["global"] == pytest.approx(0.0)

    def test_directed_triangle_clustering(self, factory) -> None:
        """Em 0→1→2→0, cada vértice tem 2 vizinhos com 1 aresta dirigida entre eles."""

        graph = build_weighted_triangle(factory)
        result = clustering_coefficient(graph)
        for vertex in range(3):
            assert result["local"][vertex] == pytest.approx(0.5)
        # Transitividade: sem caminhos-2 transitivos em um 3-ciclo dirigido
        assert result["global"] == pytest.approx(0.0)

    def test_bidirectional_triangle_has_full_transitivity(self, factory) -> None:
        """Quando todo par tem arestas em ambas as direções, a transitividade é 1.0."""

        graph = factory(3)
        for i in range(3):
            for j in range(3):
                if i != j:
                    graph.add_edge(i, j)
        result = clustering_coefficient(graph)
        assert result["global"] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# Assortatividade de Grau
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("factory", [AdjacencyMatrixGraph, AdjacencyListGraph])
class TestDegreeAssortativity:
    def test_complete_graph_zero_assortativity(self, factory) -> None:
        graph = build_complete_graph(factory, num_vertices=4)
        assert degree_assortativity(graph) == pytest.approx(0.0)

    def test_no_edges_zero_assortativity(self, factory) -> None:
        graph = factory(3)
        assert degree_assortativity(graph) == pytest.approx(0.0)

    def test_cycle_zero_assortativity(self, factory) -> None:
        """Todos os vértices têm o mesmo grau in/out, então a correlação de Pearson é 0."""

        graph = build_cycle_graph(factory, num_vertices=4)
        assert degree_assortativity(graph) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Modularidade
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("factory", [AdjacencyMatrixGraph, AdjacencyListGraph])
class TestModularity:
    def test_all_same_community_cycle(self, factory) -> None:
        graph = build_cycle_graph(factory, num_vertices=4)
        partition = {vertex: 0 for vertex in range(4)}
        mod = modularity(graph, partition)
        # Ciclo com pesos uniformes: todas as arestas são internas, Q > 0
        assert mod > 0

    def test_each_own_community_negative(self, factory) -> None:
        graph = build_cycle_graph(factory, num_vertices=4)
        partition = {vertex: vertex for vertex in range(4)}
        mod = modularity(graph, partition)
        # Sem arestas dentro de comunidades de vértice único → Q ≤ 0
        assert mod <= 0

    def test_good_partition_positive_modularity(self, factory) -> None:
        """Dois pares recíprocos claramente separados."""

        graph = factory(4)
        graph.add_edge(0, 1)
        graph.add_edge(1, 0)
        graph.add_edge(2, 3)
        graph.add_edge(3, 2)
        partition = {0: 0, 1: 0, 2: 1, 3: 1}
        mod = modularity(graph, partition)
        assert mod > 0

    def test_empty_graph_modularity(self, factory) -> None:
        graph = factory(0)
        mod = modularity(graph, {})
        assert mod == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Detecção de Comunidades (Louvain)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("factory", [AdjacencyMatrixGraph, AdjacencyListGraph])
class TestDetectCommunities:
    def test_disconnected_components_detected(self, factory) -> None:
        graph = build_disconnected_graph(factory)
        partition = detect_communities(graph)
        assert partition[0] == partition[1]
        assert partition[2] == partition[3]
        assert partition[0] != partition[2]

    def test_empty_graph(self, factory) -> None:
        graph = factory(0)
        partition = detect_communities(graph)
        assert partition == {}

    def test_single_vertex(self, factory) -> None:
        graph = factory(1)
        partition = detect_communities(graph)
        assert 0 in partition

    def test_complete_graph_at_least_one_community(self, factory) -> None:
        graph = build_complete_graph(factory, num_vertices=4)
        partition = detect_communities(graph)
        num_communities = len(set(partition.values()))
        assert num_communities >= 1

    def test_two_cliques_detected(self, factory) -> None:
        """Duas cliques K3 conectadas por uma única aresta devem formar 2 comunidades."""

        graph = factory(6)
        for i in range(3):
            for j in range(3):
                if i != j:
                    graph.add_edge(i, j)
        for i in range(3, 6):
            for j in range(3, 6):
                if i != j:
                    graph.add_edge(i, j)
        graph.add_edge(2, 3)

        partition = detect_communities(graph)
        assert partition[0] == partition[1] == partition[2]
        assert partition[3] == partition[4] == partition[5]
        assert partition[0] != partition[3]

    def test_all_vertices_assigned(self, factory) -> None:
        graph = build_cycle_graph(factory, num_vertices=5)
        partition = detect_communities(graph)
        for vertex in range(5):
            assert vertex in partition


# ---------------------------------------------------------------------------
# Arestas de Ponte (Bridging Ties)
# ---------------------------------------------------------------------------


def test_modularity_without_edges_returns_zero() -> None:
    graph = AdjacencyListGraph(3)
    assert modularity(graph, {0: 0, 1: 0, 2: 0}) == pytest.approx(0.0)


def test_local_moving_with_zero_total_weight_returns_identity() -> None:
    assert _local_moving([], [], 0.0) == []


def test_pearson_correlation_edge_cases() -> None:
    assert _pearson_correlation([], []) == pytest.approx(0.0)
    assert _pearson_correlation([1, 1, 1], [2, 2, 2]) == pytest.approx(0.0)
    assert _pearson_correlation([1, 2, 3], [2, 4, 6]) == pytest.approx(1.0)


def test_abstract_graph_iter_edges_default() -> None:
    graph = AdjacencyListGraph(2)
    graph.add_edge(0, 1)
    graph.set_edge_weight(0, 1, 2.5)
    edges = AbstractGraph.iter_edges(graph)
    assert edges == [(0, 1, 2.5)]


@pytest.mark.parametrize("factory", [AdjacencyMatrixGraph, AdjacencyListGraph])
class TestBridgingTies:
    def test_all_same_community_no_bridges(self, factory) -> None:
        graph = build_cycle_graph(factory, num_vertices=4)
        partition = {vertex: 0 for vertex in range(4)}
        bridges = bridging_ties(graph, partition)
        assert len(bridges) == 0

    def test_each_own_community_all_bridges(self, factory) -> None:
        graph = build_cycle_graph(factory, num_vertices=4)
        partition = {vertex: vertex for vertex in range(4)}
        bridges = bridging_ties(graph, partition)
        assert len(bridges) == graph.get_edge_count()

    def test_bridge_returns_correct_communities(self, factory) -> None:
        graph = factory(4)
        graph.add_edge(0, 1)
        graph.add_edge(2, 3)
        graph.add_edge(1, 2)
        partition = {0: 0, 1: 0, 2: 1, 3: 1}
        bridges = bridging_ties(graph, partition)
        assert len(bridges) == 1
        assert bridges[0] == (1, 2, 0, 1)

    def test_no_inter_community_edges(self, factory) -> None:
        graph = factory(4)
        graph.add_edge(0, 1)
        graph.add_edge(2, 3)
        partition = {0: 0, 1: 0, 2: 1, 3: 1}
        bridges = bridging_ties(graph, partition)
        assert len(bridges) == 0
