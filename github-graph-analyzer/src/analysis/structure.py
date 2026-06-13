from __future__ import annotations

import math

from src.graph.abstract_graph import AbstractGraph


# ---------------------------------------------------------------------------
# API Pública
# ---------------------------------------------------------------------------


def density(graph: AbstractGraph) -> float:
    """Calcula a densidade de um grafo dirigido.

    Fórmula: ``|E| / (|V| × (|V| - 1))``.

    Args:
        graph: Um grafo simples dirigido.

    Returns:
        Valor de densidade em ``[0.0, 1.0]``.
    """

    vertex_count = graph.get_vertex_count()
    if vertex_count <= 1:
        return 0.0
    max_edges = vertex_count * (vertex_count - 1)
    return graph.get_edge_count() / max_edges


def clustering_coefficient(graph: AbstractGraph) -> dict[str, object]:
    """Calcula o coeficiente de agrupamento dirigido (local e global).

    **Local** — para cada vértice *v*, a proporção de arestas dirigidas entre
    seus vizinhos (união de vizinhos de entrada e saída) em relação ao máximo
    possível de arestas dirigidas entre esses vizinhos.

    **Global** (transitividade) — razão entre triplas dirigidas fechadas e
    todas as triplas dirigidas. Uma tripla centrada em *j* é ``(i → j → k)``
    com ``i ≠ k``; ela é *fechada* quando ``i → k`` também existe.

    Args:
        graph: Um grafo simples dirigido.

    Returns:
        ``{"local": {vértice: float}, "global": float}``.
    """

    vertex_count = graph.get_vertex_count()
    out_neighbors, in_neighbors = _build_neighbor_sets(graph)

    local_cc: dict[int, float] = {}
    total_triangles = 0
    total_triplets = 0

    for vertex in range(vertex_count):
        neighbors = out_neighbors[vertex] | in_neighbors[vertex]
        neighbor_count = len(neighbors)

        if neighbor_count < 2:
            local_cc[vertex] = 0.0
            continue

        # Contagem de arestas direcionadas entre vizinhos
        edge_count_among = 0
        for j in neighbors:
            for k in neighbors:
                if j != k and graph.has_edge(j, k):
                    edge_count_among += 1

        max_possible = neighbor_count * (neighbor_count - 1)
        local_cc[vertex] = edge_count_among / max_possible

        # Transitividade: triplas dirigidas centradas em vertex
        # Tripla: (predecessor → vertex → successor), predecessor ≠ successor
        for predecessor in in_neighbors[vertex]:
            for successor in out_neighbors[vertex]:
                if predecessor != successor:
                    total_triplets += 1
                    if graph.has_edge(predecessor, successor):
                        total_triangles += 1

    global_cc = total_triangles / total_triplets if total_triplets > 0 else 0.0

    return {"local": local_cc, "global": global_cc}


def degree_assortativity(graph: AbstractGraph) -> float:
    """Calcula a assortatividade de grau usando o coeficiente de correlação de Pearson.

    Para cada aresta dirigida ``(u → v)``, o grau de saída da origem e o grau
    de entrada do destino são pareados. A correlação de Pearson sobre todas
    as arestas é retornada.

    Args:
        graph: Um grafo simples dirigido.

    Returns:
        Coeficiente em ``[-1.0, 1.0]``, ou ``0.0`` quando indefinido.
    """

    edges = graph.iter_edges()
    if not edges:
        return 0.0

    source_degrees: list[int] = []
    target_degrees: list[int] = []
    for source, target, _ in edges:
        source_degrees.append(graph.get_vertex_out_degree(source))
        target_degrees.append(graph.get_vertex_in_degree(target))

    return _pearson_correlation(source_degrees, target_degrees)


# ---------------------------------------------------------------------------
# Funções auxiliares internas
# ---------------------------------------------------------------------------


def _build_neighbor_sets(
    graph: AbstractGraph,
) -> tuple[list[set[int]], list[set[int]]]:
    """Constrói os conjuntos de vizinhos de saída e de entrada a partir do grafo."""

    vertex_count = graph.get_vertex_count()
    out_neighbors: list[set[int]] = [set() for _ in range(vertex_count)]
    in_neighbors: list[set[int]] = [set() for _ in range(vertex_count)]
    for source, target, _ in graph.iter_edges():
        out_neighbors[source].add(target)
        in_neighbors[target].add(source)
    return out_neighbors, in_neighbors


def _pearson_correlation(x_values: list[int], y_values: list[int]) -> float:
    """Calcula o coeficiente de correlação de Pearson entre duas sequências."""

    count = len(x_values)
    if count == 0:
        return 0.0

    mean_x = sum(x_values) / count
    mean_y = sum(y_values) / count

    covariance = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
    var_x = sum((x - mean_x) ** 2 for x in x_values)
    var_y = sum((y - mean_y) ** 2 for y in y_values)

    denominator = math.sqrt(var_x * var_y)
    if denominator == 0:
        return 0.0

    return covariance / denominator
